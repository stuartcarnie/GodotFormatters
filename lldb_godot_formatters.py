# Description: Godot formatters for lldb

# Add the following lines to your ~/.lldbinit, or run this line directly in the debug console:
# `command script import <PATH_TO_SCRIPT>/lldb_godot_formatters.py`


import datetime
import shlex
import sys
from time import sleep
import traceback
import optparse
import re

from types import TracebackType
from typing import final, Optional

# fmt: off
from lldb import (SBCommandReturnObject, SBExecutionContext, SBTypeCategory, eFormatBytes, eFormatUnicode32, eNoDynamicValues, eDynamicDontRunTarget, eDynamicCanRunTarget, eBasicTypeInvalid, eBasicTypeVoid, eBasicTypeChar, 
                  eBasicTypeSignedChar, eBasicTypeUnsignedChar, eBasicTypeWChar, eBasicTypeSignedWChar, eBasicTypeUnsignedWChar, eBasicTypeChar16, eBasicTypeChar32, 
                  eBasicTypeChar8, eBasicTypeShort, eBasicTypeUnsignedShort, eBasicTypeInt, eBasicTypeUnsignedInt, eBasicTypeLong, eBasicTypeUnsignedLong, eBasicTypeLongLong, 
                  eBasicTypeUnsignedLongLong, eBasicTypeInt128, eBasicTypeUnsignedInt128, eBasicTypeBool, eBasicTypeHalf, eBasicTypeFloat, eBasicTypeDouble, eBasicTypeLongDouble, 
                  eBasicTypeFloatComplex, eBasicTypeDoubleComplex, eBasicTypeLongDoubleComplex, eBasicTypeObjCID, eBasicTypeObjCClass, eBasicTypeObjCSel, eBasicTypeNullPtr, eReturnStatusSuccessFinishNoResult, eReturnStatusSuccessFinishResult, 
                  eTypeClassClass, eTypeClassEnumeration, eTypeClassPointer, eTypeOptionCascade)
from lldb import ( SBValue, SBAddress, SBData, SBType, SBTypeEnumMember, SBTypeEnumMemberList, SBSyntheticValueProvider, SBError, SBTarget, SBDebugger, SBTypeSummary, SBTypeSynthetic, SBTypeNameSpecifier)
# fmt: on
from enum import Enum
import weakref

from numpy import isin

UINT32_MAX = 4294967295
INT32_MAX = 2147483647


class GodotFormatterOptions:
    PRINT_VERBOSE = False
    PRINT_TRACE = False
    SUMMARY_STRING_MAX_LENGTH = 100
    MAX_AMOUNT_OF_CHILDREN_IN_SUMMARY = 6
    NAMED_COLOR_ANNOTATION = True
    MAP_KEY_VAL_STYLE = True
    SANITIZE_STRING_SUMMARY = True
    MIDEBUGGER_COMPAT = False
    FILTER = ""  #'"' + '" , "'.join([".*update.*", ".*__init__.*"]) + '"'


def get_filter():
    if not Opts.FILTER:
        return []
    thing = [s.strip('"') for s in shlex.split(Opts.FILTER) if s != ","]
    return thing


HELP_STRING_MAP = {
    "PRINT_VERBOSE": "Print verbose output",
    "PRINT_TRACE": "Print trace output",
    "SUMMARY_STRING_MAX_LENGTH": "Maximum length of a summary string",
    "MAX_AMOUNT_OF_CHILDREN_IN_SUMMARY": "Maximum amount of children to display in a summary string",
    "NAMED_COLOR_ANNOTATION": "Annotate color summaries with their named color if applicable",
    "MAP_KEY_VAL_STYLE": 'Display children in Map-like templates in a key-value list style (e.g. ["key"] = "value").\nIf false, will display children in an indexed-list style (e.g. [0] = ["key"]: "value")',
    "SANITIZE_STRING_SUMMARY": "Sanitize string summaries to escape all formatting characters and quotes",
    "MIDEBUGGER_COMPAT": "Force compatibility settings with the MIDebugger interface (i.e. the official MS C++ vscode debugger `cppdbg`).\nThis is not necessary if using a native LLDB interface (e.g. `codelldb` debugger extension for vscode)",
    "FILTER": "List of regex filters to apply to trace output",
}


def force_compat(force_mi_compat: bool):
    if force_mi_compat:
        # MIDebugger refuses to display map children when this is True, forced to False
        Opts.MAP_KEY_VAL_STYLE = False
        # MIDebugger chokes and dies when there are mixed escaped and non-escaped quotes in a string summary, so this is forced to be True
        Opts.SANITIZE_STRING_SUMMARY = True


Opts: GodotFormatterOptions = GodotFormatterOptions()

# Summary string formats
NULL_SUMMARY = "<null>"
NIL_SUMMARY = "<nil>"  # Variant nil
EMPTY_SUMMARY = "<empty>"  # Empty string, nodepath, etc.
INVALID_SUMMARY = "<invalid>"  # Invalid pointer, uninitialized objects, etc.
LIST_FORMAT = "{type_no_template}[{size}]{{{children}}}"

# Synthetic list-like configs; because linked-lists need to traverse the list to get a specific element, we need to cache the members to be performant.
NO_CACHE_MEMBERS = False
CACHE_MIN = 500
CACHE_FETCH_MAX = 5000

STRINGS_STILL_32_BIT = True  # if true, strings are still 32-bit
MAX_DEPTH = 3


# Compatibility settings


class VariantType(Enum):
    NIL = 0
    BOOL = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    VECTOR2 = 5
    VECTOR2I = 6
    RECT2 = 7
    RECT2I = 8
    VECTOR3 = 9
    VECTOR3I = 10
    TRANSFORM2D = 11
    VECTOR4 = 12
    VECTOR4I = 13
    PLANE = 14
    QUATERNION = 15
    AABB = 16
    BASIS = 17
    TRANSFORM3D = 18
    PROJECTION = 19
    COLOR = 20
    STRING_NAME = 21
    NODE_PATH = 22
    RID = 23
    OBJECT = 24
    CALLABLE = 25
    SIGNAL = 26
    DICTIONARY = 27
    ARRAY = 28
    PACKED_BYTE_ARRAY = 29
    PACKED_INT32_ARRAY = 30
    PACKED_INT64_ARRAY = 31
    PACKED_FLOAT32_ARRAY = 32
    PACKED_FLOAT64_ARRAY = 33
    PACKED_STRING_ARRAY = 34
    PACKED_VECTOR2_ARRAY = 35
    PACKED_VECTOR3_ARRAY = 36
    PACKED_COLOR_ARRAY = 37
    VARIANT_MAX = 38


def print_verbose(val: str):
    if Opts.PRINT_VERBOSE or Opts.PRINT_TRACE:
        print(val)


def print_trace(val: str, *args, **kwargs):
    if Opts.PRINT_TRACE:
        # curr_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
        # format = f"[{curr_time}] {val}"
        print(val, *args, **kwargs)


def self_none_if_invalid(func):
    def wrapper(*args, **kwargs):
        if not not_null_check(args[1]):
            return None
        return func(*args, **kwargs)

    return wrapper


def self_zero_if_invalid(func):
    def wrapper(*args, **kwargs):
        if not not_null_check(args[1]):
            return 0
        return func(*args, **kwargs)

    return wrapper


def get_start_tr_format(func_name: str):
    global level
    return ("  " * level) + func_name + " {"


def get_end_tr_format(func_name: str):
    global level
    return ("  " * level) + "} // " + func_name


def get_func_name(func, args):
    return str(func.__qualname__)


def get_arg_str(arg):
    # check if this can be turned into a string
    ret = "<unknown>"
    if arg is None:
        return "None"
    if hasattr(arg, "GetName") or isinstance(arg, SBValue) or isinstance(arg, SBType):
        return get_valobj_name(arg)
    if isinstance(arg, str) or hasattr(arg, "__str__"):
        ret = str(arg)
        if not (ret.startswith("<") and ret.endswith(">") and "object at" in ret):
            return ret
        else:
            ret = ret.split(" ")[0] + ">"
    if hasattr(arg, "__class__"):
        return "<" + arg.__class__.__name__ + ">"
    return ret


def _mk_func_call(func, *args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0:
        return func(args[0])
    return func(*args, **kwargs)


def mk_func_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error calling {func.__name__}")
        print(f"Args length: {len(args)}")
        print(f"kwargs length: {len(kwargs)}")
        is_method = "." in func.__qualname__

        def sanitize(i, arg):
            if i == 0 and is_method:
                return "self"
            elif isinstance(arg, dict):
                return "<dict>"
            return arg

        args_str = ", ".join([get_arg_str(sanitize(i, arg)) for i, arg in enumerate(args)])
        print(f"Args: {args_str}")
        kwargs_str = ", ".join([f"{key}={get_arg_str(val)}" for key, val in kwargs.items()])
        print(f"Kwargs: {kwargs_str}")
        print(str(e))
        traceback.print_exc()
        sleep(2)
        return None


level = 0


def trace_func_call(func, *args, **kwargs):
    global level
    func_name = str(func.__qualname__)
    is_method = "." in func_name
    filters = get_filter()
    # filters = []
    matched = len(filters) == 0
    for filter in get_filter():
        regex = re.compile(filter)
        if regex.match(func_name):
            matched = True
            break
    if not matched:
        return _mk_func_call(func, *args, **kwargs)
    func_name = (
        func_name.replace("SynthProvider", "SP")
        .replace("SummaryProvider", "SumProv")
        .replace("SyntheticProvider", "SP")
    )
    if len(args) > 0 and isinstance(args[0], GodotSynthProvider) and hasattr(args[0], "valobj"):
        func_name += f"<{get_valobj_name(args[0].valobj)}>"

    def sanitize(i, arg):
        if i == 0 and is_method:
            return "self"
        elif isinstance(arg, dict):
            return "<dict>"
        return arg

    args_str = ", ".join([get_arg_str(sanitize(i, arg)) for i, arg in enumerate(args)])
    args_str += ", ".join([f"{key}={get_arg_str(val)}" for key, val in kwargs.items()])
    print_trace(get_start_tr_format(f"{func_name}({args_str})"))
    level += 1
    ret = mk_func_call(func, *args, **kwargs)
    level -= 1
    ret_str = get_arg_str(ret)
    print_trace(get_end_tr_format(func_name) + f" -> {ret_str}")
    return ret


def get_gsp_print_str(func_name: str, args):
    if len(args) > 0 and isinstance(args[0], GodotSynthProvider):
        valobj = None
        if hasattr(args[0], "valobj"):
            valobj = args[0].valobj
        return get_start_tr_format(func_name) + f" on {get_valobj_name(valobj)}"
    return get_start_tr_format(func_name)


def print_trace_dec(func):
    def _pr_trace_wrap(*args, **kwargs):
        return trace_func_call(func, *args, **kwargs)

    if not Opts.PRINT_TRACE:
        return func
    _pr_trace_wrap.__name__ = func.__name__
    _pr_trace_wrap.__qualname__ = func.__qualname__
    return _pr_trace_wrap


def trace_none_if_invalid_dec(func):
    def wrapper(*args, **kwargs):
        if not not_null_check(args[1]):
            func_name = get_func_name(func, args)
            print_trace(get_gsp_print_str(func_name, args))
            print_trace(get_end_tr_format(func_name) + ": Aborting due to invalid args[1]")
            return None
        return trace_func_call(func, *args, **kwargs)

    if not Opts.PRINT_TRACE:
        return self_none_if_invalid(func)
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return wrapper


def GetFloat(valobj: SBValue) -> float:
    dataArg: SBData = valobj.GetData()
    if valobj.GetByteSize() > 4:
        # real_t is a double
        return dataArg.GetDouble(SBError(), 0)  # type: ignore
    else:
        # real_t is a float
        return dataArg.GetFloat(SBError(), 0)  # type: ignore


def GetFloatStr(valobj: SBValue, short: bool = False) -> str:
    val = GetFloat(valobj)
    if short:
        return "{:.3f}".format(val)
    return str(val)


@print_trace_dec
def Variant_GetValue(valobj: SBValue):
    # we need to get the type of the variant
    type = valobj.GetChildMemberWithName("type").GetValueAsUnsigned()
    # switch on type
    data: SBValue = valobj.GetChildMemberWithName("_data")
    mem: SBValue = data.GetChildMemberWithName("_mem")
    mem_addr: SBAddress = mem.GetAddress()
    packed_array: SBValue = data.GetChildMemberWithName("packed_array")
    packed_array_addr: SBAddress = packed_array.GetAddress()
    target: SBTarget = valobj.target
    if type == VariantType.NIL.value:
        return None
    elif type == VariantType.BOOL.value:
        return data.GetChildMemberWithName("_bool")
    elif type == VariantType.INT.value:
        return data.GetChildMemberWithName("_int")
    elif type == VariantType.FLOAT.value:
        return data.GetChildMemberWithName("_float")
    elif type == VariantType.TRANSFORM2D.value:
        _transform2d = data.GetChildMemberWithName("_transform2d")
        if is_valid_pointer(_transform2d):
            return _transform2d
        else:
            return None
    elif type == VariantType.AABB.value:
        _aabb = data.GetChildMemberWithName("_aabb")
        if is_valid_pointer(_aabb):
            return _aabb
        else:
            return None
    elif type == VariantType.BASIS.value:
        _basis = data.GetChildMemberWithName("_basis")
        if is_valid_pointer(_basis):
            return _basis
        else:
            return None
    elif type == VariantType.TRANSFORM3D.value:
        _transform3d = data.GetChildMemberWithName("_transform3d")
        if is_valid_pointer(_transform3d):
            return _transform3d
        else:
            return None
    elif type == VariantType.PROJECTION.value:
        _projection = data.GetChildMemberWithName("_projection")
        if is_valid_pointer(_projection):
            return _projection
        else:
            return None
    elif type == VariantType.STRING.value:  # For _mem values, we have to cast them to the correct type
        # find the type for "String"
        stringType: SBType = target.FindFirstType("::String")
        string: SBValue = target.CreateValueFromAddress("[string]", mem_addr, stringType)
        return string
    elif type == VariantType.VECTOR2.value:
        vector2Type: SBType = target.FindFirstType("::Vector2")
        vector2: SBValue = target.CreateValueFromAddress("[vector2]", mem_addr, vector2Type)
        return vector2
    elif type == VariantType.VECTOR2I.value:
        vector2IType: SBType = target.FindFirstType("::Vector2i")
        vector2i: SBValue = target.CreateValueFromAddress("[vector2i]", mem_addr, vector2IType)
        return vector2i
    elif type == VariantType.RECT2.value:
        rect2Type: SBType = target.FindFirstType("::Rect2")
        rect2: SBValue = target.CreateValueFromAddress("[rect2]", mem_addr, rect2Type)
        return rect2
    elif type == VariantType.RECT2I.value:
        rect2IType: SBType = target.FindFirstType("::Rect2i")
        rect2i: SBValue = target.CreateValueFromAddress("[rect2i]", mem_addr, rect2IType)
        return rect2i
    elif type == VariantType.VECTOR3.value:
        vector3Type: SBType = target.FindFirstType("::Vector3")
        vector3: SBValue = target.CreateValueFromAddress("[vector3]", mem_addr, vector3Type)
        return vector3
    elif type == VariantType.VECTOR3I.value:
        vector3iType: SBType = target.FindFirstType("::Vector3i")
        vector3i: SBValue = target.CreateValueFromAddress("[vector3i]", mem_addr, vector3iType)
        return vector3i
    elif type == VariantType.VECTOR4.value:
        vector4Type: SBType = target.FindFirstType("::Vector4")
        vector4: SBValue = target.CreateValueFromAddress("[vector4]", mem_addr, vector4Type)
        return vector4
    elif type == VariantType.VECTOR4I.value:
        vector4iType: SBType = target.FindFirstType("::Vector4i")
        vector4i: SBValue = target.CreateValueFromAddress("[vector4i]", mem_addr, vector4iType)
        return vector4i
    elif type == VariantType.PLANE.value:
        planeType: SBType = target.FindFirstType("::Plane")
        plane: SBValue = target.CreateValueFromAddress("[plane]", mem_addr, planeType)
        return plane
    elif type == VariantType.QUATERNION.value:
        quaternionType: SBType = target.FindFirstType("::Quaternion")
        quaternion: SBValue = target.CreateValueFromAddress("[quaternion]", mem_addr, quaternionType)
        return quaternion
    elif type == VariantType.COLOR.value:
        colorType: SBType = target.FindFirstType("::Color")
        color: SBValue = target.CreateValueFromAddress("[color]", mem_addr, colorType)
        return color
    elif type == VariantType.STRING_NAME.value:
        stringNameType: SBType = target.FindFirstType("::StringName")
        stringName: SBValue = target.CreateValueFromAddress("[stringName]", mem_addr, stringNameType)
        return stringName
    elif type == VariantType.NODE_PATH.value:
        nodePathType: SBType = target.FindFirstType("::NodePath")
        nodePath: SBValue = target.CreateValueFromAddress("[nodePath]", mem_addr, nodePathType)
        return nodePath
    elif type == VariantType.RID.value:
        ridType: SBType = target.FindFirstType("::RID")
        rid: SBValue = target.CreateValueFromAddress("[rid]", mem_addr, ridType)
        return rid
    elif type == VariantType.OBJECT.value:
        objDataType: SBType = target.FindFirstType("Variant::ObjData")
        objData: SBValue = target.CreateValueFromAddress("[objData]", mem_addr, objDataType)
        return objData.GetChildMemberWithName("obj")
    elif type == VariantType.CALLABLE.value:
        callableType: SBType = target.FindFirstType("::Callable")
        callable: SBValue = target.CreateValueFromAddress("[callable]", mem_addr, callableType)
        return callable
    elif type == VariantType.SIGNAL.value:
        signalType: SBType = target.FindFirstType("::Signal")
        signal: SBValue = target.CreateValueFromAddress("[signal]", mem_addr, signalType)
        return signal
    elif type == VariantType.DICTIONARY.value:
        dictionaryType: SBType = target.FindFirstType("::Dictionary")
        dictionary: SBValue = target.CreateValueFromAddress("[dictionary]", mem_addr, dictionaryType)
        return dictionary
    elif type == VariantType.ARRAY.value:
        arrayType: SBType = target.FindFirstType("::Array")
        array: SBValue = target.CreateValueFromAddress("[array]", mem_addr, arrayType)
        return array
    else:
        if not is_valid_pointer(packed_array):
            return None
        if type == VariantType.PACKED_BYTE_ARRAY.value:
            packedByteArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<unsigned char>")
            packedByteArray: SBValue = target.CreateValueFromAddress(
                "packedByteArrayref", packed_array_addr, packedByteArrayType
            )
            return packedByteArray.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_INT32_ARRAY.value:
            packedInt32ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<int>")
            packedInt32Array: SBValue = target.CreateValueFromAddress(
                "packedInt32Arrayref", packed_array_addr, packedInt32ArrayType
            )
            return packedInt32Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_INT64_ARRAY.value:
            packedInt64ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<long long>")
            packedInt64Array: SBValue = target.CreateValueFromAddress(
                "packedInt64Arrayref", packed_array_addr, packedInt64ArrayType
            )
            return packedInt64Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_FLOAT32_ARRAY.value:
            packedFloat32ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<float>")
            packedFloat32Array: SBValue = target.CreateValueFromAddress(
                "packedFloat32Arrayref", packed_array_addr, packedFloat32ArrayType
            )
            return packedFloat32Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_FLOAT64_ARRAY.value:
            packedFloat64ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<double>")
            packedFloat64Array: SBValue = target.CreateValueFromAddress(
                "packedFloat64Arrayref", packed_array_addr, packedFloat64ArrayType
            )
            return packedFloat64Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_VECTOR2_ARRAY.value:
            packedVector2ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Vector2>")
            packedVector2Array: SBValue = target.CreateValueFromAddress(
                "packedVector2Arrayref", packed_array_addr, packedVector2ArrayType
            )
            return packedVector2Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_VECTOR3_ARRAY.value:
            packedVector3ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Vector3>")
            packedVector3Array: SBValue = target.CreateValueFromAddress(
                "packedVector3Arrayref", packed_array_addr, packedVector3ArrayType
            )
            return packedVector3Array.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_STRING_ARRAY.value:
            packedStringArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<String>")
            packedStringArray: SBValue = target.CreateValueFromAddress(
                "packedStringArrayref", packed_array_addr, packedStringArrayType
            )
            return packedStringArray.GetChildMemberWithName("array")
        elif type == VariantType.PACKED_COLOR_ARRAY.value:
            packedColorArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Color>")
            packedColorArray: SBValue = target.CreateValueFromAddress(
                "packedColorArrayref", packed_array_addr, packedColorArrayType
            )
            return packedColorArray.GetChildMemberWithName("array")
    return None


class _SBSyntheticValueProviderWithSummary(SBSyntheticValueProvider):
    def get_summary(self) -> str:
        raise Exception("Not implemented")

    def check_valid(self, obj: SBValue) -> bool:
        raise Exception("Not implemented")


import json


def get_valobj_name(valobj: SBValue) -> str:
    fmt = "-{0}-"
    if valobj is None or not hasattr(valobj, "GetName"):
        return fmt.format("NULL")
    elif not valobj.IsValid():
        return "<INVALID>"
    return fmt.format(valobj.GetName())


@print_trace_dec
def get_synth_summary(synth_class, valobj: SBValue, dict):
    obj = valobj
    if valobj.IsSynthetic():
        obj = valobj.GetNonSyntheticValue()
    synth = synth_class(obj, dict, True)
    summary = synth.get_summary()
    return summary


class GodotSynthProvider(_SBSyntheticValueProviderWithSummary):
    synth_by_id: weakref.WeakValueDictionary[int, _SBSyntheticValueProviderWithSummary] = weakref.WeakValueDictionary()
    next_id = 0

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        self.valobj = valobj
        self.internal_dict = internal_dict
        self.is_summary = is_summary
        self.obj_id = GodotSynthProvider.next_id

    # SBSyntheticValueProvider, override these
    def num_children(self, max=UINT32_MAX) -> int:
        raise Exception("Not implemented")

    @print_trace_dec
    def update(self) -> None:
        pass

    def has_children(self) -> bool:
        raise Exception("Not implemented")

    def get_child_at_index(self, idx) -> SBValue:
        raise Exception("Not implemented")

    # Don't override this, override get_index_of_child instead
    @print_trace_dec
    def get_child_index(self, name: str) -> Optional[int]:
        if name == "$$object-id$$":
            return self.obj_id
        try:
            return self.get_index_of_child(name)
        except Exception as e:
            print_verbose(str(e))
            raise e

    @print_trace_dec
    def get_index_of_child(self, name: str) -> Optional[int]:
        raise Exception("Not implemented")

    # _SBSyntheticValueProviderWithSummary
    @print_trace_dec
    def get_summary(self) -> str:
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        return GenericShortSummary(self.valobj, self.internal_dict)

    def check_valid(self, obj: SBValue) -> bool:
        print("check_valid not implemented")
        return False


class Variant_SyntheticProvider(GodotSynthProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)
        self.update()

    @print_trace_dec
    def check_valid(self, obj: SBValue) -> bool:
        variant_type = obj.GetChildMemberWithName("type").GetValueAsUnsigned()
        data = Variant_GetValue(obj)
        if variant_type < VariantType.NIL.value or variant_type >= VariantType.VARIANT_MAX.value:
            return False
        if VariantType.NIL.value == variant_type:
            return True
        if data is None or not data.IsValid():
            return False
        return True

    @print_trace_dec
    def _get_variant_type(self):
        return self.valobj.GetChildMemberWithName("type").GetValueAsUnsigned()

    @print_trace_dec
    def update(self):
        self.data = Variant_GetValue(self.valobj)
        self.variant_type = self._get_variant_type()

    @print_trace_dec
    def get_summary(self):
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        type = self.variant_type
        if type == VariantType.NIL.value:
            return NIL_SUMMARY
        data = self.data
        if type == VariantType.BOOL.value:
            return "true" if data.GetValueAsUnsigned() != 0 else "false"
        elif type == VariantType.INT.value:
            return str(data.GetValueAsSigned())
        elif type == VariantType.FLOAT.value:
            return GetFloatStr(data)
        elif type == VariantType.OBJECT.value:
            prefix = "{" + str(data.GetType().GetPointeeType().GetDisplayTypeName()) + "*:"
            # TODO: avoiding infinite recursion here by not calling GenericShortSummary
            # return prefix + GenericShortSummary(data, self.internal_dict, len(prefix)+1, True) + "}"
            return prefix + "{...}}"
        else:
            summary = data.GetSummary()
            if not summary:
                summary = "{" + data.GetDisplayTypeName() + ":{...}}"
            return summary

    def num_children(self, max=UINT32_MAX):
        if self.variant_type <= VariantType.NIL.value or self.variant_type >= VariantType.VARIANT_MAX.value:
            return 0
        else:
            if self.data is None:
                return 0
            return 1

    def has_children(self):
        return self.num_children() != 0

    def get_index_of_child(self, name: str):
        return 0 if self.has_children() else None

    def get_child_at_index(self, index):
        return self.data


def StringName_SummaryProvider(valobj: SBValue, internal_dict):
    _data: SBValue = valobj.GetChildMemberWithName("_data")
    if _data.GetValueAsUnsigned() == 0:
        return NULL_SUMMARY
    if _data.GetChildMemberWithName("cname").GetValueAsUnsigned() == 0:
        return _data.GetChildMemberWithName("name").GetSummary()
    else:
        return _data.GetChildMemberWithName("cname").GetSummary()


def Ref_SummaryProvider(valobj: SBValue, internal_dict):
    return GenericShortSummary(valobj, internal_dict)


def strip_quotes(val: str):
    if val.startswith('U"'):
        val = val.removeprefix('U"').removesuffix('"')
    else:
        val = val.removeprefix('"').removesuffix('"')
    return val


def NodePath_SummaryProvider(valobj: SBValue, internal_dict):
    rstr = ""
    data: SBValue = valobj.GetChildMemberWithName("data")
    if data.GetValueAsUnsigned() == 0:
        return NULL_SUMMARY
    if not is_valid_pointer(data):
        return INVALID_SUMMARY
    path = Vector_SyntheticProvider(data.GetChildMemberWithName("path").GetNonSyntheticValue(), internal_dict)
    subpath = Vector_SyntheticProvider(data.GetChildMemberWithName("subpath").GetNonSyntheticValue(), internal_dict)
    path_size = path.num_children()
    subpath_size = subpath.num_children()
    if path_size == 0 and subpath_size == 0:
        return EMPTY_SUMMARY
    is_absolute = data.GetChildMemberWithName("absolute").GetValueAsUnsigned()
    if is_absolute != 0:
        rstr = "/"
    for i in range(path_size):
        rstr += strip_quotes(path.get_child_at_index(i).GetSummary())
        if i < path.num_children() - 1:
            rstr += "/"
    if subpath_size > 0:
        rstr += ":"
    for i in range(subpath_size):
        rstr += strip_quotes(subpath.get_child_at_index(i).GetSummary())
        if i < subpath_size - 1:
            rstr += ":"
    return rstr


@print_trace_dec
def Quaternion_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{{0}, {1}, {2}, {3}}}".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
        GetFloat(valobj.GetChildMemberWithName("w")),
    )


@print_trace_dec
def ObjectID_SummaryProvider(valobj: SBValue, internal_dict):
    fmt = "<ObjectID={0}>"
    id: SBValue = valobj.GetChildMemberWithName("id")
    if not id.IsValid():
        return fmt.format(INVALID_SUMMARY)
    val = id.GetValueAsUnsigned()
    if val == 0:
        return fmt.format(NULL_SUMMARY)
    return fmt.format(val)


@print_trace_dec
def Signal_SummaryProvider(valobj: SBValue, internal_dict):
    # Signal has a StringName name and an ObjectID object
    name: SBValue = valobj.GetChildMemberWithName("name")
    object: SBValue = valobj.GetChildMemberWithName("object")
    name_summary, object_summary = name.GetSummary(), object.GetSummary()
    if not name_summary or not object_summary:
        return INVALID_SUMMARY
    if NULL_SUMMARY in name_summary and NULL_SUMMARY in object_summary:
        return "{{<Signal> {0}}}".format(NULL_SUMMARY)
    return "{{<Signal> name:{0}, object:{1}}}".format(name_summary, object_summary)


@print_trace_dec
def Callable_SummaryProvider(valobj: SBValue, internal_dict):
    # If `method` is blank, and `custom` is not a null pointer, then it's a CallableCustom
    method: SBValue = valobj.GetChildMemberWithName("method")  # StringName
    method_name: str = method.GetSummary()
    if method_name == NULL_SUMMARY or method_name == EMPTY_SUMMARY:
        custom: SBValue = valobj.GetChildMemberWithName("custom")
        if custom.GetValueAsUnsigned() != 0:
            # TODO: Avoiding infinite recursion here by not calling GenericShortSummary
            custom_type: SBType = custom.GetType()
            if not custom_type.IsValid():
                return "{{<CallableCustom> {0}}}".format(INVALID_SUMMARY)
            return "{{<CallableCustom> {0}:{{...}}}}".format(custom_type.GetPointeeType().GetDisplayTypeName())
            # return "CallableCustom: " + GenericShortSummary(custom, internal_dict)
        else:
            # get the object
            obj_id: SBValue = valobj.GetChildMemberWithName("object")
            obj_id_val = obj_id.GetValueAsUnsigned()
            if obj_id_val == 0:
                return "{<Callable> " + NULL_SUMMARY + "}"
            return "{{<Callable> object:{0}, method:{1}}}".format(obj_id_val, method_name)


@print_trace_dec
def Vector2_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
    )


@print_trace_dec
def Vector3_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
    )


@print_trace_dec
def Vector4_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2}, {3})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
        GetFloat(valobj.GetChildMemberWithName("w")),
    )


@print_trace_dec
def Vector2i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
    )


@print_trace_dec
def Vector3i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
        valobj.GetChildMemberWithName("z").GetValueAsSigned(),
    )


@print_trace_dec
def Vector4i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2}, {3})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
        valobj.GetChildMemberWithName("z").GetValueAsSigned(),
        valobj.GetChildMemberWithName("w").GetValueAsSigned(),
    )


@print_trace_dec
def Rect2_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: ({0}, {1}), size: ({2}, {3})}}".format(
        GetFloat(valobj.GetChildMemberWithName("position").GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("position").GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("size").GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("size").GetChildMemberWithName("y")),
    )


@print_trace_dec
def Rect2i_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: ({0}, {1}), size: ({2}, {3})}}".format(
        valobj.GetChildMemberWithName("position").GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("position").GetChildMemberWithName("y").GetValueAsSigned(),
        valobj.GetChildMemberWithName("size").GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("size").GetChildMemberWithName("y").GetValueAsSigned(),
    )


def ValCheck(val: SBValue) -> SBValue:
    if not val:
        raise Exception("SBValue is None")
    error = val.GetError()
    if error.Fail() or not val.IsValid():
        fmt_err = f"{val.GetName()}: " if val.GetName() else ""
        if error.Fail():
            raise Exception(fmt_err + error.GetCString())
        else:
            raise Exception(fmt_err + "SBValue is not valid")
    return val


def ConstructNamedColorTable(global_named_colors_table: SBValue) -> dict[str, str]:
    table: dict[str, str] = dict[str, str]()
    try:
        for i in range(global_named_colors_table.GetNumChildren()):
            named_color = ValCheck(global_named_colors_table.GetChildAtIndex(i))
            name_val = ValCheck(named_color.GetChildMemberWithName("name"))
            name_val_summary = name_val.GetSummary()
            if not name_val_summary:  # nullptr at the end of the array
                break
            name = strip_quotes(name_val_summary)
            color = ValCheck(named_color.GetChildMemberWithName("color"))
            hex_str = GetHexColor(*GetColorVals(color))
            table[hex_str] = name
    except Exception as e:
        print_verbose(f"EXCEPTION ConstructNamedColorTable: " + str(e))
        return dict[str, str]()
    return table


constructed_the_table = False
hex_color_to_name: dict[str, str] = {}


def TryConstructNamedColorTable(target: SBTarget) -> None:
    global constructed_the_table
    if not constructed_the_table:
        global hex_color_to_name
        named_colors = target.FindFirstGlobalVariable("named_colors")
        if not named_colors or not named_colors.IsValid() or named_colors.GetNumChildren() == 0:
            return  # return without setting constructed_the_table; we might not be in the right context to do this
        hex_color_to_name = ConstructNamedColorTable(named_colors)
        constructed_the_table = True
        # print_trace(str(hex_color_to_name))


def GetColorAlias(valobj: SBValue, vals: Optional[tuple[float, float, float, float]] = None) -> str:
    r, g, b, a = vals if vals else GetColorVals(valobj)
    hex_str = GetHexColor(r, g, b, a)
    TryConstructNamedColorTable(valobj.target)
    if hex_str in hex_color_to_name:
        hex_str = hex_color_to_name[hex_str]
    return hex_str


def GetHexColor(r, g, b, a) -> str:
    def _get_hex(val: float):
        new_val = max(min(round(val * 255), 255), 0)
        return "{:02x}".format(new_val)

    r_hex, g_hex, b_hex, a_hex = _get_hex(r), _get_hex(g), _get_hex(b), _get_hex(a)
    return "#{0}{1}{2}{3}".format(r_hex, g_hex, b_hex, a_hex)


def GetColorVals(valobj: SBValue):
    return (
        GetFloat(valobj.GetChildMemberWithName("r")),
        GetFloat(valobj.GetChildMemberWithName("g")),
        GetFloat(valobj.GetChildMemberWithName("b")),
        GetFloat(valobj.GetChildMemberWithName("a")),
    )


@print_trace_dec
def Color_SummaryProvider(valobj: SBValue, internal_dict):
    r, g, b, a = GetColorVals(valobj)
    if not Opts.NAMED_COLOR_ANNOTATION:
        hex_str = GetHexColor(r, g, b, a)
    else:
        hex_str = GetColorAlias(valobj, (r, g, b, a))
    return "{{<{0}> r:{1:.3f}, g:{2:.3f}, b:{3:.3f}, a:{4:.3f}}}".format(hex_str, r, g, b, a)


@print_trace_dec
def Plane_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{normal: {0}, d: {1}}}".format(
        valobj.GetChildMemberWithName("normal").GetSummary(),
        valobj.GetChildMemberWithName("d").GetValueAsSigned(),
    )


@print_trace_dec
def AABB_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: {{{0}}}, size: {{{1}}}}}".format(
        valobj.GetChildMemberWithName("position").GetSummary(),
        valobj.GetChildMemberWithName("size").GetSummary(),
    )


@print_trace_dec
def Transform2D_SummaryProvider(valobj: SBValue, internal_dict):
    # transform2d has a Vector2 `origin`, Vector2 `x`, and Vector2 `y`
    x_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(0)
    y_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(1)
    o_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(2)
    return "{{x: {0}, y: {1}, o: {2}}}".format(x_row.GetSummary(), y_row.GetSummary(), o_row.GetSummary())


@print_trace_dec
def Transform3D_SummaryProvider(valobj: SBValue, internal_dict):
    # transform3d has a Basis `basis` and Vector3 `origin`
    return "{{basis: {0}, origin: {1}}}".format(
        valobj.GetChildMemberWithName("basis").GetSummary(),
        valobj.GetChildMemberWithName("origin").GetSummary(),
    )


@print_trace_dec
def Projection_SummaryProvider(valobj: SBValue, internal_dict):
    # projection has 	`Vector4 columns[4]`
    return "{{columns: {{{0}, {1}, {2}, {3}}}}}".format(
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(0).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(1).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(2).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(3).GetSummary(),
    )


@print_trace_dec
def Basis_SummaryProvider(valobj: SBValue, internal_dict):
    # basis has a Vector3[3] `rows` (NOT `elements`)
    # need to translate into (xx, xy, xy), (yx, yy, yz), (zx, zy, zz)
    x_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(0)
    y_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(1)
    z_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(2)
    return "{{{0}, {1}, {2}}}".format(x_row.GetSummary(), y_row.GetSummary(), z_row.GetSummary())


@print_trace_dec
def RID_SummaryProvider(valobj: SBValue, internal_dict):
    return "<RID=" + str(valobj.GetChildMemberWithName("_id").GetValueAsUnsigned()) + ">"


@print_trace_dec
def String_SummaryProvider(valobj: SBValue, internal_dict):
    _cowdata: SBValue = valobj.GetChildMemberWithName("_cowdata")
    size = _get_cowdata_size(_cowdata)
    if size is None:
        # check if this is a pointer to a pointer
        type = valobj.GetType()
        if type.IsPointerType() and type.GetPointeeType().IsPointerType():
            return "{...}"
        return INVALID_SUMMARY
    if size == 0:
        return EMPTY_SUMMARY

    # While cowdata has been promoted to 64-bits, this is still the limit for strings
    if STRINGS_STILL_32_BIT and size > INT32_MAX:
        return INVALID_SUMMARY
    _ptr: SBValue = _cowdata.GetChildMemberWithName("_ptr")
    _ptr.format = eFormatUnicode32
    if Opts.SANITIZE_STRING_SUMMARY:
        ret = _ptr.GetSummary()
        if ret is None:
            print_trace("String_SummaryProvider: _ptr.GetSummary() returned None")
            return EMPTY_SUMMARY
        if ret.startswith('U"'):
            ret = '"' + ret.removeprefix('U"')
        return ret
    data = _ptr.GetPointeeData(0, size)
    error: SBError = SBError()
    arr: bytearray = bytearray()
    for i in range(data.size):
        var = data.GetUnsignedInt8(error, i)
        arr.append(var)
    starr = arr.decode("utf-32LE")
    if starr.endswith("\x00"):
        starr = starr[:-1]
    return '"{0}"'.format(starr)


def is_basic_printable_type(type: SBType):
    if type.GetTypeClass() == eTypeClassEnumeration:
        return True

    basic_type = type.GetCanonicalType().GetBasicType()
    if basic_type == eBasicTypeVoid:
        return False
    if basic_type == eBasicTypeInvalid:
        return False
    if basic_type == eBasicTypeObjCID:
        return False
    if basic_type == eBasicTypeObjCClass:
        return False
    if basic_type == eBasicTypeObjCSel:
        return False
    return True


NON_RECURSIVE = [
    "String",
    "Vector2",
    "Vector2i",
    "Rect2",
    "Rect2i",
    "Vector3",
    "Vector3i",
    "Transform2D",
    "Vector4",
    "Vector4i",
    "Plane",
    "Quaternion",
    "AABB",
    "Basis",
    "Transform3D",
    "Projection",
    "Color",
    "StringName",
    "NodePath",
    "RID",
    # "Callable",
    "Signal",
    "ObjectID",
]


def is_basic_string_type(type: SBType):
    # check to see if it's a const char*, const wchar_t*, const char16_t*, const char32_t*
    if not type.IsPointerType():
        return False
    if not "const" in type.name:
        return False
    basic_type = type.GetCanonicalType().GetBasicType()
    if basic_type == eBasicTypeChar:
        return True
    if basic_type == eBasicTypeWChar:
        return True
    if basic_type == eBasicTypeChar16:
        return True
    if basic_type == eBasicTypeChar32:
        return True
    return False


@print_trace_dec
def is_string_type(type: SBType):
    if type is None:
        return False
    type_class = type.GetTypeClass()
    if type_class == eTypeClassClass or type_class == eTypeClassPointer:
        _class_type = type
        if type_class == eTypeClassPointer:
            _class_type = type.GetPointeeType()
        type_name: str = _class_type.GetUnqualifiedType().GetDisplayTypeName()
        if type_name == "String":
            return True
        elif type_name == "StringName":
            return True
        elif type_name == "StringBuffer":
            return True
        elif type_name == "NodePath":
            return True
    elif is_basic_string_type(type):
        return True

    return False


def is_basic_integer_type(type: SBType):
    if type is None:
        return False
    if type.GetTypeClass() == eTypeClassEnumeration:
        return True
    basic_type = type.GetCanonicalType().GetBasicType()
    if basic_type == eBasicTypeChar:
        return True
    if basic_type == eBasicTypeSignedChar:
        return True
    if basic_type == eBasicTypeUnsignedChar:
        return True
    if basic_type == eBasicTypeWChar:
        return True
    if basic_type == eBasicTypeSignedWChar:
        return True
    if basic_type == eBasicTypeUnsignedWChar:
        return True
    if basic_type == eBasicTypeChar16:
        return True
    if basic_type == eBasicTypeChar32:
        return True
    if basic_type == eBasicTypeChar8:
        return True
    if basic_type == eBasicTypeShort:
        return True
    if basic_type == eBasicTypeUnsignedShort:
        return True
    if basic_type == eBasicTypeInt:
        return True
    if basic_type == eBasicTypeUnsignedInt:
        return True
    if basic_type == eBasicTypeLong:
        return True
    if basic_type == eBasicTypeUnsignedLong:
        return True
    if basic_type == eBasicTypeLongLong:
        return True
    if basic_type == eBasicTypeUnsignedLongLong:
        return True
    if basic_type == eBasicTypeInt128:
        return True
    if basic_type == eBasicTypeUnsignedInt128:
        return True
    if basic_type == eBasicTypeBool:
        return True

    return False


def get_enum_string(valobj: SBValue) -> str:
    type: SBType = valobj.GetType()
    enumMembers: SBTypeEnumMemberList = type.GetEnumMembers()
    starting_value = valobj.GetValueAsUnsigned()
    if enumMembers.IsValid() and enumMembers.GetSize() > 0:
        member: SBTypeEnumMember
        member_names: list[str] = []
        member_values: list[int] = []
        for member in enumMembers:
            member_names.append(member.name)
            member_values.append(member.unsigned)
        if member_values.count(starting_value) == 0:
            # this is probably a flag
            flag_summary = ""
            remaining_value = starting_value
            for i, member_value in enumerate(member_values):
                if member_value & remaining_value:
                    if flag_summary != "":
                        flag_summary += " | "
                    flag_summary += member_names[i]
                    # remove the flag from the start_value
                    remaining_value &= ~member_value
            if remaining_value != 0:
                if remaining_value != starting_value:
                    flag_summary += " | "
                flag_summary += "0x" + format(remaining_value, "x")
            # flag_summary += " (" + str(starting_value) + ")"
            return flag_summary
        else:
            # get the index of the value
            name = member_names[member_values.index(starting_value)]
            return name  # + " (" + str(starting_value) + ")"
    return "<Invalid Enum> (" + str(starting_value) + ")"


def get_basic_printable_string(valobj: SBValue) -> str:
    type: SBType = valobj.GetType()
    if type.GetTypeClass() == eTypeClassEnumeration:
        return get_enum_string(valobj)
    # char_pointer_type: SBType = valobj.target.GetBasicType(eBasicTypeChar).GetPointerType()

    basic_type = type.GetCanonicalType().GetBasicType()
    if basic_type == eBasicTypeInvalid:
        return INVALID_SUMMARY
    if basic_type == eBasicTypeVoid:
        return "<void>"
    if basic_type == eBasicTypeObjCID:
        return str(valobj.GetSummary())
    if basic_type == eBasicTypeObjCClass:
        return str(valobj.GetSummary())
    if basic_type == eBasicTypeObjCSel:
        return str(valobj.GetSummary())
    if basic_type == eBasicTypeNullPtr:
        return NULL_SUMMARY
    if basic_type == eBasicTypeChar:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeSignedChar:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedChar:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeWChar:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeSignedWChar:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedWChar:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeChar16:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeChar32:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeChar8:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeShort:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedShort:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeInt:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedInt:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeLong:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedLong:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeLongLong:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedLongLong:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeInt128:
        return str(valobj.GetValueAsSigned())
    if basic_type == eBasicTypeUnsignedInt128:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeBool:
        return str(valobj.GetValueAsUnsigned())
    if basic_type == eBasicTypeHalf:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeFloat:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeDouble:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeLongDouble:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeFloatComplex:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeDoubleComplex:
        return GetFloatStr(valobj)
    if basic_type == eBasicTypeLongDoubleComplex:
        return GetFloatStr(valobj)
    return INVALID_SUMMARY


def is_valid_pointer(ptr: SBValue) -> bool:
    if not ptr:
        print_trace("is_valid_pointer(): ptr is None")
        return False
    if not ptr.IsValid():
        print_trace("is_valid_pointer(): ptr is not valid SBValue")
        return False
    if not ptr.GetType().IsPointerType():
        print_trace("is_valid_pointer(): ptr is not a pointer")
        return False
    if ptr.GetValueAsUnsigned() == 0:
        print_trace("is_valid_pointer(): ptr = nullptr")
        return False
    if not ptr.Dereference().IsValid():
        print_trace("is_valid_pointer(): ptr dereference is not valid")
        return False
    return True


def pointer_exists_and_is_null(ptr: SBValue) -> bool:
    if ptr is None or not ptr.IsValid():
        return False
    if not ptr.GetType().IsPointerType():
        return False
    if ptr.GetValueAsUnsigned() == 0:
        return True
    return False


# Cowdata size is located at the cowdata address - 8 bytes (sizeof(uint64_t))
def get_exception_trace(e: Exception, before_exception_limit=5, _this_call_depth=2) -> str:
    stack_prefix = "Traceback (most recent call last):\n"
    exception_trace = traceback.format_exception(type(e), e, e.__traceback__)
    stack_trace_str = "".join(exception_trace[1:]).replace("\\n", "\n")
    if before_exception_limit > 0:
        before_exc_stack_trace = traceback.format_stack(limit=(before_exception_limit + 2))
        stack_trace_str = (
            "".join(before_exc_stack_trace[:-_this_call_depth]).replace("\\n", "\n") + "Handled:\n" + stack_trace_str
        )
    return stack_prefix + stack_trace_str


def print_exception_trace(e: Exception, before_exception_limit=5) -> None:
    print(get_exception_trace(e, before_exception_limit, 3))


@print_trace_dec
def _get_cowdata_size(_cowdata: SBValue, null_means_zero=True) -> Optional[int]:
    # global cow_err_str
    size = 0
    if not _cowdata or not _cowdata.IsValid():
        print_trace("COWDATASIZE Invalid: _cowdata is not valid")
        stack_fmt = traceback.format_stack()
        print_trace("".join(stack_fmt[:-1]).replace("\\n", "\n"))
        return None
    try:
        _ptr: SBValue = _cowdata.GetChildMemberWithName("_ptr")
        if null_means_zero and pointer_exists_and_is_null(_ptr):
            return 0
        if not is_valid_pointer(_ptr):
            print_trace("COWDATASIZE Invalid: _ptr is not valid")
            return None
        _cowdata_template_type: SBType = _cowdata.GetType().GetTemplateArgumentType(0)
        if not _cowdata_template_type.IsValid():
            print_trace("COWDATASIZE Invalid: _cowdata template type is not valid")
            return None
        uint64_type: SBType = _cowdata.GetTarget().GetBasicType(eBasicTypeUnsignedLongLong)
        ptr_addr_val = _ptr.GetValueAsUnsigned()
        if ptr_addr_val - 8 < 0:
            print_trace("COWDATASIZE Invalid: ptr_addr_val - 8 is less than 0: " + str(ptr_addr_val))
            return None
        size_child: SBValue = _ptr.CreateValueFromAddress("size", ptr_addr_val - 8, uint64_type)
        if not size_child.IsValid():
            print_trace("COWDATASIZE Invalid: Size value at ptr_addr - 8 is not valid")
            return None
        size = size_child.GetValueAsSigned()
        if size < 0:
            print_trace("COWDATASIZE Invalid: Size is less than 0: " + str(size))
            return None
        if size > 0:
            item_size = _ptr.GetType().GetByteSize()
            last_val = _ptr.CreateValueFromAddress(
                "_tmp_tail",
                ptr_addr_val + ((size - 1) * item_size),
                _ptr.GetType().GetPointeeType(),
            )
            if not last_val.IsValid():
                print_trace("COWDATASIZE Invalid: Last value is not valid: " + str(last_val))
                return None
    except Exception as e:
        print_verbose("COWDATASIZE Exception: " + str(e))
        print_trace(get_exception_trace(e))
        return None

    return size


def is_cowdata_valid(_cowdata: SBValue) -> bool:
    size = _get_cowdata_size(_cowdata)
    if size is None:
        return False
    return True


def get_cowdata_size(_cowdata: SBValue) -> int:
    size = _get_cowdata_size(_cowdata)
    if size is None:
        return 0
    return size


@print_trace_dec
def GenericShortSummary(
    valobj: SBValue,
    internal_dict,
    summary_length=0,
    skip_base_class=False,
    no_children=False,
    depth=0,
) -> str:
    if not valobj or not valobj.IsValid():
        return INVALID_SUMMARY
    depth += 1
    START_SUMMARY_LENGTH = summary_length
    is_child = summary_length != 0
    MAX_LEN = Opts.SUMMARY_STRING_MAX_LENGTH - (20 if is_child else 0)
    if summary_length > Opts.SUMMARY_STRING_MAX_LENGTH or depth > MAX_DEPTH:
        # bail out
        return "{...}"
    type: SBType = valobj.GetType()
    if is_basic_printable_type(type):
        return get_basic_printable_string(valobj)

    if type.IsPointerType():
        type = type.GetPointeeType()
    unqual_type_name = str(type.GetUnqualifiedType().GetDisplayTypeName())
    if unqual_type_name == "Object" or unqual_type_name == "RefCounted":  # these lead to circular references
        return "{...}"
    if unqual_type_name.startswith("Ref<"):
        reference: SBValue = valobj.GetChildMemberWithName("reference")
        if not reference.IsValid():
            return "{" + INVALID_SUMMARY + "}"
        if reference.GetValueAsUnsigned() == 0:
            return "{" + NULL_SUMMARY + "}"
        deref: SBValue = reference.Dereference()
        if not deref.IsValid():
            return "{" + INVALID_SUMMARY + "}"
        prefix = "{[" + str(deref.GetDisplayTypeName()) + "]:"
        summary = GenericShortSummary(
            deref,
            internal_dict,
            START_SUMMARY_LENGTH + len(prefix),
            True,
            no_children,
            depth,
        )
        return prefix + summary + "}"
    summ = None
    if valobj.GetTypeSynthetic():  # Synthetic types will call this function again and could lead to infinite recursion.
        if unqual_type_name == "Variant":
            # Avoid putting it through the synthetic provider.
            variant_value = Variant_GetValue(valobj.GetNonSyntheticValue())
            return GenericShortSummary(
                variant_value,
                internal_dict,
                summary_length,
                skip_base_class,
                no_children,
                depth,
            )
        else:
            return "{...}"
    else:
        try:
            summ = valobj.GetSummary()
        except Exception as e:
            summ = " GetSummary() EXCEPTION: " + str(e)
            summ += " " + str(valobj.GetDisplayTypeName())
    if summ:
        return summ
    if no_children:
        return "{...}"
    base_classes: list[SBType] = type.get_bases_array()
    base_class_names = [base_class.GetName() for base_class in base_classes]
    summ_str = "{"
    try:
        num_children = valobj.GetNumChildren()
        skipped_base_class = False
        for i in range(num_children):
            child: SBValue = valobj.GetChildAtIndex(i)
            prefix = child.name + ":"
            if skip_base_class and base_class_names.count(child.name) > 0:
                skipped_base_class = True
                continue
            if is_basic_printable_type(child.GetType()):
                summ_str += prefix + get_basic_printable_string(child)
            else:
                summ_str += prefix + GenericShortSummary(
                    child,
                    internal_dict,
                    len(summ_str) + START_SUMMARY_LENGTH,
                    False,
                    no_children,
                    depth,
                )
            if len(summ_str) + START_SUMMARY_LENGTH > MAX_LEN:
                if i < len(valobj) - 1:
                    summ_str += ", ..."
                break
            if i < len(valobj) - 1:
                summ_str += ", "
        if summ_str == "{":
            summ_str += "..."
        if not summ_str.endswith(", ...") and skipped_base_class:
            summ_str += ", ..."
        summ_str += "}"
    except Exception as e:
        summ_str += " !!EXCEPTION: " + str(e)
        summ_str += " " + str(valobj.GetDisplayTypeName())
    return summ_str


@print_trace_dec
def get_offset_of_object_member(obj: SBValue, member: str) -> int:
    if not obj.IsValid():
        return -1
    # check if obj is a pointer
    if obj.GetType().IsPointerType():
        obj = obj.Dereference()
        if not obj.IsValid():
            return -1
    obj_addr: SBValue = obj.AddressOf()
    element_addr_val = obj_addr.GetValueAsUnsigned()
    member_val: SBValue = obj.GetChildMemberWithName(member)
    member_addr: SBValue = member_val.AddressOf()
    member_addr_val = member_addr.GetValueAsUnsigned()
    return member_addr_val - element_addr_val  # type: ignore


def key_value_summary(valobj: SBValue, internal_dict, key_val_style):
    key = valobj.GetChildMemberWithName("key")
    value = valobj.GetChildMemberWithName("value")
    if key_val_style:
        return GenericShortSummary(value, internal_dict)
    return "{0}: {1}".format(
        GenericShortSummary(key, internal_dict),
        GenericShortSummary(value, internal_dict),
    )


def map_element_summary(valobj: SBValue, internal_dict, data_name):
    data: SBValue = valobj.GetChildMemberWithName(data_name)
    if not data or not data.IsValid():
        return None
    key = data.GetChildMemberWithName("key")
    style = should_use_key_val_style(key.GetType() if not_null_check(key) else None)
    return key_value_summary(data, internal_dict, style)


def KeyValue_SummaryProvider(valobj: SBValue, internal_dict):
    return key_value_summary(valobj, internal_dict, False)


def HashMapElement_SummaryProvider(valobj: SBValue, internal_dict):
    return map_element_summary(valobj, internal_dict, "data")


def RBMapElement_SummaryProvider(valobj: SBValue, internal_dict):
    return map_element_summary(valobj, internal_dict, "_data")


# Disabled for now, causing crashes
class HashMapElement_SyntheticProvider(GodotSynthProvider):
    key_val_element_style: bool = Opts.MAP_KEY_VAL_STYLE

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)
        # self.update()

    @print_trace_dec
    def update(self):
        pass

    @print_trace_dec
    def check_valid(self, valobj: SBValue) -> bool:
        if not valobj or not valobj.IsValid():
            return False
        return True

    @print_trace_dec
    def get_index_of_child(self, name):
        if name == "[key]" or name == "key":
            return 0
        elif name == "[value]" or name == "value":
            return 1
        return None

    @print_trace_dec
    def get_data(self) -> SBValue:
        if not self.check_valid(self.valobj):
            return None
        return self.valobj.GetChildMemberWithName("data")

    @print_trace_dec
    def get_key(self) -> SBValue:
        data: SBValue = self.get_data()
        if not data or not data.IsValid():
            return None
        key = data.GetChildMemberWithName("key")
        type = key.GetType()
        return self.valobj.CreateValueFromData("[key]", key.GetData(), type)

    @print_trace_dec
    def get_value(self) -> SBValue:
        data: SBValue = self.get_data()
        if not data or not data.IsValid():
            return None
        value = data.GetChildMemberWithName("value")
        type = value.GetType()
        return self.valobj.CreateValueFromData("[value]", value.GetData(), type)

    @print_trace_dec
    def get_child_at_index(self, index):
        if index < 0 or index > 1:
            return None
        if index == 0:
            return self.get_key()
        else:
            return self.get_value()
        # return self.valobj

    @print_trace_dec
    def num_children(self, max=UINT32_MAX):
        return 2

    @print_trace_dec
    def has_children(self):
        return True

    @print_trace_dec
    def get_summary(self):
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        value_summary = GenericShortSummary(self.value, self.internal_dict)
        if hasattr(self, "is_summary") and self.key_val_element_style:  # only show the value for the summary
            return value_summary
        key_summary = GenericShortSummary(self.key, self.internal_dict)
        return "[{0}]: {1}".format(key_summary, value_summary)


class RBMapElement_SyntheticProvider(HashMapElement_SyntheticProvider):

    @print_trace_dec
    def get_data(self):
        return self.valobj.GetChildMemberWithName("_data")


class _ListOfChildren_SyntheticProvider(GodotSynthProvider):

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        self.type: SBType = valobj.GetType()
        self.typename: str = self.type.GetUnqualifiedType().GetDisplayTypeName()
        self.no_cache = NO_CACHE_MEMBERS
        self.cache_min = CACHE_MIN if not is_summary else Opts.MAX_AMOUNT_OF_CHILDREN_IN_SUMMARY
        self.cache_fetch_max = CACHE_FETCH_MAX
        self._cached_size = 0
        super().__init__(valobj, internal_dict, is_summary)
        self.update()

    def update(self):
        """
        Override this method to set any state that would normally be set in the constructor
        Note: This MUST update self.num_elements
        """
        raise Exception("Not implemented")

    def get_len(self, obj: SBValue) -> int:
        """
        Override this method to return the non-cached number of elements in this vector-like object
        """
        raise Exception("Not implemented")

    def get_ptr(self, obj: SBValue) -> SBValue:
        """
        Override this method to return the ptr to the first element; in arrays, this would just be the array pointer, in linked lists, this would be the head
        """
        raise Exception("Not implemented")

    def _create_child_at_element_index(self, index) -> SBValue:
        """
        Override this method to return the synthetic child at the given index
        @param index: The index of the child to create
        """
        raise Exception("Not implemented")

    def _get_child_summary(self, real_index) -> str:
        """
        Override this method if you want to provide a custom summary for the child at the given index
        """
        element: SBValue = self._create_child_at_element_index(real_index)
        return GenericShortSummary(element, self.internal_dict, 0, False, True)

    # def get_size_synthetic_child(self):
    #     return self.valobj.CreateValueFromData("[size]", SBData.CreateDataFromInt(self.num_elements), self.valobj.target.GetBasicType(eBasicTypeUnsignedInt))

    @property
    def num_elements(self) -> int:
        return self._cached_size

    @num_elements.setter
    def num_elements(self, value: int):
        self._cached_size = value

    @print_trace_dec
    def get_children_summary(self, max_children=Opts.MAX_AMOUNT_OF_CHILDREN_IN_SUMMARY) -> str:
        if self.num_elements == 0:
            return ""
        max_children = min(Opts.MAX_AMOUNT_OF_CHILDREN_IN_SUMMARY, self.num_elements)
        i: int = 0
        summ_str = ""
        for i in range(max_children):
            summ_str += self._get_child_summary(i)
            if len(summ_str) > Opts.SUMMARY_STRING_MAX_LENGTH:
                break
            if max_children != 1 and i < max_children - 1:
                summ_str += ", "
        if self.num_elements > i + 1:
            summ_str += ", ..."
        return summ_str

    @print_trace_dec
    def get_child_at_index(self, idx) -> SBValue:
        return self._create_child_at_element_index(idx)

    @print_trace_dec
    def num_children(self, max=UINT32_MAX) -> int:
        return self.num_elements

    @print_trace_dec
    def has_children(self) -> bool:
        return self.num_elements > 0

    @print_trace_dec
    def get_index_of_child(self, name: str) -> Optional[int]:
        try:
            return int(name.lstrip("[").rstrip("]"))
        except:
            return None

    @print_trace_dec
    def get_summary(self) -> str:
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        return LIST_FORMAT.format(
            type_name=self.typename,
            type_no_template=self.typename.split("<")[0],
            size=self.num_elements,
            children=self.get_children_summary(),
        )


class PagedArray_SyntheticProvider(_ListOfChildren_SyntheticProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        self.item_type: SBType
        self.item_size: int
        self.ptr: SBValue
        super().__init__(valobj, internal_dict, is_summary)

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("page_data")

    def get_len(self, obj: SBValue):
        return obj.GetChildMemberWithName("count").GetValueAsUnsigned(0)

    def check_valid(self, obj: SBValue):
        page_data = self.get_ptr(obj)
        size = self.get_len(obj)

        if size == 0 and page_data and page_data.TypeIsPointerType():
            return True
        if not is_valid_pointer(page_data):
            return False
        page_pool = obj.GetChildMemberWithName("page_pool")
        if not is_valid_pointer(page_pool):
            return False
        pages_allocated = page_pool.GetChildMemberWithName("pages_allocated").GetValueAsUnsigned(0)
        pages_available = page_pool.GetChildMemberWithName("pages_available").GetValueAsUnsigned(0)
        if pages_allocated < pages_available:
            return False
        try:  # try getting the last element
            index = size - 1
            page_size_shift: int = obj.GetChildMemberWithName("page_size_shift").GetValueAsUnsigned(0)
            page_size_mask: int = obj.GetChildMemberWithName("page_size_mask").GetValueAsUnsigned(0)
            page_index = index >> page_size_shift
            offset = index & page_size_mask
            if page_index > UINT32_MAX or offset > UINT32_MAX:  # PagedArray can't be bigger than this
                return False
            if page_index > pages_allocated:
                return False
            array_type = page_data.GetType().GetPointeeType().GetArrayType(size).GetPointerType()
            ptr_cast = page_data.Cast(array_type)
            last_page = ptr_cast.GetChildAtIndex(page_index)
            if not last_page or not last_page.IsValid():
                return False
            last_val: SBValue = last_page.GetChildAtIndex(offset, eDynamicCanRunTarget, True)
            if not last_val or not last_val.IsValid():
                return False
        except Exception as e:
            print_verbose("EXCEPTION: " + str(e))
            return False
        return True

    def update(self) -> None:
        """
        Updates num_elements and ptr
        """
        self.num_elements = self.get_len(self.valobj)
        self.ptr = self.get_ptr(self.valobj)
        if not self.check_valid(self.valobj):
            self.num_elements = 0
            self.ptr = None
            return
        self.item_type = self.ptr.GetType().GetPointeeType().GetPointeeType() if self.ptr else None
        self.item_size = self.item_type.GetByteSize() if self.item_type else 0
        self.page_size_shift: int = self.valobj.GetChildMemberWithName("page_size_shift").GetValueAsUnsigned(0)
        self.page_size_mask: int = self.valobj.GetChildMemberWithName("page_size_mask").GetValueAsUnsigned(0)
        pointer_to_array_type = self.ptr.GetType().GetPointeeType().GetArrayType(self.num_elements).GetPointerType()
        self.ptr_cast = self.ptr.Cast(pointer_to_array_type)

    def _create_child_at_element_index(self, index) -> SBValue:
        name = "[" + str(index) + "]"
        return self.create_child_at_real_index(index, name)

    def create_child_at_real_index(self, index, name) -> Optional[SBValue]:
        if index < 0 or index >= self.num_elements or not self.ptr:
            return None
        page_index = index >> self.page_size_shift
        offset = index & self.page_size_mask
        page_data: SBValue = self.ptr_cast.GetChildAtIndex(page_index)
        child = page_data.CreateChildAtOffset(name, offset * self.item_size, self.item_type)
        return child


class _ArrayLike_SyntheticProvider(_ListOfChildren_SyntheticProvider):

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        self.item_type: SBType
        self.item_size: int
        self.ptr: SBValue
        super().__init__(valobj, internal_dict, is_summary)

    @print_trace_dec
    def check_valid(self, obj: SBValue):
        num_elements = self.get_len(obj)
        ptr: SBValue = self.get_ptr(obj)
        item_type: SBType = ptr.GetType().GetPointeeType() if ptr else None
        item_size: int = item_type.GetByteSize() if item_type else 0
        if not ptr:
            return False
        if num_elements == 0:
            return True
        if not is_valid_pointer(ptr):
            return False
        try:
            ptr_address = ptr.GetValueAsUnsigned()
            if ptr_address == 0:
                return False
            last_val = ptr.CreateValueFromAddress(
                "_tmp_tail", ptr_address + ((num_elements - 1) * item_size), item_type
            )
            if not last_val.IsValid():
                return False
        except Exception as e:
            print_verbose("EXCEPTION: " + str(e))
            return False
        return True

    @print_trace_dec
    def update(self) -> None:
        """
        Updates num_elements and ptr
        """
        self.num_elements = self.get_len(self.valobj)
        self.ptr = self.get_ptr(self.valobj)
        self.item_type = self.ptr.GetType().GetPointeeType() if not_null_check(self.ptr) else None
        self.item_size = self.item_type.GetByteSize() if self.item_type else 0
        if not self.check_valid(self.valobj):
            self.num_elements = 0
            self.ptr = None

    @print_trace_dec
    def _create_child_at_element_index(self, index) -> SBValue:
        name = "[" + str(index) + "]"
        return self.create_child_at_real_index(index, name)

    # Helper function for proxy providers.
    @print_trace_dec
    def create_child_at_real_index(self, index, name):
        if index < 0 or index >= self.num_elements or not self.ptr:
            return None
        try:
            ptr_address = self.ptr.GetValueAsUnsigned()
            if ptr_address == 0:
                return None
            return self.ptr.CreateValueFromAddress(name, ptr_address + (index * self.item_size), self.item_type)
        except:
            return None


class Vector_SyntheticProvider(_ArrayLike_SyntheticProvider):

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("_cowdata").GetChildMemberWithName("_ptr")

    def get_len(self, obj: SBValue):
        return get_cowdata_size(obj.GetChildMemberWithName("_cowdata"))


class LocalVector_SyntheticProvider(_ArrayLike_SyntheticProvider):
    def check_valid(self, obj: SBValue):
        if not super().check_valid(obj):
            return False
        length = self.get_len(obj)
        if length == 0:
            return True
        capacity = obj.GetChildMemberWithName("capacity").GetValueAsUnsigned(0)
        if capacity < length:
            return False
        return True

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("data")

    def get_len(self, obj: SBValue):
        return obj.GetChildMemberWithName("count").GetValueAsUnsigned(0)


class HashSet_SyntheticProvider(_ArrayLike_SyntheticProvider):
    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("keys")

    def get_len(self, obj: SBValue):
        return obj.GetChildMemberWithName("num_elements").GetValueAsUnsigned(0)


def _VMap_Pair_get_keypair_summaries(valobj: SBValue, internal_dict, is_VMap_Summary=False) -> tuple[str, str]:
    key: SBValue = valobj.GetChildMemberWithName("key")
    value: SBValue = valobj.GetChildMemberWithName("value")
    key_summary = GenericShortSummary(key, internal_dict, 0, False, is_VMap_Summary)
    value_summary = GenericShortSummary(value, internal_dict, 0, False, is_VMap_Summary)
    return key_summary, value_summary


def VMap_Pair_SummaryProvider(valobj: SBValue, internal_dict):
    fmt_str = "[{0}]: {1}"
    key: SBValue = valobj.GetChildMemberWithName("key")
    key_template_type: SBType = key.GetType() if key else None
    if should_use_key_val_style(key_template_type):
        value: SBValue = valobj.GetChildMemberWithName("value")
        return GenericShortSummary(value, internal_dict)
    return fmt_str.format(*_VMap_Pair_get_keypair_summaries(valobj, internal_dict))


@print_trace_dec
def should_use_key_val_style(key_template_type) -> bool:
    return (
        Opts.MAP_KEY_VAL_STYLE
        and key_template_type is not None
        and (is_string_type(key_template_type) or is_basic_integer_type(key_template_type))
    )


class VMap_SyntheticProvider(_ArrayLike_SyntheticProvider):
    key_val_element_style: bool = Opts.MAP_KEY_VAL_STYLE

    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)

    def update(self) -> None:
        super().update()
        if self.num_elements == 0:
            return
        self.key_template_type: SBType = self.valobj.GetType().GetTemplateArgumentType(0) if self.valobj else None
        self.key_val_element_style = should_use_key_val_style(self.key_template_type)
        pointer_to_array_type = self.ptr.GetType().GetPointeeType().GetArrayType(self.num_elements).GetPointerType()
        self.ptr_cast = self.ptr.Cast(pointer_to_array_type)
        self.cached_key_summaries = list[str]()
        self.cached_key_to_idx_map = dict[str, int]()
        self.cache_elements(self.cache_min)

    def get_len(self, obj: SBValue):
        return get_cowdata_size(obj.GetChildMemberWithName("_cowdata"))

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("_cowdata").GetChildMemberWithName("_ptr")

    def cache_elements(self, size: int):
        if size > self.num_elements:
            size = self.num_elements
        if len(self.cached_key_summaries) >= size or size == 0:
            return
        start = len(self.cached_key_summaries)
        for i in range(start, size):
            child = self.ptr_cast.GetChildAtIndex(i, eDynamicCanRunTarget, True)
            if not child.IsValid():
                continue
            # get the key summary
            key: SBValue = child.GetChildMemberWithName("key")
            key_summary = GenericShortSummary(key, self.internal_dict)
            self.cached_key_summaries.append(key_summary)
            self.cached_key_to_idx_map[key_summary] = i

    def _get_child_summary(self, index: int):
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None
        element = self._create_child_at_element_index(index)
        key, value = _VMap_Pair_get_keypair_summaries(element, self.internal_dict, True)
        if not element or not element.IsValid():
            return "INVALID"
        return "[{0}]: {1}".format(key, value)

    def get_key_by_index(self, index: int) -> Optional[str]:
        if index < 0 or index >= self.num_elements:
            return None
        if self.no_cache:
            child = self.ptr_cast.GetChildAtIndex(index, eDynamicCanRunTarget, True)
            key: SBValue = child.GetChildMemberWithName("key")
            key_summary = GenericShortSummary(key, self.internal_dict)
            return key_summary
        if index < len(self.cached_key_summaries):
            return self.cached_key_summaries[index]
        # otherwise, start caching
        while len(self.cached_key_summaries) < self.num_elements:
            new_length = len(self.cached_key_summaries) + self.cache_fetch_max
            if new_length > self.num_elements:
                new_length = self.num_elements
            self.cache_elements(new_length)
            if new_length >= index:
                break
        return self.cached_key_summaries[index]

    def _create_child_at_element_index(self, index) -> SBValue:
        key = (
            self.get_key_by_index(index)
            if hasattr(self, "key_val_element_style") and self.key_val_element_style
            else str(index)
        )
        return self.create_child_at_real_index(index, f"[{key}]")

    def get_index_of_key(self, key: str) -> Optional[int]:
        if self.no_cache:
            for i in range(self.num_elements):
                child = self.ptr_cast.GetChildAtIndex(i, eDynamicCanRunTarget, True)
                key_summary = GenericShortSummary(child.GetChildMemberWithName("key"), self.internal_dict)
                if key_summary == key:
                    return i
            return None

        if key in self.cached_key_to_idx_map:
            return self.cached_key_to_idx_map[key]
        # start caching
        while len(self.cached_key_summaries) < self.num_elements:
            new_length = len(self.cached_key_summaries) + self.cache_fetch_max
            if new_length > self.num_elements:
                new_length = self.num_elements
            self.cache_elements(new_length)
            if key in self.cached_key_to_idx_map:
                return self.cached_key_to_idx_map[key]
        return None

    def get_index_of_child(self, name: str):
        if self.key_val_element_style:
            return self.get_index_of_key(name.lstrip("[").rstrip("]"))
        else:
            return int(name.lstrip("[").rstrip("]"))


class _LinkedListLike_SyntheticProvider(_ListOfChildren_SyntheticProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        self.cached_elements: list[SBValue] = list[SBValue]()
        super().__init__(valobj, internal_dict, is_summary)

    def _create_synthetic_child(self, element: SBValue, index) -> SBValue:
        raise Exception("Not implemented")

    def get_tail(self, obj: SBValue) -> SBValue:
        raise Exception("Not implemented")

    def get_list_element_next(self, element: SBValue) -> SBValue:
        raise Exception("Not implemented")

    def get_list_element_prev(self, element: SBValue) -> SBValue:
        raise Exception("Not implemented")

    def get_list_element_data(self, element: SBValue) -> SBValue:
        raise Exception("Not implemented")

    @print_trace_dec
    def _cache_elements(self, size: int):
        if self.num_elements == 0 or size == 0:
            return
        if size > self.num_elements:
            size = self.num_elements
        start = 0
        element: SBValue
        if len(self.cached_elements) == 0:
            element = self.get_ptr(self.valobj)
            self.cached_elements.append(element)
        else:
            start = len(self.cached_elements) - 1
            if start > size:
                return
            element = self.cached_elements[start]
        for _ in range(start + 1, size):
            element = self.get_list_element_next(element)
            if element.GetValueAsUnsigned() == 0:
                break
            self.cached_elements.append(element)

    @print_trace_dec
    def check_valid(self, obj: SBValue) -> bool:
        if not not_null_check(obj):
            return False
        size = self.get_len(obj)
        if size > 0:
            # check if head_element is valid
            head_element: SBValue = self.get_ptr(obj)
            if not is_valid_pointer(head_element):
                print_trace("head_element is not valid")
                return False
            # check if head_element->prev() is nullptr (it should be if the size is > 0)
            prev: SBValue = self.get_list_element_prev(head_element)
            if not pointer_exists_and_is_null(prev):
                print_trace("head_element->prev is not nullptr")
                return False
            # check if tail_element is valid
            tail_element: SBValue = self.get_tail(obj)
            if not is_valid_pointer(tail_element):
                print_trace("tail_element is not valid")
                return False
            # check if tail_element->next() is nullptr (it should be if the size is > 0)
            next: SBValue = self.get_list_element_next(tail_element)
            if not pointer_exists_and_is_null(next):
                print_trace("tail_element->next is not nullptr")
                return False
            if size >= 2:
                # check if head_element->next() is valid
                next = self.get_list_element_next(head_element)
                if not is_valid_pointer(next):
                    print_trace("head_element->next is not valid")
                    return False
                # check if tail_element->prev() is valid
                prev = self.get_list_element_prev(self.get_tail(obj))
                if not is_valid_pointer(prev):
                    print_trace("tail_element->prev is not valid")
                    return False
        return True

    @print_trace_dec
    def update(self):
        if self.cached_elements is None:
            self.cached_elements = list[SBValue]()
        self.num_elements = self.get_len(self.valobj)
        if self.check_valid(self.valobj) == False:
            self.num_elements = 0
        self.cached_elements.clear()
        if self.no_cache or self.num_elements == 0:
            return
        self._cache_elements(self.cache_min)

    @print_trace_dec
    def _get_uncached_element_at_index(self, index) -> SBValue:
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None
        element = self.get_ptr(self.valobj)
        for _ in range(index):
            element = self.get_list_element_next(element)
        return element

    @print_trace_dec
    def _create_child_at_element_index(self, index) -> SBValue:
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None

        element: SBValue
        if self.no_cache or index >= self.cache_fetch_max:
            element = self._get_uncached_element_at_index(index)
        else:
            if index >= len(self.cached_elements):
                self._cache_elements(len(self.cached_elements) + self.cache_fetch_max)
            element = self.cached_elements[index]
        return self._create_synthetic_child(element, index)


class List_SyntheticProvider(_LinkedListLike_SyntheticProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)

    # overrides _VectorLike_SyntheticProvider
    def get_len(self, obj: SBValue):
        if not obj.IsValid():
            return 0
        _data: SBValue = obj.GetChildMemberWithName("_data")
        if not is_valid_pointer(_data):
            return 0
        size_cache: SBValue = _data.GetChildMemberWithName("size_cache")
        if not not_null_check(size_cache.IsValid()):
            return 0
        return size_cache.GetValueAsUnsigned()

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("_data").GetChildMemberWithName("first")

    def get_tail(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("_data").GetChildMemberWithName("last")

    def get_list_element_next(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("next_ptr")

    def get_list_element_prev(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("prev_ptr")

    def get_list_element_data(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("value")

    def _create_synthetic_child(self, element: SBValue, index):
        value: SBValue = element.GetChildMemberWithName("value")
        offset = get_offset_of_object_member(element, "value")
        if offset < 0:
            return None
        return element.CreateChildAtOffset("[{0}]".format(str(index)), offset, value.GetType())


def not_null_check(valobj: SBValue) -> bool:
    if not valobj or not valobj.IsValid():
        return False
    return True


class HashMap_SyntheticProvider(_LinkedListLike_SyntheticProvider):
    key_val_element_style: bool = Opts.MAP_KEY_VAL_STYLE

    @print_trace_dec
    def __init__(self, valobj: SBValue, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)

    @print_trace_dec
    def update(self) -> None:
        self.num_elements = self.get_len(self.valobj)
        is_valid = self.check_valid(self.valobj)
        if not is_valid:
            self.num_elements = 0
        if self.cached_elements is None:
            self.cached_elements = list[SBValue]()
        self.cached_elements.clear()
        self.cached_key_to_idx_map = dict[str, int]()
        self.cached_idx_to_key_map = dict[int, str]()
        self.key_val_element_style: bool = False
        self.key_template_type: SBType = None
        if self.num_elements != 0:
            self.key_template_type = self.valobj.GetType().GetTemplateArgumentType(0) if is_valid else None
            self.key_val_element_style = should_use_key_val_style(self.key_template_type)
        if not self.no_cache:
            self._cache_elements(self.cache_min)

    @print_trace_dec
    def get_len(self, obj: SBValue):
        if not not_null_check(obj):
            return 0
        return obj.GetChildMemberWithName("num_elements").GetValueAsUnsigned()

    @trace_none_if_invalid_dec
    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("head_element")

    @trace_none_if_invalid_dec
    def get_tail(self, obj: SBValue) -> SBValue:
        return obj.GetChildMemberWithName("tail_element")

    @trace_none_if_invalid_dec
    def get_list_element_next(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("next")

    @trace_none_if_invalid_dec
    def get_list_element_prev(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("prev")

    @trace_none_if_invalid_dec
    def get_list_element_data(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("data")

    @print_trace_dec
    def get_list_element_key(self, element: SBValue) -> SBValue:
        element_data = self.get_list_element_data(element)
        if not not_null_check(element_data):
            return None
        return self.get_list_element_data(element).GetChildMemberWithName("key")

    @print_trace_dec
    def get_list_element_keyvalue(self, element: SBValue) -> SBValue:
        element_data = self.get_list_element_data(element)
        if not not_null_check(element_data):
            return None
        return self.get_list_element_data(element).GetChildMemberWithName("value")

    @print_trace_dec
    def get_index_of_child(self, name: str):
        if self.key_val_element_style:
            return self.get_index_of_key(name.lstrip("[").rstrip("]"))
        else:
            return int(name.lstrip("[").rstrip("]"))

    @print_trace_dec
    def get_index_of_key(self, key: str):
        if key in self.cached_key_to_idx_map and self.cached_key_to_idx_map[key] is not None:
            return self.cached_key_to_idx_map[key]
        while len(self.cached_elements) < self.num_elements:  # type: ignore
            new_length = len(self.cached_elements) + self.cache_fetch_max
            if new_length > self.num_elements:
                new_length = self.num_elements
            self._cache_elements(new_length)
            idx = self.cached_key_to_idx_map[key]
            if idx is not None:  # type: ignore
                return idx
        return None

    @print_trace_dec
    def _get_child_summary(self, index):
        if index < 0 or index >= self.num_elements or not self.valobj or self.valobj.IsValid() == False:
            return INVALID_SUMMARY
        child = self._create_child_at_element_index(index)
        if not not_null_check(child):
            return INVALID_SUMMARY
        element = child.GetNonSyntheticValue()
        key = self.get_list_element_key(element)
        value = self.get_list_element_keyvalue(element)
        key_summary = GenericShortSummary(key, self.internal_dict)
        value_summary = GenericShortSummary(value, self.internal_dict)
        return "[{0}]: {1}".format(key_summary, value_summary)

    @print_trace_dec
    def _cache_elements(self, size: int):
        if self.num_elements == 0 or size == 0:
            return
        if size > self.num_elements:
            size = self.num_elements
        start = 0
        element: SBValue
        if self.cached_elements is None:
            self.cached_elements = list[SBValue]()
        if len(self.cached_elements) == 0:
            element = self.get_ptr(self.valobj)
            self.cached_elements.append(element)
        else:
            start = len(self.cached_elements) - 1
            if start > size:
                return
            element = self.cached_elements[start]
        if self.key_val_element_style:
            key = self.get_list_element_key(element)
            keySummary = GenericShortSummary(key, self.internal_dict, 0, False, False)
            self.cached_key_to_idx_map[keySummary] = start
            self.cached_idx_to_key_map[start] = keySummary
        for _ in range(start + 1, size):
            element = self.get_list_element_next(element)
            if not element or element.GetValueAsUnsigned() == 0:
                break
            self.cached_elements.append(element)
            if self.key_val_element_style:
                key = self.get_list_element_key(element)
                keySummary = GenericShortSummary(key, self.internal_dict, 0, False, False)
                self.cached_key_to_idx_map[keySummary] = len(self.cached_elements) - 1
                self.cached_idx_to_key_map[len(self.cached_elements) - 1] = keySummary

    @print_trace_dec
    def _create_synthetic_child(self, element: SBValue, index):
        if not element or not element.IsValid():
            return None
        if self.key_val_element_style:
            keyname = ""
            if index in self.cached_idx_to_key_map:
                keyname = self.cached_idx_to_key_map[index]
            else:
                key = self.get_list_element_key(element)
                keyname = GenericShortSummary(key, self.internal_dict, 0, False, False)
        else:
            keyname = str(index)
        if keyname not in self.cached_key_to_idx_map:
            self.cached_key_to_idx_map[keyname] = index
        if index not in self.cached_idx_to_key_map:
            self.cached_idx_to_key_map[index] = keyname
        value = element.CreateValueFromData("[" + keyname + "]", element.GetData(), element.GetType())
        return value


class RBMap_SyntheticProvider(HashMap_SyntheticProvider):
    def get_len(self, obj: SBValue):
        return obj.GetChildMemberWithName("_data").GetChildMemberWithName("size_cache").GetValueAsUnsigned(0)

    def get_ptr(self, obj: SBValue) -> SBValue:
        return obj.EvaluateExpression("front()").GetNonSyntheticValue()

    def get_tail(self, obj: SBValue) -> SBValue:
        raise Exception("Not implemented, should not be called")

    def get_list_element_next(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("_next")

    def get_list_element_prev(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("_prev")

    def get_list_element_data(self, element: SBValue) -> SBValue:
        return element.GetChildMemberWithName("_data")

    def check_valid(self, obj: SBValue) -> bool:
        size = self.get_len(obj)
        if size > 0:
            # check if head_element is valid
            head_element: SBValue = self.get_ptr(obj)
            if not is_valid_pointer(head_element):
                return False
            prev = self.get_list_element_prev(head_element)
            if not pointer_exists_and_is_null(prev):
                return False
            if size >= 2:
                # check if head_element->next() is valid
                next: SBValue = self.get_list_element_next(head_element)
                if not is_valid_pointer(next):
                    return False
        return True


class _Proxy_SyntheticProvider(GodotSynthProvider):
    def __init__(self, valobj, internal_dict, is_summary=False):
        super().__init__(valobj, internal_dict, is_summary)
        self.synth_proxy: _ListOfChildren_SyntheticProvider = None
        self.update()

    def update(self):
        """
        set the self.synth_proxy value here
        """
        raise Exception("Not implemented")

    def check_valid(self, obj: SBValue):
        return self.synth_proxy and self.synth_proxy.check_valid(self.synth_proxy.valobj)

    def get_summary(self):
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        size = self.synth_proxy.num_elements
        children_summary = self.synth_proxy.get_children_summary()
        type_name = self.valobj.GetType().GetUnqualifiedType().GetDisplayTypeName()
        return LIST_FORMAT.format(
            type_name=type_name,
            type_no_template=type_name.split("<")[0],
            size=size,
            children=children_summary,
        )

    def num_children(self, max=UINT32_MAX):
        if self.synth_proxy:
            return self.synth_proxy.num_children()
        return 0

    def has_children(self):
        if self.synth_proxy:
            return self.synth_proxy.has_children()
        return False

    def get_index_of_child(self, name: str):
        if self.synth_proxy:
            return self.synth_proxy.get_child_index(name)
        return None

    def get_child_at_index(self, index):
        if self.synth_proxy:
            return self.synth_proxy.get_child_at_index(index)
        return None


def get_synth_provider_for_object(cls, valobj: SBValue, internal_dict, is_summary) -> GodotSynthProvider:
    obj_id = valobj.GetIndexOfChildWithName("$$object-id$$")
    if obj_id in GodotSynthProvider.synth_by_id:
        return GodotSynthProvider.synth_by_id[obj_id]
    return cls(valobj.GetNonSyntheticValue(), internal_dict, is_summary)  # type: ignore


# just a proxy for Vector_SyntheticProvider
class Array_SyntheticProvider(_Proxy_SyntheticProvider):
    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        _p: SBValue = self.valobj.GetChildMemberWithName("_p")
        if is_valid_pointer(_p):
            self.synth_proxy = get_synth_provider_for_object(
                Vector_SyntheticProvider,
                _p.GetChildMemberWithName("array"),
                self.internal_dict,
                self.is_summary,
            )


class Dictionary_SyntheticProvider(_Proxy_SyntheticProvider):
    def update(self):
        self.synth_proxy: HashMap_SyntheticProvider = None
        try:
            _p: SBValue = self.valobj.GetChildMemberWithName("_p")
            if is_valid_pointer(_p):
                self.synth_proxy = get_synth_provider_for_object(
                    HashMap_SyntheticProvider,
                    _p.GetChildMemberWithName("variant_map"),
                    self.internal_dict,
                    self.is_summary,
                )
        except Exception as e:
            self.exception = e


class VSet_SyntheticProvider(_Proxy_SyntheticProvider):
    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        _data: SBValue = self.valobj.GetChildMemberWithName("_data")
        if _data.IsValid():
            self.synth_proxy = get_synth_provider_for_object(
                Vector_SyntheticProvider, _data, self.internal_dict, self.is_summary
            )


class RingBuffer_SyntheticProvider(_Proxy_SyntheticProvider):
    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        self.read_pos = 0
        self.write_pos = 0
        self.size_mask = 0
        _data: SBValue = self.valobj.GetChildMemberWithName("data")
        if _data.IsValid():
            self.synth_proxy = get_synth_provider_for_object(
                Vector_SyntheticProvider, _data, self.internal_dict, self.is_summary
            )
            self.size_mask = self.valobj.GetChildMemberWithName("size_mask").GetValueAsSigned()
            self.read_pos = self.valobj.GetChildMemberWithName("read_pos").GetValueAsSigned() & self.size_mask
            self.write_pos = self.valobj.GetChildMemberWithName("write_pos").GetValueAsSigned() & self.size_mask

    def get_summary(self):
        if not self.check_valid(self.valobj):
            return INVALID_SUMMARY
        children_summary = ""
        size = 0
        if self.synth_proxy and self.synth_proxy.num_elements > 0:
            size = self.synth_proxy.num_elements
            read_pos_summary = "<read_pos:{0}>".format(self.read_pos)
            write_pos_summary = "<write_pos:{0}>".format(self.write_pos)
            proxy_children_sum = self.synth_proxy.get_children_summary()
            children_summary = f"{read_pos_summary} {write_pos_summary} {proxy_children_sum}"
        return LIST_FORMAT.format(
            type_name=self.valobj.GetType().GetUnqualifiedType().GetDisplayTypeName(),
            type_no_template="RingBuffer",
            size=size,
            children=children_summary,
        )

    def num_children(self, max=UINT32_MAX):
        if self.synth_proxy:
            return self.synth_proxy.num_children() + 2
        return 0

    def has_children(self):
        if self.synth_proxy:
            return self.synth_proxy.has_children()
        return False

    def get_index_of_child(self, name: str):
        if self.synth_proxy:
            if name.startswith("[read_pos"):
                return 0
            elif name.startswith("[write_pos"):
                return 1
            return self.synth_proxy.get_child_index(name)
        return None

    def get_child_at_index(self, index):
        if self.synth_proxy:
            if index == 0 or index == 1:
                pos_name = "read_pos" if index == 0 else "write_pos"
                pos_val = self.read_pos if index == 0 else self.write_pos
                synth_name = f"[{pos_name} <{pos_val}>]"
                if pos_val < 0 or pos_val >= self.synth_proxy.num_elements:
                    return self.valobj.CreateValueFromData(
                        synth_name,
                        SBData.CreateDataFromInt(0),
                        self.valobj.target.GetBasicType(eBasicTypeNullPtr),
                    )
                return self.synth_proxy.create_child_at_real_index(pos_val, synth_name)
            return self.synth_proxy.get_child_at_index(index - 2)
        return None


IDRE = "([^,]+)"


def id_template(min, max):
    th = f"{IDRE}"
    if min == 1 and max == 1:
        return th
    temp = f"{th}"
    for i in range(min - 1):
        temp += f",{th}"
    for i in range(max - min):
        temp += f"(?:,{th})?"
    return temp


def get_template_regex(name: str, min, max) -> str:
    return f"^(::)?{name}<{id_template(min, max)}>$"


# fmt: off

HASHSET_PATTERN:str = "^(::)?HashSet<.+(,[^,]+)?(,[^,]+)?>$"
HASHMAP_PATTERN:str = "^(::)?HashMap<.+,.+(,[^,]+)?(,[^,]+)?(,[^,]+)?>$"
LIST_PATTERN:str = "^(::)?List<.+(,[^,]+)?>$"
ARRAY_PATTERN:str = "^(::)?Array$"
TYPEDARRAY_PATTERN:str = "^(::)?TypedArray<.+>$"
DICTIONARY_PATTERN:str = "^(::)?Dictionary$"
VECTOR_PATTERN:str = "^(::)?Vector<.+>$"
HASH_MAP_ELEMENT_PATTERN:str = "^(::)?HashMapElement<.+,.+>$"
KEY_VALUE_PATTERN:str = "^(::)?KeyValue<.+,.+>$"
VMAP_PATTERN:str = "^(::)?VMap<.+,.+>$"
VMAP_PAIR_PATTERN:str = "^(::)?VMap<.+,.+>::Pair$"
VSET_PATTERN:str = "^(::)?VSet<.+>$"
RINGBUFFER_PATTERN:str = "^(::)?RingBuffer<.+>$"
LOCAL_VECTOR_PATTERN:str = "^(::)?LocalVector<.+(,[^,]+){0,3}>$"
PAGED_ARRAY_PATTERN:str = "^(::)?PagedArray<.+>$"
RBMAP_PATTERN:str = "^(::)?RBMap<.+,.+(,[^,]+){0,2}>$"
RBMAP_ELEMENT_PATTERN:str = "^(::)?RBMap<.+,.+(,[^,]+){0,2}>::Element$"


SYNTHETIC_PROVIDERS: dict[str,type] = {
    "^(::)?Variant$":          Variant_SyntheticProvider,
    # HASH_MAP_ELEMENT_PATTERN:  HashMapElement_SyntheticProvider,
    VECTOR_PATTERN:            Vector_SyntheticProvider,
    LIST_PATTERN:              List_SyntheticProvider,
    HASHSET_PATTERN:           HashSet_SyntheticProvider,
    ARRAY_PATTERN:             Array_SyntheticProvider,
    TYPEDARRAY_PATTERN:        Array_SyntheticProvider,
    HASHMAP_PATTERN:           HashMap_SyntheticProvider,
    DICTIONARY_PATTERN:        Dictionary_SyntheticProvider,
    VMAP_PATTERN:              VMap_SyntheticProvider,
    VSET_PATTERN:              VSet_SyntheticProvider,
    RINGBUFFER_PATTERN:        RingBuffer_SyntheticProvider,
    LOCAL_VECTOR_PATTERN:      LocalVector_SyntheticProvider,
    PAGED_ARRAY_PATTERN:       PagedArray_SyntheticProvider,
    RBMAP_PATTERN:             RBMap_SyntheticProvider,
    # RBMAP_ELEMENT_PATTERN:     RBMapElement_SyntheticProvider,
}

SUMMARY_PROVIDERS: dict[str,object] = {
    "^(::)?String$":        String_SummaryProvider,
    "^(::)?Ref<.+>$":       Ref_SummaryProvider,
    "^(::)?Vector2$":       Vector2_SummaryProvider,
    "^(::)?Vector2i$":      Vector2i_SummaryProvider,
    "^(::)?Rect2$":         Rect2_SummaryProvider,
    "^(::)?Rect2i$":        Rect2i_SummaryProvider,
    "^(::)?Vector3$":       Vector3_SummaryProvider,
    "^(::)?Vector3i$":      Vector3i_SummaryProvider,
    "^(::)?Transform2D$":   Transform2D_SummaryProvider,
    "^(::)?Vector4$":       Vector4_SummaryProvider,
    "^(::)?Vector4i$":      Vector4i_SummaryProvider,
    "^(::)?Plane$":         Plane_SummaryProvider,
    "^(::)?Quaternion$":    Quaternion_SummaryProvider,
    "^(::)?AABB$":          AABB_SummaryProvider,
    "^(::)?Basis$":         Basis_SummaryProvider,
    "^(::)?Transform3D$":   Transform3D_SummaryProvider,
    "^(::)?Projection$":    Projection_SummaryProvider,
    "^(::)?Color$":         Color_SummaryProvider,
    "^(::)?StringName$":    StringName_SummaryProvider,
    "^(::)?NodePath$":      NodePath_SummaryProvider,
    "^(::)?RID$":           RID_SummaryProvider,
    "^(::)?Callable$":      Callable_SummaryProvider,
    "^(::)?Signal$":        Signal_SummaryProvider,
    "^(::)?ObjectID$":      ObjectID_SummaryProvider,
    KEY_VALUE_PATTERN:      KeyValue_SummaryProvider,
    HASH_MAP_ELEMENT_PATTERN: HashMapElement_SummaryProvider,
    RBMAP_ELEMENT_PATTERN:     RBMapElement_SummaryProvider,
    VMAP_PAIR_PATTERN:      VMap_Pair_SummaryProvider,
}
# fmt: on

module = sys.modules[__name__]
cpp_category: SBTypeCategory


def attach_synthetic_to_type(type_name, synth_class, is_regex=True):
    global module, cpp_category
    # print_trace('attaching synthetic %s to "%s", is_regex=%s' %(synth_class.__name__, type_name, is_regex))
    synth = SBTypeSynthetic.CreateWithClassName(__name__ + "." + synth_class.__name__)
    synth.SetOptions(eTypeOptionCascade)
    cpp_category.AddTypeSynthetic(SBTypeNameSpecifier(type_name, is_regex), synth)

    def summary_fn(valobj, dict):
        return get_synth_summary(synth_class, valobj, dict)

    # LLDB accesses summary fn's by name, so we need to create a unique one.
    summary_fn.__name__ = "_get_synth_summary_" + synth_class.__name__
    setattr(module, summary_fn.__name__, summary_fn)
    print_trace(f"attaching summary {summary_fn.__name__} to {type_name}, is_regex={is_regex}")
    summary = SBTypeSummary.CreateWithFunctionName(__name__ + "." + summary_fn.__name__)
    summary.SetOptions(eTypeOptionCascade)
    cpp_category.AddTypeSummary(SBTypeNameSpecifier(type_name, is_regex), summary)

    # attach_summary_to_type(summary_fn, type_name, is_regex)


def attach_summary_to_type(type_name, real_summary_fn, is_regex=False, real_fn_name: Optional[str] = None):
    global module, cpp_category
    if not real_fn_name:
        real_fn_name = str(real_summary_fn.__qualname__)

    def __spfunc(valobj, dict):
        try:
            return real_summary_fn(valobj, dict)
        except Exception as e:
            err_msg = "ERROR in " + real_fn_name + ": " + str(e)
            print_verbose(err_msg)
            print_verbose(get_exception_trace(e))
            return f"<{err_msg}>"

    # LLDB accesses summary fn's by name, so we need to create a unique one.
    __spfunc.__name__ = "__spfunc__" + real_fn_name.replace(".", "_")
    setattr(module, __spfunc.__name__, __spfunc)

    summary = SBTypeSummary.CreateWithFunctionName(__name__ + "." + __spfunc.__name__)
    summary.SetOptions(eTypeOptionCascade)
    cpp_category.AddTypeSummary(SBTypeNameSpecifier(type_name, is_regex), summary)


# TODO: Collate globals better
def clear_globals():
    GodotSynthProvider.synth_by_id.clear()
    GodotSynthProvider.next_id = 0
    hex_color_to_name.clear()
    global constructed_the_table
    constructed_the_table = False


def register_all_synth_and_summary_providers():
    force_compat(Opts.MIDEBUGGER_COMPAT)
    clear_globals()
    for key in SUMMARY_PROVIDERS:
        try:
            attach_summary_to_type(key, SUMMARY_PROVIDERS[key], True)
        except Exception as e:
            print_verbose("EXCEPTION: " + str(e))
    for key in SYNTHETIC_PROVIDERS:
        try:
            attach_synthetic_to_type(key, SYNTHETIC_PROVIDERS[key], True)
        except Exception as e:
            print_verbose("EXCEPTION st: " + str(e))


def monkey_patch_optparse():
    if not "bool" in optparse.Option.TYPES:
        optparse.Option.TYPES = optparse.Option.TYPES + ("bool",)
    if not "bool" in optparse.Option.TYPE_CHECKER:
        optparse.Option.TYPE_CHECKER["bool"] = lambda option, opt, value: value.lower() in [
            "true",
            "t",
            "yes",
            "y",
            "1",
        ]


def __lldb_init_module(debugger: SBDebugger, dict):
    global cpp_category

    cpp_category = debugger.GetDefaultCategory()
    register_all_synth_and_summary_providers()
    monkey_patch_optparse()
    print("godot-formatter synth and summary types have been loaded")
    debugger.HandleCommand('command container add godot-formatter -h "godot-formatter commands" -o')
    SetOptsCommand.register_lldb_command(debugger, __name__, "godot-formatter")
    GetOptsCommand.register_lldb_command(debugger, __name__, "godot-formatter")
    ReloadCommand.register_lldb_command(debugger, __name__, "godot-formatter")


class _LLDBCommandBase:
    program = ""
    description = ""

    @classmethod
    def register_lldb_command(cls, debugger: SBDebugger, module_name, container_name):
        if not cls.program:
            print("ERROR: No program name specified for command")
            return
        try:
            parser = cls.create_options()
            cls.__doc__ = parser.format_help() if parser else cls.description
            # Add any commands contained in this module to LLDB
            command = "command script add -o -c %s.%s %s %s" % (
                module_name,
                cls.__name__,
                container_name,
                cls.program,
            )
            debugger.HandleCommand(command)
        except Exception as e:
            print("ERROR: " + str(e))
            print('The "{0}" command failed to install.'.format(cls.program))
            return

        full_program_name = cls.program if not container_name else container_name + " " + cls.program
        print('The "{0}" command has been installed, type "help {0}" for detailed help.'.format(full_program_name))

    @classmethod
    def create_options(cls):
        return None

    def get_short_help(self):
        return self.description

    def get_long_help(self):
        return self.description

    def __init__(self, debugger, unused):
        pass


class ReloadCommand(_LLDBCommandBase):
    program = "reload"
    description = "Reloads all synthetic types and such."

    def __call__(
        self,
        debugger: SBDebugger,
        command,
        exe_ctx: SBExecutionContext,
        result: SBCommandReturnObject,
    ):
        # Use the Shell Lexer to properly parse up command options just like a
        # shell would
        register_all_synth_and_summary_providers()
        # not returning anything is akin to returning success
        return


class GetOptsCommand(_LLDBCommandBase):
    program = "get-opts"
    description = "This command prints a list of the current option settings for the Godot formatter script."

    def __call__(
        self,
        debugger: SBDebugger,
        command,
        exe_ctx: SBExecutionContext,
        result: SBCommandReturnObject,
    ):
        # Use the Shell Lexer to properly parse up command options just like a
        # shell would
        results = []
        dir_opts = dir(Opts)
        for attr in dir(Opts):
            if attr.startswith("__"):
                continue
            result = f"{attr}: {getattr(Opts, attr)}"
            print(result)
            results.append(result)
        result.AppendMessage("\n".join(results))
        result.SetStatus(eReturnStatusSuccessFinishResult)
        # not returning anything is akin to returning success
        return


class SetOptsCommand(_LLDBCommandBase):
    program = "set-opts"
    description = "This command sets the options for the Godot formatter script."

    @classmethod
    def create_options(cls):
        usage = "usage: %prog [options]"

        # Pass add_help_option = False, since this keeps the command in line
        #  with lldb commands, and we wire up "help command" to work by
        # providing the long & short help methods below.
        parser = optparse.OptionParser(
            description=cls.description,
            prog=cls.program,
            usage=usage,
            add_help_option=False,
            formatter=optparse.IndentedHelpFormatter(2, 30, width=80),
        )

        for attr in dir(GodotFormatterOptions):
            if attr.startswith("__"):
                continue
            # get the type of the attribute
            attr_val = getattr(GodotFormatterOptions, attr)
            attr_type = type(attr_val)
            # get the attribute docstring
            help_string = HELP_STRING_MAP[attr] + f" (default: {attr_val})\n"
            parser.add_option(
                f"--{attr.lower().replace('_', '-')}",
                action="store",
                type=attr_type.__name__,
                dest=attr,
                help=help_string,
                metavar=f"<{str(attr_type.__name__).upper()}>",
                # default=attr_val,
            )
        # parser.print_help()
        return parser

    def get_short_help(self):
        return self.description

    def get_long_help(self):
        return self.help_string

    def __init__(self, debugger, unused):
        self.parser = self.create_options()
        self.help_string = self.parser.format_help()

    def __call__(
        self,
        debugger: SBDebugger,
        command,
        exe_ctx: SBExecutionContext,
        result: SBCommandReturnObject,
    ):
        # Use the Shell Lexer to properly parse up command options just like a
        # shell would
        command_args = shlex.split(command)
        try:
            (options, args) = self.parser.parse_args(command_args)
        except:
            if command_args and len(command_args) > 0 and ("--help" in command_args or "-h" in command_args):
                print(self.get_long_help())
                return
            # if you don't handle exceptions, passing an incorrect argument to
            # the OptionParser will cause LLDB to exit (courtesy of OptParse
            # dealing with argument errors by throwing SystemExit)
            print("Error: Unknown option")
            print(self.get_long_help())
            result.SetError("option parsing failed")
            return

        option: str
        set_option = False
        for option in options.__dict__:
            if option.startswith("__"):
                continue
            if options.__dict__[option] is None:
                continue
            set_option = True
            Opts.__setattr__(option, options.__dict__[option])
        if not set_option:
            result.SetError("No options were set")
            self.parser.print_help()
            return

        print("Options have been set. Resetting formatters...")
        register_all_synth_and_summary_providers()
        result.SetStatus(eReturnStatusSuccessFinishNoResult)
        # not returning anything is akin to returning success
        return
