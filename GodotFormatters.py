# import lldb from typings but also from the lldb module
# Description: Godot formatters for lldb

import lldb
import typing
if typing.TYPE_CHECKING:
    from typing import lldb
from lldb import eFormatUnicode32, eDynamicCanRunTarget, eBasicTypeInvalid, eBasicTypeVoid, eBasicTypeChar, eBasicTypeSignedChar, eBasicTypeUnsignedChar, eBasicTypeWChar, eBasicTypeSignedWChar, eBasicTypeUnsignedWChar, eBasicTypeChar16, eBasicTypeChar32, eBasicTypeChar8, eBasicTypeShort, eBasicTypeUnsignedShort, eBasicTypeInt, eBasicTypeUnsignedInt, eBasicTypeLong, eBasicTypeUnsignedLong, eBasicTypeLongLong, eBasicTypeUnsignedLongLong, eBasicTypeInt128, eBasicTypeUnsignedInt128, eBasicTypeBool, eBasicTypeHalf, eBasicTypeFloat, eBasicTypeDouble, eBasicTypeLongDouble, eBasicTypeFloatComplex, eBasicTypeDoubleComplex, eBasicTypeLongDoubleComplex, eBasicTypeObjCID, eBasicTypeObjCClass, eBasicTypeObjCSel, eBasicTypeNullPtr, eTypeClassClass, eTypeClassEnumeration, eTypeClassPointer
from lldb import SBValue, SBAddress, SBData, SBType, SBTypeEnumMember, SBTypeEnumMemberList, SBSyntheticValueProvider, SBError, SBTarget, SBDebugger
from enum import Enum
import weakref

# Summary string config
NULL_SUMMARY = "<null>"
EMPTY_SUMMARY = "<empty>"
INVALID_SUMMARY = "<invalid>"
SIZE_SUMMARY = "<size: {0}>"
SUMM_STR_MAX_LEN = 100
MAX_DEPTH = 5
MAX_CHILDREN_IN_SUMMARY = 6
HASH_MAP_KEY_VAL_LIST_STYLE = False # if true, will display children in HashMaps in a key-value list style (e.g. ["key"] = "value"); if false, will display children in an indexed-list style (e.g. [0] = ["key"]: "value")

# Synthetic list-like configs; because linked-lists need to traverse the list to get a specific element, we need to cache the members to be performant.
NO_CACHE_MEMBERS = False
CACHE_MIN = 500
CACHE_MAX = 5000

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




def GetFloat(valobj: SBValue):
    dataArg: SBData = valobj.GetData()
    if valobj.GetByteSize() > 4:
        # real_t is a double
        return dataArg.GetDouble(SBError(), 0)
    else:
        # real_t is a float
        return dataArg.GetFloat(SBError(), 0)

def GetFloatStr(valobj: SBValue):
    return str(GetFloat(valobj))



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
        return data.GetChildMemberWithName("_transform2d")
    elif type == VariantType.AABB.value:
        return data.GetChildMemberWithName("_aabb")
    elif type == VariantType.BASIS.value:
        return data.GetChildMemberWithName("_basis")
    elif type == VariantType.TRANSFORM3D.value:
        return data.GetChildMemberWithName("_transform3d")
    elif type == VariantType.PROJECTION.value:
        return data.GetChildMemberWithName("_projection")
    elif (type == VariantType.STRING.value):  # For _mem values, we have to cast them to the correct type
        # find the type for "String"
        stringType: SBType = target.FindFirstType("::String")
        string: SBValue = target.CreateValueFromAddress("[string]", mem_addr, stringType)
        return string
    elif type == VariantType.VECTOR2.value:
        vector2Type: SBType = target.FindFirstType("::Vector2")
        vector2: SBValue = target.CreateValueFromAddress("[vector2]", mem_addr, vector2Type)
        return vector2
    elif type == VariantType.VECTOR2I.value:
        vector2Type: SBType = target.FindFirstType("::Vector2i")
        vector2: SBValue = target.CreateValueFromAddress("[vector2i]", mem_addr, vector2Type)
        return vector2
    elif type == VariantType.RECT2.value:
        rect2Type: SBType = target.FindFirstType("::Rect2")
        rect2: SBValue = target.CreateValueFromAddress("[rect2]", mem_addr, rect2Type)
        return rect2
    elif type == VariantType.RECT2I.value:
        rect2Type: SBType = target.FindFirstType("::Rect2i")
        rect2: SBValue = target.CreateValueFromAddress("[rect2i]", mem_addr, rect2Type)
        return rect2
    elif type == VariantType.VECTOR3.value:
        vector3Type: SBType = target.FindFirstType("::Vector3")
        vector3: SBValue = target.CreateValueFromAddress("[vector3]", mem_addr, vector3Type)
        return vector3
    elif type == VariantType.VECTOR3I.value:
        vector3Type: SBType = target.FindFirstType("::Vector3i")
        vector3: SBValue = target.CreateValueFromAddress("[vector3i]", mem_addr, vector3Type)
        return vector3
    elif type == VariantType.VECTOR4.value:
        vector4Type: SBType = target.FindFirstType("::Vector4")
        vector4: SBValue = target.CreateValueFromAddress("[vector4]", mem_addr, vector4Type)
        return vector4
    elif type == VariantType.VECTOR4I.value:
        vector4Type: SBType = target.FindFirstType("::Vector4i")
        vector4: SBValue = target.CreateValueFromAddress("[vector4i]", mem_addr, vector4Type)
        return vector4
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
    elif type == VariantType.PACKED_BYTE_ARRAY.value:
        packedByteArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<unsigned char>")
        packedByteArray: SBValue = target.CreateValueFromAddress("packedByteArrayref", packed_array_addr, packedByteArrayType)
        return packedByteArray.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_INT32_ARRAY.value:
        packedInt64ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<int>")
        packedInt32Array: SBValue = target.CreateValueFromAddress("packedInt32Arrayref", packed_array_addr, packedInt64ArrayType)
        return packedInt32Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_INT64_ARRAY.value:
        packedInt64ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<long long>")
        packedInt64Array: SBValue = target.CreateValueFromAddress("packedInt64Arrayref", packed_array_addr, packedInt64ArrayType)
        return packedInt64Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_FLOAT32_ARRAY.value:
        packedFloat32ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<float>")
        packedFloat32Array: SBValue = target.CreateValueFromAddress("packedFloat32Arrayref", packed_array_addr, packedFloat32ArrayType)
        return packedFloat32Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_FLOAT64_ARRAY.value:
        packedFloat64ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<double>")
        packedFloat64Array: SBValue = target.CreateValueFromAddress("packedFloat64Arrayref", packed_array_addr, packedFloat64ArrayType)
        return packedFloat64Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_VECTOR2_ARRAY.value:
        packedVector2ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Vector2>")
        packedVector2Array: SBValue = target.CreateValueFromAddress("packedVector2Arrayref", packed_array_addr, packedVector2ArrayType)
        return packedVector2Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_VECTOR3_ARRAY.value:
        packedVector3ArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Vector3>")
        packedVector3Array: SBValue = target.CreateValueFromAddress("packedVector3Arrayref", packed_array_addr, packedVector3ArrayType)
        return packedVector3Array.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_STRING_ARRAY.value:
        packedStringArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<String>")
        packedStringArray: SBValue = target.CreateValueFromAddress("packedStringArrayref", packed_array_addr, packedStringArrayType)
        return packedStringArray.GetChildMemberWithName("array")
    elif type == VariantType.PACKED_COLOR_ARRAY.value:
        packedColorArrayType: SBType = target.FindFirstType("Variant::PackedArrayRef<Color>")
        packedColorArray: SBValue = target.CreateValueFromAddress("packedColorArrayref", packed_array_addr, packedColorArrayType)
        return packedColorArray.GetChildMemberWithName("array")
    else:
        return None


def Variant_SummaryProvider(valobj: SBValue, internal_dict):
    if valobj.IsSynthetic():
        return Variant_SyntheticProvider(valobj.GetNonSyntheticValue(), internal_dict).get_summary()
    else:
        return Variant_SyntheticProvider(valobj, internal_dict).get_summary()

class Variant_SyntheticProvider:
    def __init__(self, valobj: SBValue, internal_dict):
        self.valobj = valobj
        self.internal_dict = internal_dict

    def _get_variant_type(self):
        return self.valobj.GetChildMemberWithName("type").GetValueAsUnsigned()

    def get_summary(self):
        type = self._get_variant_type()
        if type == VariantType.NIL.value:
            return "nil"
        elif type >= VariantType.VARIANT_MAX.value:
            return INVALID_SUMMARY
        data = Variant_GetValue(self.valobj)
        if data is None or not data.IsValid():
            return INVALID_SUMMARY
        if type == VariantType.BOOL.value:
            return "true" if data.GetValueAsUnsigned() != 0 else "false"
        elif type == VariantType.INT.value:
            return str(data.GetValueAsSigned())
        elif type == VariantType.FLOAT.value:
            return GetFloatStr(data)
        elif type == VariantType.OBJECT.value:
            prefix = "{" + str(data.GetType().GetPointeeType().GetDisplayTypeName())+ "*:"
            # TODO: avoiding infinite recursion here by not calling GenericShortSummary
            # return prefix + GenericShortSummary(data, self.internal_dict, len(prefix)+1, True) + "}"
            return prefix + "{...}}"
        else:
            # _data = self.valobj.GetChildMemberWithName("_data")
            # if not _data.IsValid():
            #     return INVALID_SUMMARY
            # _ptr = _data.GetChildMemberWithName("_ptr")
            # if not is_valid_pointer(_ptr):
            #     return INVALID_SUMMARY
            summary = data.GetSummary()
            if not summary:
                summary = "{" + data.GetDisplayTypeName() + ":{...}}"
            return summary

    def num_children(self):
        var_type = self._get_variant_type()
        if (
            var_type == VariantType.NIL.value
            or var_type >= VariantType.VARIANT_MAX.value
        ):
            return 0
        else:
            return 1

    def has_children(self):
        return self.num_children() != 0

    def get_child_index(self, name: str):
        return 0 if self.has_children() else None

    def get_child_at_index(self, index):
        return Variant_GetValue(self.valobj)


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
    try:
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
    except Exception as e:
        rstr = "EXCEPTION: " + str(e)
    return rstr


def Quaternion_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{{0}, {1}, {2}, {3}}}".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
        GetFloat(valobj.GetChildMemberWithName("w")),
    )

def ObjectID_SummaryProvider(valobj: SBValue, internal_dict):
    fmt = "<ObjectID={0}>"
    id: SBValue = valobj.GetChildMemberWithName("id")
    if (not id.IsValid()):
        return fmt.format(INVALID_SUMMARY)
    val = id.GetValueAsUnsigned()
    if val == 0:
        return fmt.format(NULL_SUMMARY)
    return fmt.format(val)

def Signal_SummaryProvider(valobj: SBValue, internal_dict):
    # Signal has a StringName name and an ObjectID object
    name: SBValue = valobj.GetChildMemberWithName("name")
    object: SBValue = valobj.GetChildMemberWithName("object")
    return "{{name:{0}, object:{1}}}".format(
        name.GetSummary(),
        object.GetSummary(),
    )


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
            return "{{<CallableCustom> {0}:{...}}}".format(custom_type.GetPointeeType().GetDisplayTypeName())
            # return "CallableCustom: " + GenericShortSummary(custom, internal_dict)
        else:
            # get the object
            obj_id: SBValue = valobj.GetChildMemberWithName("object")
            obj_id_val = obj_id.GetValueAsUnsigned()
            if obj_id_val == 0:
                return "{<Callable> " + NULL_SUMMARY + ""
            return "{{<Callable> object:{0}, method:{1}}}".format(
                obj_id_val, method_name
            )


def Vector2_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
    )


def Vector3_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
    )


def Vector4_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2}, {3})".format(
        GetFloat(valobj.GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("z")),
        GetFloat(valobj.GetChildMemberWithName("w")),
    )


def Vector2i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
    )


def Vector3i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
        valobj.GetChildMemberWithName("z").GetValueAsSigned(),
    )


def Vector4i_SummaryProvider(valobj: SBValue, internal_dict):
    return "({0}, {1}, {2}, {3})".format(
        valobj.GetChildMemberWithName("x").GetValueAsSigned(),
        valobj.GetChildMemberWithName("y").GetValueAsSigned(),
        valobj.GetChildMemberWithName("z").GetValueAsSigned(),
        valobj.GetChildMemberWithName("w").GetValueAsSigned(),
    )


def Rect2_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: ({0}, {1}), size: ({2}, {3})}}".format(
        GetFloat(valobj.GetChildMemberWithName("position").GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("position").GetChildMemberWithName("y")),
        GetFloat(valobj.GetChildMemberWithName("size").GetChildMemberWithName("x")),
        GetFloat(valobj.GetChildMemberWithName("size").GetChildMemberWithName("y")),
    )


def Rect2i_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: ({0}, {1}), size: ({2}, {3})}}".format(
        valobj.GetChildMemberWithName("position")
        .GetChildMemberWithName("x")
        .GetValueAsSigned(),
        valobj.GetChildMemberWithName("position")
        .GetChildMemberWithName("y")
        .GetValueAsSigned(),
        valobj.GetChildMemberWithName("size")
        .GetChildMemberWithName("x")
        .GetValueAsSigned(),
        valobj.GetChildMemberWithName("size")
        .GetChildMemberWithName("y")
        .GetValueAsSigned(),
    )


import math


def _get_hex(val: float):
    new_val = max(min(round(val * 255), 255), 0)
    return "{:02x}".format(new_val)


def Color_SummaryProvider(valobj: SBValue, internal_dict):
    r, g, b, a = (
        GetFloat(valobj.GetChildMemberWithName("r")),
        GetFloat(valobj.GetChildMemberWithName("g")),
        GetFloat(valobj.GetChildMemberWithName("b")),
        GetFloat(valobj.GetChildMemberWithName("a")),
    )
    r_hex, g_hex, b_hex, a_hex = _get_hex(r), _get_hex(g), _get_hex(b), _get_hex(a)
    return "{{<#{0}{1}{2}{3}> r:{4}, g:{5}, b:{6}, a:{7}}}".format(
        r_hex, g_hex, b_hex, a_hex, r, g, b, a
    )


def Plane_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{normal: {0}, d: {1}}}".format(
        valobj.GetChildMemberWithName("normal").GetSummary(),
        valobj.GetChildMemberWithName("d").GetValueAsSigned(),
    )


def AABB_SummaryProvider(valobj: SBValue, internal_dict):
    return "{{position: {{{0}}}, size: {{{1}}}}}".format(
        valobj.GetChildMemberWithName("position").GetSummary(),
        valobj.GetChildMemberWithName("size").GetSummary(),
    )


def Transform2D_SummaryProvider(valobj: SBValue, internal_dict):
    # transform2d has a Vector2 `origin`, Vector2 `x`, and Vector2 `y`
    x_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(0)
    y_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(1)
    o_row = valobj.GetChildMemberWithName("columns").GetChildAtIndex(2)
    return "{{x: {0}, y: {1}, o: {2}}}".format(
        x_row.GetSummary(), y_row.GetSummary(), o_row.GetSummary()
    )


def Transform3D_SummaryProvider(valobj: SBValue, internal_dict):
    # transform3d has a Basis `basis` and Vector3 `origin`
    return "{{basis: {0}, origin: {1}}}".format(
        valobj.GetChildMemberWithName("basis").GetSummary(),
        valobj.GetChildMemberWithName("origin").GetSummary(),
    )


def Projection_SummaryProvider(valobj: SBValue, internal_dict):
    # projection has 	`Vector4 columns[4]`
    return "{{columns: {{{0}, {1}, {2}, {3}}}}}".format(
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(0).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(1).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(2).GetSummary(),
        valobj.GetChildMemberWithName("columns").GetChildAtIndex(3).GetSummary(),
    )


def Basis_SummaryProvider(valobj: SBValue, internal_dict):
    # basis has a Vector3[3] `rows` (NOT `elements`)
    # need to translate into (xx, xy, xy), (yx, yy, yz), (zx, zy, zz)
    x_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(0)
    y_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(1)
    z_row = valobj.GetChildMemberWithName("rows").GetChildAtIndex(2)
    return "{{{0}, {1}, {2}}}".format(
        x_row.GetSummary(), y_row.GetSummary(), z_row.GetSummary()
    )

def RID_SummaryProvider(valobj: SBValue, internal_dict):
    return "<RID=" + str(valobj.GetChildMemberWithName("_id").GetValueAsUnsigned()) + ">"

def String_SummaryProvider(valobj: SBValue, internal_dict):
    try:
        _cowdata: SBValue = valobj.GetChildMemberWithName("_cowdata")
        size = _get_cowdata_size(_cowdata)
        if size is None:
            return INVALID_SUMMARY
        if size == 0:
            return EMPTY_SUMMARY
        _ptr: SBValue = _cowdata.GetChildMemberWithName("_ptr")
        _ptr.format = eFormatUnicode32
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
    except Exception as e:
        return "<String> EXCEPTION: " + str(e)

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
    "ObjectID"
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

def is_string_type(type: SBType):
    type_class = type.GetTypeClass() 
    if (type_class == eTypeClassClass or type_class == eTypeClassPointer):
        if (type_class == eTypeClassPointer):
            type: SBType = type.GetPointeeType()
        type_name: str = type.GetUnqualifiedType().GetDisplayTypeName()
        if (type_name == "String"):
            return True
        elif (type_name == "StringName"):
            return True
        elif (type_name == "StringBuffer"):
            return True
        elif (type_name == "NodePath"):
            return True
    elif is_basic_string_type(type):
        return True
        
    return False

def is_basic_integer_type(type:SBType):
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

def get_enum_string(valobj: SBValue):
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
            return name # + " (" + str(starting_value) + ")"
    return "<Invalid Enum> (" + str(starting_value) + ")"


def get_basic_printable_string(valobj: SBValue):
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
        return valobj.GetSummary()
    if basic_type == eBasicTypeObjCClass:
        return valobj.GetSummary()
    if basic_type == eBasicTypeObjCSel:
        return valobj.GetSummary()
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
    
# cow_err_str = ""
def is_valid_pointer(ptr: SBValue) -> bool:
    # global cow_err_str
    if not ptr:
        # cow_err_str = "is_valid_pointer(): ptr is None"
        return False
    if not ptr.IsValid():
        # cow_err_str = "is_valid_pointer(): ptr is not valid SBValue"
        return False
    if not ptr.GetType().IsPointerType():
        # cow_err_str = "is_valid_pointer(): ptr is not a pointer"
        return False
    if ptr.GetValueAsUnsigned() == 0:
        # cow_err_str = "is_valid_pointer(): ptr = nullptr"
        return False
    if not ptr.Dereference().IsValid():
        # cow_err_str = "is_valid_pointer(): ptr dereference is not valid"
        return False
    return True

def pointer_exists_and_is_null(ptr: SBValue) -> bool:
    if not ptr or not ptr.IsValid():
        return False
    if not ptr.GetType().IsPointerType():
        return False
    if ptr.GetValueAsUnsigned() == 0:
        return True
    return False

# Cowdata size is located at the cowdata address - 8 bytes (sizeof(uint64_t))

def _get_cowdata_size(_cowdata: SBValue, null_means_zero = True) -> int:
    # global cow_err_str
    size = 0
    if not _cowdata or not _cowdata.IsValid():
        # cow_err_str = "COWDATASIZE Invalid: _cowdata is not valid"
        return None
    try:
        _ptr: SBValue = _cowdata.GetChildMemberWithName("_ptr")
        if null_means_zero and pointer_exists_and_is_null(_ptr):
            return 0
        if (not is_valid_pointer(_ptr)):
            # cow_err_str = "COWDATASIZE Invalid: " + cow_err_str
            return None
        _cowdata_template_type: SBType = _cowdata.GetType().GetTemplateArgumentType(0)
        if not _cowdata_template_type.IsValid():
            # cow_err_str = "COWDATASIZE Invalid: _cowdata template type is not valid"
            return None
        uint64_type: SBType = _cowdata.GetTarget().GetBasicType( eBasicTypeUnsignedLongLong )
        ptr_addr_val = _ptr.GetValueAsUnsigned()
        size_child: SBValue = _ptr.CreateValueFromAddress("size", ptr_addr_val - 8, uint64_type )
        size = size_child.GetValueAsSigned()
        if size < 0:
            # cow_err_str = "COWDATASIZE Invalid: Size is less than 0: " + str(size)
            return None
        if size > 0:
            last_val: SBValue = _ptr.GetChildAtIndex(size - 1, eDynamicCanRunTarget, True)
            if (not last_val.IsValid()):
                # cow_err_str = "COWDATASIZE Invalid: Last value is not valid: " + str(last_val)
                return None
    except Exception as e:
        # cow_err_str = "COWDATASIZE EXCEPTION:" + str(e)
        return None
    # cow_err_str = ""
    return size

def is_cowdata_valid(_cowdata: SBValue) -> bool:
    size = _get_cowdata_size(_cowdata)
    if size is None:
        return False
    return True

def get_cowdata_size(_cowdata: SBValue) -> int:
    # check to see if _ptr is null
    size = _get_cowdata_size(_cowdata)
    if size is None:
        return 0
    return size

def GenericShortSummary(
    valobj: SBValue,
    internal_dict,
    summary_length=0,
    skip_base_class=False,
    no_children=False,
    depth = 0
):
    if not valobj or not valobj.IsValid():
        return INVALID_SUMMARY
    depth += 1
    START_SUMMARY_LENGTH = summary_length
    is_child = summary_length != 0
    MAX_LEN = SUMM_STR_MAX_LEN - (20 if is_child else 0)
    if summary_length > SUMM_STR_MAX_LEN or depth > MAX_DEPTH:
        # bail out
        return "{...}"
    type: SBType = valobj.GetType()
    if is_basic_printable_type(type):
        return get_basic_printable_string(valobj)

    if (type.IsPointerType()):
        type = type.GetPointeeType()
    unqual_type_name = str(type.GetUnqualifiedType().GetDisplayTypeName())
    if unqual_type_name == "Object" or unqual_type_name == "RefCounted": # these lead to circular references
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
        deref_type_name = str(deref.GetDisplayTypeName())
        # seen_objects.append(deref)
        return ( "{[" + deref_type_name + "]:" + GenericShortSummary(deref, internal_dict, START_SUMMARY_LENGTH + 1, True, no_children, depth) + "}")
    summ = None
    if valobj.GetTypeSynthetic(): # Synthetic types will call this function again and could lead to infinite recursion.
        if unqual_type_name == "Variant":
            # Avoid putting it through the synthetic provider.
            variant_value = Variant_GetValue(valobj.GetNonSyntheticValue())
            return GenericShortSummary(variant_value, internal_dict, summary_length, skip_base_class, no_children, depth)
        else:
            return "{...}"
    else:
        try:
            summ = valobj.GetSummary()
        except Exception as e:
            summ = " !!EXCEPTION: " + str(e)
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
        for i in range(num_children):
            child: SBValue = valobj.GetChildAtIndex(i)
            prefix = child.name + ":"
            if skip_base_class and base_class_names.count(child.name) > 0:
                continue
            if is_basic_printable_type(child.GetType()):
                summ_str += prefix + get_basic_printable_string(child)
            else:
                summ_str += prefix + GenericShortSummary( child, internal_dict, len(summ_str) + START_SUMMARY_LENGTH, False, no_children, depth)
            if len(summ_str) + START_SUMMARY_LENGTH > MAX_LEN:
                if i < len(valobj) - 1:
                    summ_str += ", ..."
                break
            if i < len(valobj) - 1:
                summ_str += ", "
        if summ_str == "{":
            summ_str += "..."
        summ_str += "}"
    except Exception as e:
        summ_str += " !!EXCEPTION: " + str(e)
        summ_str += " " + str(valobj.GetDisplayTypeName())
    return summ_str

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
    member: SBValue = obj.GetChildMemberWithName(member)
    member_addr: SBValue = member.AddressOf()
    member_addr_val = member_addr.GetValueAsUnsigned()
    return member_addr_val - element_addr_val


def _HashMapElement_GetKeyValue(valobj: SBValue, internal_dict, is_HashMap_Summary=False, str_len = 0, depth = 0) -> tuple[str,str]:
    if valobj.IsSynthetic():
        valobj = valobj.GetNonSyntheticValue()
    data: SBValue = valobj.GetChildMemberWithName("data")
    key: SBValue = data.GetChildMemberWithName("key")
    value: SBValue = data.GetChildMemberWithName("value")
    key_summary = GenericShortSummary(key, internal_dict, str_len, False, is_HashMap_Summary, depth)
    value_summary = GenericShortSummary(value, internal_dict, str_len, False, is_HashMap_Summary, depth)
    return key_summary, value_summary

def HashMapElement_SummaryProvider(valobj: SBValue, internal_dict, str_len = 0, depth = 0) -> str:
    fmt_str = "[{0}]: {1}"
    key, value = _HashMapElement_GetKeyValue(valobj, internal_dict, False, str_len, depth)
    return fmt_str.format(key, value)

class HashMapElement_SyntheticProvider(SBSyntheticValueProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return HashMapElement_SyntheticProvider(valobj, internal_dict, True).get_summary()
    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        # check if valobj is synthetic, and if so, get the non-synthetic value
        if valobj.IsSynthetic():
            self.was_synthetic = True
            self.valobj = valobj.GetNonSyntheticValue()
        else:
            self.valobj: SBValue = valobj
        self.internal_dict = internal_dict
        self.is_summary: bool = is_summary
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        key: SBValue = data.GetChildMemberWithName("key")
        self.key_template_type: SBType = key.GetType()
        self.key_val_element_style: bool = False
        if HASH_MAP_KEY_VAL_LIST_STYLE and (is_string_type(self.key_template_type) or is_basic_integer_type(self.key_template_type)):
            self.key_val_element_style = True

    def _get_hashmap_keyvalue(self, is_HashMap_Summary=False) -> tuple[SBValue,SBValue]:
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        key: SBValue = data.GetChildMemberWithName("key")
        value: SBValue = data.GetChildMemberWithName("value")
        return key, value

    def get_child_index(self,name):
        if name == "[key]":
            return 0
        elif name == "[value]":
            return 1
        return None
    
    def _get_offset(self, member: str):
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        data_addr: SBValue = data.AddressOf()
        element_addr_val = data_addr.GetValueAsUnsigned()
        member: SBValue = data.GetChildMemberWithName(member)
        member_addr: SBValue = member.AddressOf()
        member_addr_val = member_addr.GetValueAsUnsigned()
        return member_addr_val - element_addr_val

    def _create_member_child(self, member:str):
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        value: SBValue = data.GetChildMemberWithName(member)
        return data.CreateChildAtOffset('[{0}]'.format(member), self._get_offset(member), value.GetType())

    def get_key_value_summaries(self, is_HashMap_Summary=False) -> tuple[str,str]:
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        key: SBValue = data.GetChildMemberWithName("key")
        value: SBValue = data.GetChildMemberWithName("value")
        key_summary = GenericShortSummary(key, self.internal_dict, 0, False, is_HashMap_Summary)
        value_summary = GenericShortSummary(
            value, self.internal_dict, 0, False, is_HashMap_Summary
        )
        return key_summary, value_summary

    def get_child_at_index(self, index):
        data: SBValue = self.valobj.GetChildMemberWithName("data")
        if not data or not data.IsValid() or index < 0 or index > 1:
            return None
        if index == 0:
            key = data.GetChildMemberWithName("key")
            type = key.GetType()
            return key.CreateChildAtOffset('[key]', 0, type)
        else:
            value = data.GetChildMemberWithName("value")
            type = value.GetType()
            return value.CreateChildAtOffset('[value]', 0, type)
        # return self.valobj

    def num_children(self):
        return 2

    def has_children(self):
        return True

    def get_summary(self):
        key, value = self.get_key_value_summaries()
        if self.key_val_element_style and self.was_synthetic:
            return value
        else:
            return "[{0}]: {1}".format(key, value)

def SummaryProviderTemplate(valobj: SBValue, internal_dict, initalizer_function):
    try:
        if valobj.IsSynthetic():
            return initalizer_function(valobj.GetNonSyntheticValue(), internal_dict, True).get_summary()
        else:
            return initalizer_function(valobj, internal_dict, True).get_summary()
    except Exception as e:
        return "EXCEPTION: " + str(e)
    
    

class _VectorLike_SyntheticProvider(SBSyntheticValueProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        self.valobj: SBValue = valobj
        self.internal_dict = internal_dict
        self.type: SBType = valobj.GetType()
        self.typename: str = self.type.GetUnqualifiedType().GetDisplayTypeName()
        self._is_summary: bool = is_summary
        self.no_cache = NO_CACHE_MEMBERS
        self.cache_min = CACHE_MIN if not is_summary else MAX_CHILDREN_IN_SUMMARY
        self.cache_max = CACHE_MAX
        self._cached_size = 0
        self.update()

    @property
    def is_summary(self) -> bool:
        return self._is_summary

    @property
    def num_elements(self) -> int:
        return self._cached_size
    
    @num_elements.setter
    def num_elements(self, value: int):
        self._cached_size = value

    def update(self):
        """
            Override this method to set any state that would normally be set in the constructor
            Note: This MUST update self.num_elements
        """
        raise Exception("Not implemented")

    def _get_size(self) -> int:
        """
            Override this method to return the non-cached number of elements in this vector-like object
        """
        raise Exception("Not implemented")
    
    def _create_child_at_element_index(self, index) -> SBValue:
        """
        Override this method to return the synthetic child at the given index
        """
        raise Exception("Not implemented")

    def _get_child_summary(self, real_index):
        """
        Override this method if you want to provide a custom summary for the child at the given index
        """
        element:SBValue = self._create_child_at_element_index(real_index)
        return GenericShortSummary(element, self.internal_dict, 0, False, True)

    # def get_size_synthetic_child(self):
    #     return self.valobj.CreateValueFromData("[size]", SBData.CreateDataFromInt(self.num_elements), self.valobj.target.GetBasicType(eBasicTypeUnsignedInt))

    def get_children_summary(self, max_children=MAX_CHILDREN_IN_SUMMARY):
        try:
            max_children = min(MAX_CHILDREN_IN_SUMMARY, self.num_elements)
            i: int = 0
            summ_str = ""
            for i in range(max_children):
                summ_str += self._get_child_summary(i)
                if len(summ_str) > SUMM_STR_MAX_LEN:
                    break
                if (max_children != 1 and i < max_children - 1):
                    summ_str += ", "
            if self.num_elements > i + 1:
                summ_str += ", ..."
            return summ_str
        except Exception as e:
            return "<ERROR>: " + str(e)

    def get_child_at_index(self, idx):
        return self._create_child_at_element_index(idx)

    def num_children(self):
        return self.num_elements

    def has_children(self):
        return True

    def get_child_index(self, name: str):
        try:
            return int(name.lstrip("[").rstrip("]"))
        except:
            return None

    def get_summary(self):
        try:
            prefix = "{" + SIZE_SUMMARY.format(self.num_elements)
            if self.num_elements == 0:
                return prefix + "}"
            return prefix + " " + self.get_children_summary() + "}"
        except Exception as e:
            return "<ERROR>: " + str(e)

class Vector_SyntheticProvider(_VectorLike_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        self.template_type: SBType
        self.element_size: int
        self._ptr: SBValue
        super().__init__(valobj, internal_dict, is_summary)

    def update(self):
        try:
            self.num_elements = self._get_size()
            self.template_type: SBType = self.valobj.GetType().GetTemplateArgumentType(0)
            self.element_size: int = self._get_element_size()
            self._ptr: SBValue = self.valobj.GetChildMemberWithName("_cowdata").GetChildMemberWithName("_ptr") if self.num_elements > 0 else None
        except Exception as e:
            err_str = "EXCEPTION: " + str(e)
            raise Exception(err_str)
    def _get_element_size(self):
        return self.valobj.GetType().GetTemplateArgumentType(0).GetByteSize()
    def _get_size(self):
        try:               
            return get_cowdata_size(self.valobj.GetChildMemberWithName("_cowdata"))
        except Exception as e:
            raise Exception("EXCEPTION: " + str(e))

    def _create_child_at_element_index(self, index):
        return self.create_child_at_real_index(index, "[" + str(index) + "]")
    
    # Helper function for proxy providers.
    def create_child_at_real_index(self, index, name):
        if index < 0 or index >= self.num_elements or not self._ptr:
            return None
        try:
            return self._ptr.CreateChildAtOffset(name, self.get_offset_at_index(index), self.template_type)
        except:
            return None
    def get_offset_at_index(self, index):
        return index * self.element_size

class HashSet_SyntheticProvider(_VectorLike_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        super().__init__(valobj, internal_dict, is_summary)

    def update(self):
        self.num_elements = self._get_size()
        self.template_type: SBType = self.valobj.GetType().GetTemplateArgumentType(0)
        self.element_size = self.template_type.GetByteSize()
        self.keys: SBValue = self.valobj.GetChildMemberWithName("keys") if self.num_elements > 0 else None

    def _get_size(self):
        try:
            num = self.valobj.GetChildMemberWithName("num_elements").GetValueAsUnsigned()
            if num > 0:
                keys: SBValue = self.valobj.GetChildMemberWithName("keys")
                if (not is_valid_pointer(keys)):
                    return 0
                # check the last element to see if it's valid
                last_val: SBValue = keys.GetChildAtIndex(num - 1, eDynamicCanRunTarget, True)
                if (not last_val.IsValid()):
                    return 0
            return self.valobj.GetChildMemberWithName("num_elements").GetValueAsUnsigned()
        except:
            return 0

    def _create_child_at_element_index(self, index):
        if index < 0 or index >= self.num_elements or not self.valobj or self.valobj.IsValid() == False:
            return None
        if not self.keys:
            return None
        try:
            return self.keys.CreateChildAtOffset(
                "[" + str(index) + "]", index * self.element_size, self.template_type
            )
        except:
            return None


def _VMap_Pair_get_keypair_summaries(
    valobj: SBValue, internal_dict, is_VMap_Summary=False
) -> tuple[str,str]:
    if valobj.IsSynthetic():
        valobj = valobj.GetNonSyntheticValue()
    key: SBValue = valobj.GetChildMemberWithName("key")
    value: SBValue = valobj.GetChildMemberWithName("value")
    key_summary = GenericShortSummary(key, internal_dict, 0, False, is_VMap_Summary)
    value_summary = GenericShortSummary(value, internal_dict, 0, False, is_VMap_Summary)
    return key_summary, value_summary

def VMap_Pair_SummaryProvider(valobj: SBValue, internal_dict):
    fmt_str = "[{0}]: {1}"
    return fmt_str.format(*_VMap_Pair_get_keypair_summaries(valobj, internal_dict))

class VMap_SyntheticProvider(_VectorLike_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        super().__init__(valobj, internal_dict, is_summary)

    def update(self):
        try:
            self.num_elements = self._get_size()
            self._cowdata: SBValue = None
            self.pair_type: SBType = None
            self.pair_type_size: int = 0
            self._ptr: SBValue = None
            if (self.num_elements == 0):
                return
            self._cowdata: SBValue = self.valobj.GetChildMemberWithName("_cowdata")
            self.pair_type: SBType = self._cowdata.GetType().GetTemplateArgumentType(0)
            self.pair_type_size: int = self.pair_type.GetByteSize()
            self._ptr: SBValue = self.valobj.GetChildMemberWithName("_cowdata").GetChildMemberWithName("_ptr")
        except Exception as e:
            err_str = "EXCEPTION: " + str(e)
            raise Exception(err_str)

    def _get_size(self):
        try:
            return get_cowdata_size(self.valobj.GetChildMemberWithName("_cowdata"))
        except Exception as e:
            raise Exception("EXCEPTION: " + str(e))

    def _get_child_summary(self, index):
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None
        element = self._create_child_at_element_index(index)
        if not element or not element.IsValid():
            return "INVALID"
        key, value = _VMap_Pair_get_keypair_summaries(element, self.internal_dict, True)
        return "[{0}]: {1}".format(key, value)

    def _create_child_at_element_index(self, index):
        if not self._ptr or index < 0 or index >= self.num_elements:
            return None
        try:
            return self._ptr.CreateChildAtOffset("[" + str(index) + "]", index * self.pair_type_size, self.pair_type)
        except:
            return None

class _ListLike_SyntheticProvider(_VectorLike_SyntheticProvider):
    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        self.cached_elements: list[SBValue] = list[SBValue]()
        super().__init__(valobj, internal_dict, is_summary)

    def _cache_elements(self, size: int):
        """
            Override this method to cache non-synthetic elements from the list-like object
        """
        raise Exception("Not implemented")
    def _get_uncached_element_at_index(self, index):
        raise Exception("Not implemented")
    def _create_synthetic_child(self, element:SBValue, index):
        raise Exception("Not implemented")

    def update(self):
        self.num_elements = self._get_size()
        if self.no_cache or self.num_elements == 0:
            return
        self.cached_elements.clear()
        self._cache_elements(self.cache_min)

    def _create_child_at_element_index(self, index):
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None
        
        element: SBValue
        if self.no_cache or index >= self.cache_max:
            element = self._get_uncached_element_at_index(index)
        else:
            if (index >= len(self.cached_elements)):
                self._cache_elements(self.cache_max)
            element: SBValue = self.cached_elements[index]
        return self._create_synthetic_child(element, index)

class HashMap_SyntheticProvider(_ListLike_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        super().__init__(valobj, internal_dict, is_summary)
    
    def update(self):
        self.num_elements = self._get_size()
        if self.no_cache or self.num_elements == 0:
            return
        self.cached_elements.clear()
        self.cached_key_to_idx_map = dict[str, int]()
        self.cached_idx_to_key_map = dict[int, str]()
        self.key_template_type: SBType = self.valobj.GetType().GetTemplateArgumentType(0)
        self.key_val_element_style: bool = False
        if HASH_MAP_KEY_VAL_LIST_STYLE and (is_string_type(self.key_template_type) or is_basic_integer_type(self.key_template_type)):
            self.key_val_element_style = True
        self._cache_elements(self.cache_min)

    def _get_size(self):
        size = self.valobj.GetChildMemberWithName("num_elements").GetValueAsUnsigned()
        if size > 0:
            # check if head_element is valid
            head_element: SBValue = self.valobj.GetChildMemberWithName("head_element")
            if not is_valid_pointer(head_element):
                return 0
            # check if head_element->prev() is nullptr (it should be if the size is > 0)
            prev: SBValue = head_element.GetChildMemberWithName("prev")
            if not pointer_exists_and_is_null(prev):
                return 0
            # check if tail_element is valid
            tail_element: SBValue = self.valobj.GetChildMemberWithName("tail_element")
            if not is_valid_pointer(tail_element):
                return 0
            # check if tail_element->next() is nullptr (it should be if the size is > 0)
            next: SBValue = tail_element.GetChildMemberWithName("next")
            if not pointer_exists_and_is_null(next):
                return 0
            if size >= 2:
                # check if head_element->next() is valid
                next: SBValue = head_element.GetChildMemberWithName("next")
                if not is_valid_pointer(next):
                    return 0
                # check if tail_element->prev() is valid
                prev: SBValue = tail_element.GetChildMemberWithName("prev")
                if not is_valid_pointer(prev):
                    return 0
        return size
    def get_child_index(self, name: str):
        if self.key_val_element_style:
            idx = self.cached_key_to_idx_map[(name.lstrip("[").rstrip("]"))]
            if idx is not None:
                return idx
            while len(self.cached_elements) < self.num_elements:
                new_length = len(self.cached_elements) + self.cache_max
                if new_length > self.num_elements:
                    new_length = self.num_elements
                self._cache_elements(new_length)
                idx = self.cached_key_to_idx_map[(name.lstrip("[").rstrip("]"))]
                if idx is not None:
                    return idx
            return None
        else:
            return int(name.lstrip("[").rstrip("]"))

    def _get_child_summary(self, index):
        if index < 0 or index >= self.num_elements or not self.valobj or self.valobj.IsValid() == False:
            return None
        element = self._create_child_at_element_index(index)
        key, value = _HashMapElement_GetKeyValue(element, self.internal_dict, True)
        return "[{0}]: {1}".format(key, value)

    def _cache_elements(self, size: int):
        if self.num_elements == 0 or size == 0:
            return
        if size > self.num_elements:
            size = self.num_elements
        start = 0
        element: SBValue
        if not self.cached_elements:
            self.cached_elements = list[SBValue]()
        if len(self.cached_elements) == 0:
            element: SBValue = self.valobj.GetChildMemberWithName("head_element")
            self.cached_elements.append(element)
        else:
            start = len(self.cached_elements) - 1
            if start > size:
                return
            element: SBValue = self.cached_elements[start]
        if self.key_val_element_style:
            key = element.GetChildMemberWithName("data").GetChildMemberWithName("key")
            keySummary = GenericShortSummary(key, self.internal_dict, 0, False, False)
            self.cached_key_to_idx_map[keySummary] = start
            self.cached_idx_to_key_map[start] = keySummary
        for _ in range(start + 1, size):
            element = element.GetChildMemberWithName("next")
            if element.GetValueAsUnsigned() == 0:
                break
            self.cached_elements.append(element)
            if self.key_val_element_style:
                key = element.GetChildMemberWithName("data").GetChildMemberWithName("key")
                keySummary = GenericShortSummary(key, self.internal_dict, 0, False, False)
                self.cached_key_to_idx_map[keySummary] = len(self.cached_elements) - 1
                self.cached_idx_to_key_map[len(self.cached_elements) - 1] = keySummary

    def _create_synthetic_child(self, element:SBValue, index):
        if self.key_val_element_style:
            keyname = ""
            if index in self.cached_idx_to_key_map:
                keyname = self.cached_idx_to_key_map[index]
            else:
                key = element.GetChildMemberWithName("data").GetChildMemberWithName("key")
                keyname = GenericShortSummary(key, self.internal_dict, 0, False, False)
        else:
            keyname = str(index)
        value = element.CreateValueFromData("[" + keyname + "]", element.GetData(), element.GetType())
        return value

    def _get_uncached_element_at_index(self, index):
        # linked list, get head_element
        element: SBValue = self.valobj.GetChildMemberWithName("head_element")
        for _ in range(index):
            element = element.GetChildMemberWithName("next")
        return element

class List_SyntheticProvider(_ListLike_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def __init__(self, valobj: SBValue, internal_dict, is_summary = False):
        super().__init__(valobj, internal_dict, is_summary)

    # overrides _VectorLike_SyntheticProvider
    def _get_size(self):
        if not self.valobj.IsValid():
            return 0
        _data: SBValue = self.valobj.GetChildMemberWithName("_data")
        if not is_valid_pointer(_data):
            return 0
        size_cache: SBValue = _data.GetChildMemberWithName('size_cache')
        if not size_cache.IsValid():
            return 0
        size = size_cache.GetValueAsUnsigned()

        size = _data.GetChildMemberWithName('size_cache').GetValueAsUnsigned()
        if (size > 0):
            # check if _data.first.prev_ptr is null
            first: SBValue = _data.GetChildMemberWithName('first')
            if not is_valid_pointer(first):
                return 0
            first_prev: SBValue = first.GetChildMemberWithName('prev_ptr')
            # first_prev should be a null_ptr
            if not pointer_exists_and_is_null(first_prev):
                return 0
            offs = get_offset_of_object_member(first, "value")
            if offs < 0:
                return 0
            last: SBValue = _data.GetChildMemberWithName('last')
            if not is_valid_pointer(last):
                return 0
            last_next: SBValue = last.GetChildMemberWithName('next_ptr')
            # last_next should be a null_ptr
            if not pointer_exists_and_is_null(last_next):
                return 0
            offs = get_offset_of_object_member(last, "value")
            if offs < 0:
                return 0
        return size
    
    # overrides _ListLike_SyntheticProvider

    def _cache_elements(self, size: int):
        if self.num_elements == 0 or size == 0:
            return
        if size > self.num_elements:
            size = self.num_elements
        start = 0
        element: SBValue
        if len(self.cached_elements) == 0:
            _data: SBValue = self.valobj.GetChildMemberWithName("_data")
            element = _data.GetChildMemberWithName("first")
            self.cached_elements.append(element)
        else:
            start = len(self.cached_elements) - 1
            if start > size:
                return
            element = self.cached_elements[start]
        for _ in range(start + 1, size):
            element = element.GetChildMemberWithName("next_ptr")
            if element.GetValueAsUnsigned() == 0:
                break
            self.cached_elements.append(element)

    def _create_synthetic_child(self, element: SBValue, index):
        value: SBValue = element.GetChildMemberWithName("value")
        offset = get_offset_of_object_member(element, "value")
        if offset < 0:
            return None
        return element.CreateChildAtOffset('[{0}]'.format(str(index)), offset, value.GetType())

    def _get_uncached_element_at_index(self, index) -> SBValue:
        if index < 0 or index >= self.num_elements or self.valobj.IsValid() == False:
            return None
        _data: SBValue = self.valobj.GetChildMemberWithName("_data")
        element: SBValue = _data.GetChildMemberWithName("first")
        if element.GetValueAsUnsigned() == 0:
            return None
        for _ in range(index):
            element = element.GetChildMemberWithName("next_ptr")
        return element

class _Proxy_SyntheticProvider(SBSyntheticValueProvider):
    def __init__(self, valobj, internal_dict, is_summary = False):
        self.valobj: SBValue = valobj
        self.internal_dict = internal_dict
        self.is_summary = is_summary
        self.synth_proxy: _VectorLike_SyntheticProvider = None
        self.update()
        
    def update(self):
        """
        set the self.synth_proxy value here
        """
        raise Exception("Not implemented")
    
    def get_summary(self):
        try:
            if self.synth_proxy:
                return self.synth_proxy.get_summary()
        except Exception as e:
            return "EXCEPTION: " + str(e)
        return "{" + SIZE_SUMMARY.format(0) + "}"

    def num_children(self):
        if self.synth_proxy:
            return self.synth_proxy.num_children()
        return 0

    def has_children(self):
        if self.synth_proxy:
            return self.synth_proxy.has_children()
        return False

    def get_child_index(self, name: str):
        if self.synth_proxy:
            return self.synth_proxy.get_child_index(name)
        return None

    def get_child_at_index(self, index):
        if self.synth_proxy:
            return self.synth_proxy.get_child_at_index(index)
        return None

# just a proxy for Vector_SyntheticProvider
class Array_SyntheticProvider(_Proxy_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        _p: SBValue = self.valobj.GetChildMemberWithName("_p")
        if is_valid_pointer(_p):
            array:SBValue = _p.GetChildMemberWithName("array")
            if not array.IsSynthetic():
                self.synth_proxy = Vector_SyntheticProvider(array, self.internal_dict, self.is_summary)
            else:
                self.synth_proxy = Vector_SyntheticProvider(array.GetNonSyntheticValue(), self.internal_dict, self.is_summary)

class Dictionary_SyntheticProvider(_Proxy_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def update(self):
        self.synth_proxy: HashMap_SyntheticProvider = None
        try:
            _p: SBValue = self.valobj.GetChildMemberWithName("_p")
            if is_valid_pointer(_p):
                hash_map: SBValue = _p.GetChildMemberWithName("variant_map")
                if not hash_map.IsSynthetic():
                    self.synth_proxy = HashMap_SyntheticProvider(hash_map, self.internal_dict, self.is_summary)
                else:
                    self.synth_proxy = HashMap_SyntheticProvider(hash_map.GetNonSyntheticValue(), self.internal_dict, self.is_summary)
            else:
                self.synth_proxy = None
        except Exception as e:
            self.exception = e


class VSet_SyntheticProvider(_Proxy_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)

    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        _data: SBValue = self.valobj.GetChildMemberWithName("_data")
        if _data.IsValid():
            if not _data.IsSynthetic():
                self.synth_proxy = Vector_SyntheticProvider(_data, self.internal_dict, self.is_summary)
            else:
                self.synth_proxy = Vector_SyntheticProvider(_data.GetNonSyntheticValue(), self.internal_dict, self.is_summary)


class RingBuffer_SyntheticProvider(_Proxy_SyntheticProvider):
    @staticmethod
    def SummaryProvider(valobj: SBValue, internal_dict):
        return SummaryProviderTemplate(valobj, internal_dict, __class__)
    def update(self):
        self.synth_proxy: Vector_SyntheticProvider = None
        self.read_pos = 0
        self.write_pos = 0
        self.size_mask = 0
        _data: SBValue = self.valobj.GetChildMemberWithName("data")
        if _data.IsValid():
            if not _data.IsSynthetic():
                self.synth_proxy = Vector_SyntheticProvider(_data, self.internal_dict, self.is_summary)
            else:
                self.synth_proxy = Vector_SyntheticProvider(_data.GetNonSyntheticValue(), self.internal_dict, self.is_summary)
            self.size_mask = self.valobj.GetChildMemberWithName("size_mask").GetValueAsSigned()
            self.read_pos = self.valobj.GetChildMemberWithName("read_pos").GetValueAsSigned() & self.size_mask
            self.write_pos = self.valobj.GetChildMemberWithName("write_pos").GetValueAsSigned() & self.size_mask

    def get_summary(self):
        try:
            if self.synth_proxy and self.synth_proxy.num_elements > 0:
                read_pos_summary = "<read_pos:{0}>".format(self.read_pos)
                write_pos_summary = "<write_pos:{0}>".format(self.write_pos)
                size_summary = SIZE_SUMMARY.format(self.synth_proxy.num_elements)
                children_summary = self.synth_proxy.get_children_summary()
                return f'{{{read_pos_summary} {write_pos_summary} {size_summary} {children_summary}}}'
        except Exception as e:
            return "EXCEPTION: " + str(e)
        return "{" + SIZE_SUMMARY.format(0) + "}"


    def num_children(self):
        if self.synth_proxy:
            return self.synth_proxy.num_children() + 2
        return 0

    def has_children(self):
        if self.synth_proxy:
            return self.synth_proxy.has_children()
        return False

    def get_child_index(self, name: str):
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
                synth_name = f'[{pos_name} <{pos_val}>]'
                if pos_val < 0 or pos_val >= self.synth_proxy.num_elements:
                    return self.valobj.CreateValueFromData(synth_name, SBData.CreateDataFromInt(0), self.valobj.target.GetBasicType(eBasicTypeNullPtr))
                return self.synth_proxy.create_child_at_real_index(pos_val, synth_name)
            return self.synth_proxy.get_child_at_index(index - 2)
        return None


# turn off black-formatter
# fmt: off

HASHSET_PATTERN:str = "^(::)?HashSet<.+(,[^,]+)?(,[^,]+)?>$"
HASHMAP_PATTERN:str = "^(::)?HashMap<.+,.+(,[^,]+)?(,[^,]+)?(,[^,]+)?>$"
LIST_PATTERN:str = "^(::)?List<.+(,[^,]+)?>$"
ARRAY_PATTERN:str = "^(::)?Array$"
TYPEDARRAY_PATTERN:str = "^(::)?TypedArray<.+>$"
DICTIONARY_PATTERN:str = "^(::)?Dictionary$"
VECTOR_PATTERN:str = "^(::)?Vector<.+>$"
HASH_MAP_ELEMENT_PATTERN:str = "^(::)?HashMapElement<.+,.+>$"
VMAP_PATTERN:str = "^(::)?VMap<.+,.+>$"
VMAP_PAIR_PATTERN:str = "^(::)?VMap<.+,.+>::Pair$"
VSET_PATTERN:str = "^(::)?VSet<.+>$"
RINGBUFFER_PATTERN:str = "^(::)?RingBuffer<.+>$"

SYNTHETIC_PROVIDERS: dict[str,str] = {
    "^(::)?Variant$":     "Variant_SyntheticProvider",
    HASH_MAP_ELEMENT_PATTERN: "HashMapElement_SyntheticProvider",
    VECTOR_PATTERN:       "Vector_SyntheticProvider",
    LIST_PATTERN:         "List_SyntheticProvider",
    HASHSET_PATTERN:      "HashSet_SyntheticProvider",
    ARRAY_PATTERN:        "Array_SyntheticProvider",
    TYPEDARRAY_PATTERN:   "Array_SyntheticProvider",
    HASHMAP_PATTERN:      "HashMap_SyntheticProvider",
    DICTIONARY_PATTERN:   "Dictionary_SyntheticProvider",
    VMAP_PATTERN:         "VMap_SyntheticProvider",
    VSET_PATTERN:         "VSet_SyntheticProvider",
    RINGBUFFER_PATTERN:   "RingBuffer_SyntheticProvider",
}

SUMMARY_PROVIDERS: list[tuple[str, str]] = [
    ["^(::)?String$", "String_SummaryProvider"],
    ["^(::)?Ref<.+>$", "Ref_SummaryProvider"],
    ["^(::)?Vector2$", "Vector2_SummaryProvider"],
    ["^(::)?Vector2i$", "Vector2i_SummaryProvider"],
    ["^(::)?Rect2$", "Rect2_SummaryProvider"],
    ["^(::)?Rect2i$", "Rect2i_SummaryProvider"],
    ["^(::)?Vector3$", "Vector3_SummaryProvider"],
    ["^(::)?Vector3i$", "Vector3i_SummaryProvider"],
    ["^(::)?Transform2D$", "Transform2D_SummaryProvider"],
    ["^(::)?Vector4$", "Vector4_SummaryProvider"],
    ["^(::)?Vector4i$", "Vector4i_SummaryProvider"],
    ["^(::)?Plane$", "Plane_SummaryProvider"],
    ["^(::)?Quaternion$", "Quaternion_SummaryProvider"],
    ["^(::)?AABB$", "AABB_SummaryProvider"],
    ["^(::)?Basis$", "Basis_SummaryProvider"],
    ["^(::)?Transform3D$", "Transform3D_SummaryProvider"],
    ["^(::)?Projection$", "Projection_SummaryProvider"],
    ["^(::)?Color$", "Color_SummaryProvider"],
    ["^(::)?StringName$", "StringName_SummaryProvider"],
    ["^(::)?NodePath$", "NodePath_SummaryProvider"],
    ["^(::)?RID$", "RID_SummaryProvider"],
    ["^(::)?Callable$", "Callable_SummaryProvider"],
    ["^(::)?Variant$", "Variant_SummaryProvider"],
    ["^(::)?Signal$", "Signal_SummaryProvider"],
    ["^(::)?ObjectID$", "ObjectID_SummaryProvider"],
    [HASH_MAP_ELEMENT_PATTERN, SYNTHETIC_PROVIDERS[HASH_MAP_ELEMENT_PATTERN] + ".SummaryProvider"],
    [VMAP_PAIR_PATTERN, "VMap_Pair_SummaryProvider"],
    [DICTIONARY_PATTERN, SYNTHETIC_PROVIDERS[DICTIONARY_PATTERN] + ".SummaryProvider"],
    [VECTOR_PATTERN, SYNTHETIC_PROVIDERS[VECTOR_PATTERN] + ".SummaryProvider"],
    [LIST_PATTERN, SYNTHETIC_PROVIDERS[LIST_PATTERN] + ".SummaryProvider"],
    [HASHSET_PATTERN, SYNTHETIC_PROVIDERS[HASHSET_PATTERN] + ".SummaryProvider"],
    [ARRAY_PATTERN, SYNTHETIC_PROVIDERS[ARRAY_PATTERN] + ".SummaryProvider"],
    [TYPEDARRAY_PATTERN, SYNTHETIC_PROVIDERS[TYPEDARRAY_PATTERN] + ".SummaryProvider"],
    [HASHMAP_PATTERN, SYNTHETIC_PROVIDERS[HASHMAP_PATTERN] + ".SummaryProvider"],
    [DICTIONARY_PATTERN, SYNTHETIC_PROVIDERS[DICTIONARY_PATTERN] + ".SummaryProvider"],
    [VMAP_PATTERN, SYNTHETIC_PROVIDERS[VMAP_PATTERN] + ".SummaryProvider"],
    [VSET_PATTERN, SYNTHETIC_PROVIDERS[VSET_PATTERN] + ".SummaryProvider"],
    [RINGBUFFER_PATTERN, SYNTHETIC_PROVIDERS[RINGBUFFER_PATTERN] + ".SummaryProvider"],
]
SUMMARY_ADD_COMMAND = 'type summary add -x "{0}" -e -F {1}.{2}'
SYNTHETIC_ADD_COMMAND = 'type synthetic add -x "{0}" -l {1}.{2}'

# Don't need these for now.
# SUMMARY_DELETE_COMMAND = 'type summary delete "{0}"'
# SYNTHETIC_DELETE_COMMAND = 'type synthetic delete "{0}"'

def __lldb_init_module(debugger : SBDebugger, dict):
    for summary in SUMMARY_PROVIDERS:
        debugger.HandleCommand(SUMMARY_ADD_COMMAND.format(summary[0], __name__, summary[1]))
    for key in SYNTHETIC_PROVIDERS:
        debugger.HandleCommand(SYNTHETIC_ADD_COMMAND.format(key, __name__, SYNTHETIC_PROVIDERS[key]))




