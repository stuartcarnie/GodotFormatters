import lldb
from builtins import chr
from enum import Enum

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

def Variant_GetValue(valobj: lldb.SBValue):
        # we need to get the type of the variant
        type = valobj.GetChildMemberWithName('type').GetValueAsUnsigned()
        # switch on type
        data: lldb.SBValue = valobj.GetChildMemberWithName('_data')
        mem: lldb.SBValue = data.GetChildMemberWithName('_mem')
        mem_addr: lldb.SBAddress = mem.GetAddress()
        packed_array: lldb.SBValue = data.GetChildMemberWithName('packed_array')
        packed_array_addr: lldb.SBAddress = packed_array.GetAddress()
        target: lldb.SBTarget = valobj.target
        if type == VariantType.NIL.value:
            return None
        elif type == VariantType.BOOL.value:
            return data.GetChildMemberWithName('_bool')
        elif type == VariantType.INT.value:
            return data.GetChildMemberWithName('_int')
        elif type == VariantType.FLOAT.value:
            return data.GetChildMemberWithName('_float')
        elif type == VariantType.TRANSFORM2D.value:
            return data.GetChildMemberWithName('_transform2d')
        elif type == VariantType.AABB.value:
            return data.GetChildMemberWithName('_aabb')
        elif type == VariantType.BASIS.value:
            return data.GetChildMemberWithName('_basis')
        elif type == VariantType.TRANSFORM3D.value:
            return data.GetChildMemberWithName('_transform3d')
        elif type == VariantType.PROJECTION.value:
            return data.GetChildMemberWithName('_projection')
        elif type == VariantType.STRING.value: #For _mem values, we have to cast them to the correct type
            # find the type for "String" 
            stringType: lldb.SBType = target.FindFirstType('::String')
            string: lldb.SBValue = target.CreateValueFromAddress('string', mem_addr, stringType)
            return string
        elif type == VariantType.VECTOR2.value:
            vector2Type: lldb.SBType = target.FindFirstType('::Vector2')
            vector2: lldb.SBValue = target.CreateValueFromAddress('vector2', mem_addr, vector2Type)
            return vector2
        elif type == VariantType.RECT2.value:
            rect2Type: lldb.SBType = target.FindFirstType('::Rect2')
            rect2: lldb.SBValue = target.CreateValueFromAddress('rect2', mem_addr, rect2Type)
            return rect2
        elif type == VariantType.VECTOR3.value:
            vector3Type: lldb.SBType = target.FindFirstType('::Vector3')
            vector3: lldb.SBValue = target.CreateValueFromAddress('vector3', mem_addr, vector3Type)
            return vector3
        elif type == VariantType.VECTOR4.value:
            vector4Type: lldb.SBType = target.FindFirstType('::Vector4')
            vector4: lldb.SBValue = target.CreateValueFromAddress('vector4', mem_addr, vector4Type)
            return vector4
        elif type == VariantType.PLANE.value:
            planeType: lldb.SBType = target.FindFirstType('::Plane')
            plane: lldb.SBValue = target.CreateValueFromAddress('plane', mem_addr, planeType)
            return plane
        elif type == VariantType.QUATERNION.value:
            quaternionType: lldb.SBType = target.FindFirstType('::Quaternion')
            quaternion: lldb.SBValue = target.CreateValueFromAddress('quaternion', mem_addr, quaternionType)
            return quaternion
        elif type == VariantType.COLOR.value:
            colorType: lldb.SBType = target.FindFirstType('::Color')
            color: lldb.SBValue = target.CreateValueFromAddress('color', mem_addr, colorType)
            return color
        elif type == VariantType.STRING_NAME.value:
            stringNameType: lldb.SBType = target.FindFirstType('::StringName')
            stringName: lldb.SBValue = target.CreateValueFromAddress('stringName', mem_addr, stringNameType)
            return stringName
        elif type == VariantType.NODE_PATH.value:
            nodePathType: lldb.SBType = target.FindFirstType('::NodePath')
            nodePath: lldb.SBValue = target.CreateValueFromAddress('nodePath', mem_addr, nodePathType)
            return nodePath
        elif type == VariantType.RID.value:
            ridType: lldb.SBType = target.FindFirstType('::RID')
            rid: lldb.SBValue = target.CreateValueFromAddress('rid', mem_addr, ridType)
            return rid
        elif type == VariantType.OBJECT.value:
            objDataType: lldb.SBType = target.FindFirstType('Variant::ObjData')
            objData: lldb.SBValue = target.CreateValueFromAddress('objData', mem_addr, objDataType)
            return objData.GetChildMemberWithName('obj')
        elif type == VariantType.DICTIONARY.value:
            dictionaryType: lldb.SBType = target.FindFirstType('::Dictionary')
            dictionary: lldb.SBValue = target.CreateValueFromAddress('dictionary', mem_addr, dictionaryType)
            return dictionary
        elif type == VariantType.ARRAY.value:
            arrayType: lldb.SBType = target.FindFirstType('::Array')
            array: lldb.SBValue = target.CreateValueFromAddress('array', mem_addr, arrayType)
            return array
        elif type == VariantType.PACKED_BYTE_ARRAY.value:
            packedByteArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<unsigned char>')
            packedByteArray: lldb.SBValue = target.CreateValueFromAddress('packedByteArrayref', packed_array_addr, packedByteArrayType)
            return packedByteArray.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_INT32_ARRAY.value:
            packedInt64ArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<int>')
            packedInt32Array: lldb.SBValue = target.CreateValueFromAddress('packedInt32Arrayref', packed_array_addr, packedInt64ArrayType)
            # return packedInt32Array.CreateValueFromData('packedInt32Array', packedInt32Array.GetChildMemberWithName('array'), target.FindFirstType('::PackedInt32Array'))
            packedInt32Array.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_INT64_ARRAY.value:
            packedInt64ArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<long long>')
            packedInt64Array: lldb.SBValue = target.CreateValueFromAddress('packedInt64Arrayref', packed_array_addr, packedInt64ArrayType)
            # return packedInt64Array.CreateValueFromData('packedInt64Array', packedInt64Array.GetChildMemberWithName('array'), target.FindFirstType('::PackedInt64Array'))
            packedInt64Array.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_FLOAT32_ARRAY.value:
            packedFloat32ArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<float>')
            packedFloat32Array: lldb.SBValue = target.CreateValueFromAddress('packedFloat32Arrayref', packed_array_addr, packedFloat32ArrayType)
            # return packedFloat32Array.CreateValueFromData('packedFloat32Array', packedFloat32Array.GetChildMemberWithName('array'), target.FindFirstType('::PackedFloat32Array'))
            packedFloat32Array.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_FLOAT64_ARRAY.value:
            packedFloat64ArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<double>')
            packedFloat64Array: lldb.SBValue = target.CreateValueFromAddress('packedFloat64Arrayref', packed_array_addr, packedFloat64ArrayType)
            # return packedFloat64Array.CreateValueFromData('packedFloat64Array', packedFloat64Array.GetChildMemberWithName('array'), target.FindFirstType('::PackedFloat64Array'))
            packedFloat64Array.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_STRING_ARRAY.value:
            packedStringArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<String>')
            packedStringArray: lldb.SBValue = target.CreateValueFromAddress('packedStringArrayref', packed_array_addr, packedStringArrayType)
            # return packedStringArray.CreateValueFromData('packedStringArray', packedStringArray.GetChildMemberWithName('array'), target.FindFirstType('::PackedStringArray'))
            return packedStringArray.GetChildMemberWithName('array')
        elif type == VariantType.PACKED_COLOR_ARRAY.value:    
            packedColorArrayType: lldb.SBType = target.FindFirstType('Variant::PackedArrayRef<Color>')
            packedColorArray: lldb.SBValue = target.CreateValueFromAddress('packedColorArrayref', packed_array_addr, packedColorArrayType)
            # return packedColorArray.CreateValueFromData('packedColorArray', packedColorArray.GetChildMemberWithName('array'), target.FindFirstType('::PackedColorArray'))
            packedColorArray.GetChildMemberWithName('array')
        else:
            return None

def Variant_SummaryProvider(valobj: lldb.SBValue, internal_dict):
        # we need to get the type of the variant
        if (valobj.IsSynthetic()):
            return Variant_SyntheticProvider(valobj.GetNonSyntheticValue(), internal_dict).get_summary()
        else:
            return Variant_SyntheticProvider(valobj, internal_dict).get_summary()

def GetFloat(valobj: lldb.SBValue):
    dataArg: lldb.SBData = valobj.GetData()
    if valobj.GetByteSize() > 4:
        # real_t is a double
        return dataArg.GetDouble(lldb.SBError(), 0)
    else:
        # real_t is a float
        return dataArg.GetFloat(lldb.SBError(), 0)
    
def GetFloatStr(valobj: lldb.SBValue):
    return str(GetFloat(valobj))

class Variant_SyntheticProvider:
    def __init__(self, valobj, internal_dict):
            self.valobj = valobj            
    def _get_variant_type(self):
        return self.valobj.GetChildMemberWithName('type').GetValueAsUnsigned()
    def get_summary(self):
        type = self._get_variant_type()
        if type == VariantType.NIL.value:
            return 'nil'
        elif type >= VariantType.VARIANT_MAX.value:
            return '[INVALID]'
        data = Variant_GetValue(self.valobj)
        if type == VariantType.BOOL.value:
            return 'true' if data.GetValueAsUnsigned() != 0 else 'false'
        elif type == VariantType.INT.value:
            return str(data.GetValueAsSigned())
        elif type == VariantType.FLOAT.value:
            dataArg: lldb.SBData = data.GetData()
            if data.GetByteSize() > 4:
                # real_t is a double
                return str(dataArg.GetDouble(lldb.SBError(), 0))
            else:
                # real_t is a float
                return str(dataArg.GetFloat(lldb.SBError(), 0))
        elif type == VariantType.OBJECT.value:
            # TODO: do something intelligent here; for now just get the type
            return "{" + str(data.GetType().GetPointeeType().GetDisplayTypeName()) + " {...}}"
        else:
            summary = data.GetSummary()
            if not summary:
                summary = data.GetObjectDescription()
            if not summary:
                summary = data.GetDisplayTypeName()
            return summary
    def num_children(self):
            var_type = self._get_variant_type()
            if var_type == VariantType.NIL.value or var_type >= VariantType.VARIANT_MAX.value:
                    return 0
            else:   
                return 1
    def has_children(self):
            return self.num_children() != 0
    def get_child_index(self,name: str):
            return 0 if self.has_children() else None
    def get_child_at_index(self,index):
            return Variant_GetValue(self.valobj)

def StringName_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    _data: lldb.SBValue = valobj.GetChildMemberWithName('_data')
    if (_data.GetValueAsUnsigned() == 0):
        return "<INVALID>"
    if (_data.GetChildMemberWithName('cname').GetValueAsUnsigned() == 0):
        return _data.GetChildMemberWithName('name').GetSummary()
    else:
        return _data.GetChildMemberWithName('cname').GetSummary()
    
def Ref_SummaryProvider(valobj, internal_dict):
    try:
        reference:lldb.SBValue = valobj.GetChildMemberWithName('reference')
        if (reference.GetValueAsUnsigned() == 0):
            return "<INVALID>"
        deref: lldb.SBValue = reference.Dereference()
        summary = deref.GetSummary()
        type: lldb.SBType = reference.GetType().GetPointeeType()
        # if not summary:
        #     # check for parent types
        #     if type.GetNumberOfDirectBaseClasses() > 0:
        #         for i in range(type.GetNumberOfDirectBaseClasses()-1, -1, -1):
        #             base_type: lldb.SBType = type.GetDirectBaseClassAtIndex(i).GetType()
        #             # return str(base_type.GetDisplayTypeName())
        #             summary = reference.Cast(base_type.GetPointerType()).Dereference().GetSummary()
        #             if not summary:
        #                 summary = reference.Cast(base_type.GetPointerType()).Dereference().GetObjectDescription()
        #             if summary:
        #                 break
        #     if type.GetNumberOfVirtualBaseClasses() > 0:
        #         for i in range(type.GetNumberOfVirtualBaseClasses()-1, -1, -1):
        #             base_type: lldb.SBType = type.GetVirtualBaseClassAtIndex(i).GetType()
        #             summary = reference.Cast(base_type.GetPointerType()).Dereference().GetSummary()
        #             if summary:
        #                 break
        if not summary:
            # get whatever lldb would normally display for this
            # evalaute the expression and return the result
            # frame : lldb.SBFrame = valobj.GetFrame()
            # expr = "*(%s*)%s" % (str(reference.GetType().GetPointeeType().GetName()), str(reference.GetValueAsUnsigned()))
            # summary = str(frame.EvaluateExpression(expr))
            # just do a {...} for now
            summary = "{" + type.GetDisplayTypeName() + " {...}}"
            
        return summary
    except Exception as e:
        return "EXCEPTION: " + str(e)

def strip_quotes(val: str):
    if (val.startswith('U"')):
        val = val.removeprefix('U"').removesuffix('"')
    else:
        val = val.removeprefix('"').removesuffix('"')
    return val


def NodePath_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    try:
        rstr = ""
        data = valobj.GetChildMemberWithName('data')
        if (data.GetValueAsUnsigned() == 0):
            return "<INVALID>"
        path = Vector_SyntheticProvider(data.GetChildMemberWithName('path').GetNonSyntheticValue(), internal_dict)
        subpath = Vector_SyntheticProvider(data.GetChildMemberWithName('subpath').GetNonSyntheticValue(), internal_dict)
        is_absolute = data.GetChildMemberWithName('absolute').GetValueAsUnsigned()
        if (is_absolute):
            rstr = "/"
        for i in range(path.num_children()):
            rstr += strip_quotes(path.get_child_at_index(i).GetSummary())
            if (i < path.num_children() - 1):
                rstr += "/"
        if (subpath.num_children() > 0):
            rstr += ":"
        for i in range(subpath.num_children()):
            rstr += strip_quotes(subpath.get_child_at_index(i).GetSummary())
            if (i < subpath.num_children() - 1):
                rstr += ":"
    except Exception as e:
        rstr = "EXCEPTION: " + str(e)
    return rstr

def Quaternion_SummaryProvider(valobj, internal_dict):
    return "{{{0}, {1}, {2}, {3}}}".format(GetFloat(valobj.GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('y')), GetFloat(valobj.GetChildMemberWithName('z')), GetFloat(valobj.GetChildMemberWithName('w')))

def Vector3_SummaryProvider(valobj, internal_dict):
    return "{{{0}, {1}, {2}}}".format(GetFloat(valobj.GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('y')), GetFloat(valobj.GetChildMemberWithName('z')))

def Vector2_SummaryProvider(valobj, internal_dict):
    return "{{{0}, {1}}}".format(GetFloat(valobj.GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('y')))

def Vector4_SummaryProvider(valobj, internal_dict):
    return "{{{0}, {1}, {2}, {3}}}".format(GetFloat(valobj.GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('y')), GetFloat(valobj.GetChildMemberWithName('z')), GetFloat(valobj.GetChildMemberWithName('w')))

def Rect2_SummaryProvider(valobj, internal_dict):
    return "{{position= {{{0}, {1}}}, size= {{{2}, {3}}} }}".format(GetFloat(valobj.GetChildMemberWithName('position').GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('position').GetChildMemberWithName('y')), GetFloat(valobj.GetChildMemberWithName('size').GetChildMemberWithName('x')), GetFloat(valobj.GetChildMemberWithName('size').GetChildMemberWithName('y')))

def Rect2i_SummaryProvider(valobj, internal_dict):
    return "{{position= {{{0}, {1}}}, size= {{{2}, {3}}} }}".format(valobj.GetChildMemberWithName('position').GetChildMemberWithName('x').GetValueAsSigned(), valobj.GetChildMemberWithName('position').GetChildMemberWithName('y').GetValueAsSigned(), valobj.GetChildMemberWithName('size').GetChildMemberWithName('x').GetValueAsSigned(), valobj.GetChildMemberWithName('size').GetChildMemberWithName('y').GetValueAsSigned())

def Color_SummaryProvider(valobj, internal_dict):
    return "{{r: {0}, g: {1}, b: {2}, a: {3}}}".format(valobj.GetChildMemberWithName('r').GetValueAsSigned(), valobj.GetChildMemberWithName('g').GetValueAsSigned(), valobj.GetChildMemberWithName('b').GetValueAsSigned(), valobj.GetChildMemberWithName('a').GetValueAsSigned())
#Plane has a Vector3 `normal` and a float `d`
def Plane_SummaryProvider(valobj, internal_dict):
    return "{{normal= {{{0}}}, d= {1}}}".format(valobj.GetChildMemberWithName('normal').GetSummary(), valobj.GetChildMemberWithName('d').GetValueAsSigned())

def AABB_SummaryProvider(valobj, internal_dict):
    # jsut print out the Vector3s
    return "{{position= {{{0}}}, size= {{{1}}}}}".format(valobj.GetChildMemberWithName('position').GetSummary(), valobj.GetChildMemberWithName('size').GetSummary())

def Transform2D_SummaryProvider(valobj, internal_dict):
    # transform2d has a Vector2 `origin`, Vector2 `x`, and Vector2 `y`
    return "{{origin= {{{0}}}, x= {{{1}}}, y= {{{2}}}}}".format(valobj.GetChildMemberWithName('origin').GetSummary(), valobj.GetChildMemberWithName('x').GetSummary(), valobj.GetChildMemberWithName('y').GetSummary())

def Transform3D_SummaryProvider(valobj, internal_dict):
    # transform3d has a Basis `basis` and Vector3 `origin`
    return "{{basis= {{{0}}}, origin= {{{1}}}}}".format(valobj.GetChildMemberWithName('basis').GetSummary(), valobj.GetChildMemberWithName('origin').GetSummary())

def Projection_SummaryProvider(valobj, internal_dict):
    # projection has 	`Vector4 columns[4]`
    return "{{columns= {{{0}, {1}, {2}, {3}}}}}".format(valobj.GetChildMemberWithName('columns').GetChildAtIndex(0).GetSummary(), valobj.GetChildMemberWithName('columns').GetChildAtIndex(1).GetSummary(), valobj.GetChildMemberWithName('columns').GetChildAtIndex(2).GetSummary(), valobj.GetChildMemberWithName('columns').GetChildAtIndex(3).GetSummary())

def Basis_SummaryProvider(valobj, internal_dict):
    # basis has a Vector3[3] `rows` (NOT `elements`)
    # need to translate into (xx, xy, xy), (yx, yy, yz), (zx, zy, zz)
    x_row = valobj.GetChildMemberWithName('rows').GetChildAtIndex(0)   
    y_row = valobj.GetChildMemberWithName('rows').GetChildAtIndex(1)
    z_row = valobj.GetChildMemberWithName('rows').GetChildAtIndex(2) 
    return "{{({0}), ({1}), ({2})}}".format(x_row.GetSummary(), y_row.GetSummary(), z_row.GetSummary())

def Dictionary_SummaryProvider(valobj, internal_dict):
    return "DICT" # TODO

def Array_SummaryProvider(valobj, internal_dict):
    return Array_SyntheticProvider(valobj if not valobj.IsSynthetic() else valobj.GetNonSyntheticValue(), internal_dict).get_summary()
class Array_SyntheticProvider:
    def __init__(self, valobj, internal_dict):
            self.valobj = valobj
            
    def get_summary(self):
        return "size = " + str(self.num_children())

    def num_children(self):
            try:
                _p = self.valobj.GetChildMemberWithName('_p')
                if (_p.GetValueAsUnsigned() == 0):
                    return 0
                return getCowDataSize(_p.GetChildMemberWithName('array').GetChildMemberWithName('_cowdata'))
            except:
                    return 0
    def has_children(self):
            return True
    def get_child_index(self,name: str):
            try:
                    return int(name.lstrip('[').rstrip(']'))
            except:
                    return None

    def get_child_at_index(self,index):
            if index < 0:
                    return None
            if index >= self.num_children():
                    return None
            if self.valobj.IsValid() == False:
                    return None
            _p = self.valobj.GetChildMemberWithName('_p')
            array = _p.GetChildMemberWithName('array')
            _ptr: lldb.SBValue = array.GetChildMemberWithName('_cowdata').GetChildMemberWithName('_ptr')
            if _ptr.GetValueAsUnsigned() == 0:
                    return None
            try:
                # vector is a templated argument
                # _cowdata._ptr is a pointer of the same type as the vector template
                # we need to get the type of the vector template
                type: lldb.SBType = array.GetType().GetTemplateArgumentType(0)
                elementSize = type.GetByteSize()
                return _ptr.CreateChildAtOffset('[' + str(index) + ']', index * elementSize, type)
            except:
                    return _ptr.CreateChildAtOffset()
                
class TypedArray_SyntheticProvider(Array_SyntheticProvider):
    def get_child_at_index(self,index):
        # call the super, but then cast the result to the correct type
        child = super().get_child_at_index(index)
        return child #Variant_GetValue(child)


def String_SummaryProvider(valobj : lldb.SBValue, internal_dict):
    # frame: lldb.SBFrame = valobj.GetFrame()
    try:
        _cowdata: lldb.SBValue = valobj.GetChildMemberWithName('_cowdata')
        size = getCowDataSize(_cowdata)
        if (size == 0):
            return "[empty]"
        _ptr: lldb.SBValue = _cowdata.GetChildMemberWithName('_ptr')
        _ptr.format = lldb.eFormatUnicode32
        data:lldb.SBData = _ptr.GetPointeeData(0, size)
        error: lldb.SBError = lldb.SBError()
        arr: bytearray = bytearray()
        for i in range(data.size):
            var = data.GetUnsignedInt8(error, i)
            arr.append(var)
        star = arr.decode('utf-32LE')
        if star.endswith('\x00'):
            star = star[:-1]
        return 'U"{0}"'.format(star)
    except Exception as e:
        return "EXCEPTION: " + str(e)

def get_numeric_string(valobj: lldb.SBValue):
    basic_type = valobj.GetType().GetCanonicalType().GetBasicType()
    if basic_type == lldb.eBasicTypeInvalid: return "[null]"
    if basic_type == lldb.eBasicTypeVoid: return "[void]"
    if basic_type == lldb.eBasicTypeObjCID: return  valobj.GetSummary()
    if basic_type == lldb.eBasicTypeObjCClass: return valobj.GetSummary()
    if basic_type == lldb.eBasicTypeObjCSel: return  valobj.GetSummary()
    if basic_type == lldb.eBasicTypeNullPtr: return  "[null]"
    if basic_type == lldb.eBasicTypeChar: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeSignedChar: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedChar: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeWChar: return  str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeSignedWChar: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedWChar: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeChar16: return  str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeChar32: return  str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeChar8: return  str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeShort: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedShort: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeInt: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedInt: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeLong: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedLong: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeLongLong: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedLongLong: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeInt128: return str(valobj.GetValueAsSigned())
    if basic_type == lldb.eBasicTypeUnsignedInt128: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeBool: return  str(valobj.GetValueAsUnsigned())
    if basic_type == lldb.eBasicTypeHalf: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeFloat: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeDouble: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeLongDouble: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeFloatComplex: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeDoubleComplex: return GetFloatStr(valobj)
    if basic_type == lldb.eBasicTypeLongDoubleComplex: return GetFloatStr(valobj)

#Cowdata size is located at the cowdata address - 4 bytes (sizeof(uint32_t))
def getCowDataSize(_cowdata : lldb.SBValue) -> int:
    # check to see if _ptr is null
    size = 0
    try:
        _ptr: lldb.SBValue = _cowdata.GetChildMemberWithName('_ptr')
        if (not _ptr.IsValid() or _ptr.GetValueAsUnsigned() == 0):
            return 0
        uint32_type: lldb.SBType = _cowdata.GetTarget().GetBasicType(lldb.eBasicTypeUnsignedInt)
        _ptr_addr = _ptr.GetValueAsUnsigned()
        _uint32_ptr: lldb.SBValue = _ptr.Cast(uint32_type.GetPointerType())
        size_val : lldb.SBValue = _uint32_ptr.CreateValueFromAddress('size', _ptr_addr-4, uint32_type)
        size = size_val.GetValueAsUnsigned()
    except:
        return 0
    return size


def HashMapElement_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    data = valobj.GetChildMemberWithName('data')
    key = data.GetChildMemberWithName('key')
    value = data.GetChildMemberWithName('value')
    # check if either key or value are basic types
    key_summary = key.GetSummary()
    value_summary = value.GetSummary()
    
    return "key = {0}, value = {1}".format(key_summary if key_summary else get_numeric_string(key), value_summary if value_summary else get_numeric_string(value))
class HashMap_SyntheticProvider:
    def __init__(self, valobj : lldb.SBValue, internal_dict):
            self.valobj: lldb.SBValue = valobj

    def num_children(self):
        return self.valobj.GetChildMemberWithName('num_elements').GetValueAsUnsigned()

    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return None
    def get_child_at_index(self,index):
        if index < 0:
            return None
        if index >= self.num_children():
            return None
        if self.valobj.IsValid() == False:
            return None
        try:
            # linked list, get head_element
            element: lldb.SBValue = self.valobj.GetChildMemberWithName('head_element')
            elements: lldb.SBValue = self.valobj.GetChildMemberWithName('elements')
            data_size = elements.GetType().GetByteSize()
            thing = index
            for i in range(thing):
                element = element.GetChildMemberWithName('next')
                    
            # return elements.CreateChildAtOffset('[' + str(index) + ']', index * data_size, element.GetType())
            return element.CreateValueFromData('[' + str(index) + ']', element.GetData(), element.GetType())
        except:
            return None

class Dictionary_SyntheticProvider:
    def __init__(self, valobj, internal_dict):
            self.valobj = valobj

    def num_children(self):
        _p = self.valobj.GetChildMemberWithName('_p')
        if (_p.GetValueAsUnsigned() == 0):
            return 0
        return _p.GetChildMemberWithName('variant_map').GetChildMemberWithName('num_elements').GetValueAsUnsigned()
    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return None
    def get_child_at_index(self,index):
        if index < 0:
            return None
        if index >= self.num_children():
            return None
        if self.valobj.IsValid() == False:
            return None
        try:
            _p = self.valobj.GetChildMemberWithName('_p')
            variant_map = _p.GetChildMemberWithName('variant_map')
            return HashMap_SyntheticProvider(variant_map, None).get_child_at_index(index)
        except:
            return None
    

def Vector_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    if (valobj.IsSynthetic()):
        return Vector_SyntheticProvider(valobj.GetNonSyntheticValue(), internal_dict).get_summary()
    else:
        return Vector_SyntheticProvider(valobj, internal_dict).get_summary()

class List_SyntheticProvider:
    def __init__(self, valobj: lldb.SBValue, internal_dict):
            self.valobj = valobj
    
    def num_children(self):
        _data = self.valobj.GetChildMemberWithName('_data')
        if (_data.GetValueAsUnsigned() == 0):
            return 0
        return _data.GetChildMemberWithName('size_cache').GetValueAsUnsigned()
    def get_child_index(self,name):
        try:
            return int(name.lstrip('[').rstrip(']'))
        except:
            return None
    def get_child_at_index(self,index):
        if index < 0:
            return None
        if index >= self.num_children():
            return None
        if self.valobj.IsValid() == False:
            return None
        try:
            _data = self.valobj.GetChildMemberWithName('_data')
            element: lldb.SBValue = _data.GetChildMemberWithName('first')
            if element.GetValueAsUnsigned() == 0:
                return None
            #linked list traversal
            thing = index
            for i in range(thing):
                element = element.GetChildMemberWithName('next_ptr')
                    
            # return elements.CreateChildAtOffset('[' + str(index) + ']', index * data_size, element.GetType())
            value = element.GetChildMemberWithName("value")
            return element.CreateValueFromData('[' + str(index) + ']', value.GetData(), value.GetType())

            return _ptr.CreateChildAtOffset('[' + str(index) + ']', index * elementSize, type)
        except:
            return None


class Vector_SyntheticProvider:
    def __init__(self, valobj: lldb.SBValue, internal_dict):
            self.valobj = valobj
            
    def get_summary(self):
        return "size = " + str(self.num_children())

    def num_children(self):
            try:
                    return getCowDataSize(self.valobj.GetChildMemberWithName('_cowdata'))
            except:
                    return 0
    def has_children(self):
            return True
    def get_child_index(self,name: str):
            try:
                    return int(name.lstrip('[').rstrip(']'))
            except:
                    return None

    def get_child_at_index(self,index):
            if index < 0:
                    return None
            if index >= self.num_children():
                    return None
            if self.valobj.IsValid() == False:
                    return None
            _ptr: lldb.SBValue = self.valobj.GetChildMemberWithName('_cowdata').GetChildMemberWithName('_ptr')
            if _ptr.GetValueAsUnsigned() == 0:
                    return None
            try:
                # vector is a templated argument
                # _cowdata._ptr is a pointer of the same type as the vector template
                # we need to get the type of the vector template
                type: lldb.SBType = self.valobj.GetType().GetTemplateArgumentType(0)
                elementSize = type.GetByteSize()
                return _ptr.CreateChildAtOffset('[' + str(index) + ']', index * elementSize, type)
            except:
                    return _ptr.CreateChildAtOffset()

class PackedStringArray_SyntheticProvider(Vector_SyntheticProvider):
    def __init__(self, valobj: lldb.SBValue, internal_dict):
            # just cast valobj to `Vector<::String>` and use the Vector_SyntheticProvider
            target = valobj.GetTarget()
            type: lldb.SBType = target.FindFirstType('::Vector<::String>')
            # super.__init__(valobj.Cast(type))
            self.valobj = valobj.Cast(type)
    def get_summary(self):
        return "FUCK!"

            
class PackedColorArray_SyntheticProvider(Vector_SyntheticProvider):
    def __init__(self, valobj: lldb.SBValue, internal_dict):
            # just cast valobj to `Vector<::Color>` and use the Vector_SyntheticProvider
            target = valobj.GetTarget()
            type: lldb.SBType = target.FindFirstType('::Vector<::Color>')
            super.__init__(valobj.Cast(type))
            
def PackedStringArray_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    typey = valobj.target.FindFirstType('Vector<String>')
    if (not typey):
        return "FUCK"
    return valobj.target.FindFirstType('Vector<String>').GetDisplayTypeName()

    if (valobj.IsSynthetic()):
        return PackedStringArray_SyntheticProvider(valobj.GetNonSyntheticValue(), internal_dict).get_summary()
    else:
        return PackedStringArray_SyntheticProvider(valobj, internal_dict).get_summary()

def PackedColorArray_SummaryProvider(valobj: lldb.SBValue, internal_dict):
    if (valobj.IsSynthetic()):
        return PackedColorArray_SyntheticProvider(valobj.GetNonSyntheticValue(), internal_dict).get_summary()
    else:
        return PackedColorArray_SyntheticProvider(valobj, internal_dict).get_summary()
