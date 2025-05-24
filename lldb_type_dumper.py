import inspect
from typing import Any
from enum import Enum
import types

def __LLDB_DUMPER():
    PRINT_DOC_STRINGS = False
    ENUM_DICT : dict[str, list[str]] = {
    "StateType": [
        "eStateInvalid",
        "kLastStateType",
    ],
    "LaunchFlags": [
        "eLaunchFlagNone",
        "eLaunchFlagInheritTCCFromParent",
    ],
    "RunMode": [
        "eOnlyThisThread",
        "eOnlyDuringStepping",
    ],
    "ByteOrder": [
        "eByteOrderInvalid",
        "eByteOrderLittle",
    ],
    "Encoding": [
        "eEncodingInvalid",
        "eEncodingVector",
    ],
    "Format": [
        "eFormatDefault",
        "kNumFormats",
    ],
    "DescriptionLevel": [
        "eDescriptionLevelBrief",
        "kNumDescriptionLevels",
    ],
    "ScriptLanguage": [
        "eScriptLanguageNone",
        "eScriptLanguageDefault",
    ],
    "RegisterKind": [
        "eRegisterKindEHFrame",
        "kNumRegisterKinds",
    ],
    "StopReason": [
        "eStopReasonInvalid",
        "eStopReasonVForkDone",
    ],
    "ReturnStatus": [
        "eReturnStatusInvalid",
        "eReturnStatusQuit",
    ],
    "ExpressionResults": [
        "eExpressionCompleted",
        "eExpressionUnrecognizedOpcode",
    ],
    "SearchDepth": [
        "eSearchDepthTarget",
        "eSearchDepthDefault",
    ],
    "ConnectionStatus": [
        "eConnectionStatusSuccess",
        "eConnectionStatusInterrupted",
    ],
    "ErrorType": [
        "eErrorTypeInvalid",
        "eErrorTypeWin32",
    ],
    "ValueType": [
        "eValueTypeInvalid",
        "eValueTypeVTableEntry",
    ],
    "InputReaderGranularity": [
        "eInputReaderGranularityInvalid",
        "eInputReaderGranularityAll",
    ],
    "SymbolContextItem": [
        "eSymbolContextTarget",
        "eSymbolContextLastItem",
    ],
    "Permissions": [
        "ePermissionsWritable",
        "ePermissionsExecutable",
    ],
    "InputReaderAction": [
        "eInputReaderActivate",
        "eInputReaderDone",
    ],
    "BreakpointEventType": [
        "eBreakpointEventTypeInvalidType",
        "eBreakpointEventTypeAutoContinueChanged",
    ],
    "WatchpointEventType": [
        "eWatchpointEventTypeInvalidType",
        "eWatchpointEventTypeTypeChanged",
    ],
    "WatchpointWriteType": [
        "eWatchpointWriteTypeDisabled",
        "eWatchpointWriteTypeOnModify",
    ],
    "LanguageType": [
        "eLanguageTypeUnknown",
        "eNumLanguageTypes",
    ],
    "InstrumentationRuntimeType": [
        "eInstrumentationRuntimeTypeAddressSanitizer",
        "eNumInstrumentationRuntimeTypes",
    ],
    "DynamicValueType": [
        "eNoDynamicValues",
        "eDynamicDontRunTarget",
    ],
    "StopShowColumn": [
        "eStopShowColumnAnsiOrCaret",
        "eStopShowColumnNone",
    ],
    "AccessType": [
        "eAccessNone",
        "eAccessPackage",
    ],
    "CommandArgumentType": [
        "eArgTypeAddress",
        "eArgTypeLastArg",
    ],
    "SymbolType": [
        "eSymbolTypeAny",
        "eSymbolTypeReExported",
    ],
    "SectionType": [
        "eSectionTypeInvalid",
        "eSectionTypeSwiftModules",
    ],
    "EmulateInstructionOptions": [
        "eEmulateInstructionOptionNone",
        "eEmulateInstructionOptionIgnoreConditions",
    ],
    "FunctionNameType": [
        "eFunctionNameTypeNone",
        "eFunctionNameTypeAny",
    ],
    "BasicType": [
        "eBasicTypeInvalid",
        "eBasicTypeOther",
    ],
    "TraceType": [
        "eTraceTypeNone",
        "eTraceTypeProcessorTrace",

    ],
    "StructuredDataType": [
        "eStructuredDataTypeInvalid",
        "eStructuredDataTypeUnsignedInteger",
    ],
    "TypeClass": [
        "eTypeClassInvalid",
        "eTypeClassAny",
    ],
    "TemplateArgumentKind": [
        "eTemplateArgumentKindNull",
        "eTemplateArgumentKindNullPtr",
    ],
    "FormatterMatchType": [
        "eFormatterMatchExact",
        "eLastFormatterMatchType",
    ],
    "TypeOptions": [
        "eTypeOptionNone",
        "eTypeOptionFrontEndWantsDereference",
    ],
    "FrameComparison": [
        "eFrameCompareInvalid",
        "eFrameCompareOlder",
    ],
    "FilePermissions": [
        "eFilePermissionsUserRead",
        "eFilePermissionsDirectoryDefault",
    ],
    "QueueItemKind": [
        "eQueueItemKindUnknown",
        "eQueueItemKindBlock",
    ],
    "QueueKind": [
        "eQueueKindUnknown",
        "eQueueKindConcurrent",
    ],
    "ExpressionEvaluationPhase": [
        "eExpressionEvaluationParse",
        "eExpressionEvaluationComplete",
    ],
    "InstructionControlFlowKind": [
        "eInstructionControlFlowKindUnknown",
        "eInstructionControlFlowKindFarJump",
    ],
    "WatchpointKind": [
        "eWatchpointKindWrite",
        "eWatchpointKindRead",

    ],
    "GdbSignal": [
        "eGdbSignalBadAccess",
        "eGdbSignalBreakpoint",
    ],
    "PathType": [
        "ePathTypeLLDBShlibDir",
        "ePathTypeClangDir",
    ],
    "MemberFunctionKind": [
        "eMemberFunctionKindUnknown",
        "eMemberFunctionKindStaticMethod",

    ],
    "MatchType": [
        "eMatchTypeNormal",
        "eMatchTypeStartsWith",
    ],
    "TypeFlags": [
        "eTypeHasChildren",
        "eTypeInstanceIsPointer",
    ],
    "CommandFlags": [
        "eCommandRequiresTarget",
        "eCommandProcessMustBeTraced",
    ],
    "TypeSummaryCapping": [
        "eTypeSummaryCapped",
        "eTypeSummaryUncapped",

    ],
    "CommandInterpreterResult": [
        "eCommandInterpreterResultSuccess",
        "eCommandInterpreterResultQuitRequested",
    ],
    "SaveCoreStyle": [
        "eSaveCoreUnspecified",
        "eSaveCoreStackOnly",
    ],
    "TraceEvent": [
        "eTraceEventDisabledSW",
        "eTraceEventSyncPoint",
    ],
    "TraceItemKind": [
        "eTraceItemKindError",
        "eTraceItemKindInstruction",
    ],
    "TraceCursorSeekType": [
        "eTraceCursorSeekTypeBeginning",
        "eTraceCursorSeekTypeEnd",
    ],
    "DWIMPrintVerbosity": [
        "eDWIMPrintVerbosityNone",
        "eDWIMPrintVerbosityFull",
    ],
    "WatchpointValueKind": [
        "eWatchPointValueKindInvalid",
        "eWatchPointValueKindExpression",
    ],
    "CompletionType": [
        "eNoCompletion",
        "eCustomCompletion",
    ],
    }

    FLAG_TYPE_ENUMS = [
        "LaunchFlags"
        "ByteOrder"
        "SymbolContextItem"
        "Permissions"
        "BreakpointEventType"
        "WatchpointEventType"
        "EmulateInstructionOptions"
        "FunctionNameType"
        "TypeClass"
        "TypeOptions"
        "FilePermissions"
        "WatchpointKind"
        "TypeFlags"
        "CommandFlags"
        "CompletionType"
    ]
    INT_TYPES= [
        'size_t',
        'char',
        'int',
        'int8_t',
        'int16_t',
        'int32_t',
        'int64_t',
        'uint8_t',
        'uint16_t',
        'uint32_t',
        'uint64_t',
        
        'size_t const',
        'char const',
        'int const',
        'int8_t const',
        'int16_t const',
        'int32_t const',
        'int64_t const',
        'uint8_t const',
        'uint16_t const',
        'uint32_t const',
        'uint64_t const',
        
        'size_t &',
        'char &',
        'int &',
        'int8_t &',
        'int16_t &',
        'int32_t &',
        'int64_t &',
        'uint8_t &',
        'uint16_t &',
        'uint32_t &',
        'uint64_t &',
        
        'lldb::addr_t',
        'lldb::pid_t',
        'lldb::break_id_t',
        'lldb::tid_t',
        'lldb::offset_t',
        'lldb::user_id_t',
        'lldb::pid_t const',
        'lldb::watch_id_t',
        'lldb::cpu_id_t',
        
        'bytes_read',
        'written_read'
    ]

    INT_LIST_TYPES = [
        'int32_t *',
        'int64_t *',
        'uint32_t *',
        'uint64_t *',
        'int32_t const *',
        'int64_t const *',
        'uint32_t const *',
        'uint64_t const *',
        'const int32_t *',
        'const int64_t *',
        'const uint32_t *',
        'const uint64_t *',
    ]

    BOOL_TYPES = [
        'bool',
        'bool const',
        'const bool',
        'bool &',
    ]
    FLOAT_TYPES = [
        'double',
        'float',
        'long double',

        'double const',
        'float const',
        'long double const',
        'const double',
        'const float',
        'const long double',
        'double &',
        'float &',
        'long double &',
        
    ]
    FLOAT_LIST_TYPES = [
        'double *',
        'float *',
        'long double *',
        'float const *',
        'double const *',
        'long double const *',
        'const double *',
        'const float *',
        'const long double *'
    ]

    STR_TYPES = [
        'char const *',
        'std::string',
        'const char *',
        'char *',
        'string'
    ]

    STR_LIST_TYPES = [
        'std::vector<std::string>',
        'std::vector<char const *>',
        'std::vector<char *>',
        'char const **'
    ]
    BYTES_TYPES = [
        'uint8_t const *',
        'void *',
        'void const *'
    ]

    REMOVE_TYPES = [ # no equivalent in python, would be an `object` type but we'll just remove them
        'lldb::thread_t',
        'lldb::thread_func_t',
        'lldb::thread_result_t *'
    ]

    FUNCTION_TYPES: dict[str, str] = {
        'lldb::SBCommunication::ReadThreadBytesReceived': 'Callable[[any, any, int], None]',
        'lldb::SBPlatformLocateModuleCallback': 'Callable[[any, SBModuleSpec, SBFileSpec, SBFileSpec], SBError]',
        'lldb::LogOutputCallback': 'Callable[[str, any], None]',
        'lldb::SBDebuggerDestroyCallback': 'Callable[[int, any], None]'
    }

    RETURN_TYPE_OVERRIDE_MAP: dict[str, str] = {
        "GetSummary": "str",
    }

    CLASS_FUNCTION_DECL_MAP: dict[str, str] = {
        'SBCommunication': 'ReadThreadBytesReceived = Callable[[Any, Any, int], None]'
    }

    def __is_relevant(obj):
        """Filter for the inspector to filter out non user defined functions/classes"""
        if hasattr(obj, '__name__'):
            if obj.__name__ == 'type':
                return False

        if inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismethod(obj) or isinstance(obj, property):
            return True

    def format_docstring(doc:str, indent = 0):
        """Format the docstring for printing"""
        if not doc or not doc.strip():
            return ''
        indent_str = '    ' * indent
        if not '\n' in doc:
            return indent_str + f"'''{doc}'''"

        prefix = indent_str + '"""\n'
        suffix = '\n' +indent_str + '"""\n'
        return prefix + '    ' * indent + doc.replace('\n', '\n' + '    ' * indent) + suffix

    def __process_function_doc_strings(obj_name, doc:str):
        # remove all the lines that don't begin with the obj_name or "Returns"
        if not doc:
            return None
        lines = []
        for line in doc.split('\n'):
            if line.startswith(obj_name + "("):
                lines.append(line)
        return '\n'.join(lines)

    non_lldb_types: list[str] = []
    lldb_types = []
    lldb_typedefs = []
    SBTypes = []
    failed_types = []
    enum_start_to_type_map :dict[str, str] = {}
    enum_defs: dict[str, list[str]] = {}

    def get_python_type(arg_type: str):
        if not arg_type:
            return ''

        if ',' in arg_type:
            arg_types = arg_type.split(',')
            new_arg_types = []
            for arg_type in arg_types:
                new_arg_types.append(get_python_type(arg_type.strip()))
            return "tuple[" +  ', '.join(new_arg_types) + ']'
        if arg_type.startswith('lldb::'):
            if arg_type.strip(" *").replace(" const","").strip().endswith('_t'):
                if not arg_type in lldb_typedefs:
                    lldb_typedefs.append(arg_type)
            else:
                if not arg_type in lldb_types:
                    lldb_types.append(arg_type)
        elif arg_type.startswith('SB'):
            if not arg_type in SBTypes:
                SBTypes.append(arg_type)
        else:
            if not arg_type in non_lldb_types:
                non_lldb_types.append(arg_type)

        if arg_type in INT_TYPES:
            arg_type = 'int'
        elif arg_type in INT_LIST_TYPES:
            arg_type = 'list[int]'
        elif arg_type in STR_TYPES:
            arg_type= 'str'
        elif arg_type in STR_LIST_TYPES:
            arg_type= 'list[str]'
        elif arg_type in FLOAT_LIST_TYPES:
            arg_type= 'list[float]'
        elif arg_type in FLOAT_TYPES:
            arg_type= 'float'
        elif arg_type in BYTES_TYPES:
            arg_type= 'bytes'
        elif arg_type in BOOL_TYPES:
            arg_type= 'bool'
        elif arg_type in REMOVE_TYPES:
            arg_type= ''
        elif arg_type in FUNCTION_TYPES:
            arg_type = FUNCTION_TYPES[arg_type]
        elif arg_type.startswith('lldb::'):
            arg_type= arg_type[6:].removesuffix(' const').removesuffix(' &').removesuffix(' const').strip().replace('::', '.')
        else:
            if not arg_type.startswith('SB'):
                failed_types.append(arg_type)
        if arg_type in ENUM_DICT:
            # TODO: eventually get enums working
            # arg_type = arg_type + '.value'
            arg_type = 'int'

        return arg_type.strip()

    class ArgDef:
        def __init__(self, name:str, type:str , default_val: str = None):
            self.name = name
            self.type:str = type
            self.default_val:str = default_val
        def __str__(self):
            ret_str = f"{self.name}"
            if self.type:
                ret_str += f": {self.type}"
            if self.default_val:
                ret_str += f" = {self.default_val}"
            return ret_str
    class FunctionStub:
        def __init__(self, name: str, args: list[ArgDef], return_type: str, docString: str = "", is_static: bool = False, is_class_method: bool = False):
            self.name = name
            self.args = args
            self.return_type = return_type
            self.docString = docString
            self.is_static = is_static
            self.is_class_method = is_class_method
        def get_string(self, indent = 1):
            indent_str = "    " * indent
            ret_str = indent_str + f"def {self.name}({', '.join([str(arg) for arg in self.args])})" + (f" -> {self.return_type}: ..." if self.return_type else ": ...")
            if PRINT_DOC_STRINGS and self.docString and self.docString.strip():
                ret_str += '\n'+ format_docstring(self.docString, indent)
            if self.is_static:
                ret_str = indent_str+ "@staticmethod\n" + ret_str
            elif self.is_class_method:
                ret_str = indent_str + "@classmethod\n" + ret_str
            return ret_str
        def __str__(self):
            return self.get_string()

    class PropertyStub:
        def __init__(self, name: str, type: str, getter: str, setter: str, deleter: str, docString: str = ""):
            self.name = name
            self.type = type
            self.getter = getter
            self.setter = setter
            self.deleter = deleter
            self.docString = docString
        def get_string(self, indent = 1):
            indent_str = "    " * indent
            ret_str = indent_str + "@property\n"
            ret_str += indent_str + f"def {self.name}(self)" + (f" -> {self.type}: ..." if self.type else ": ...")
            if PRINT_DOC_STRINGS and self.docString and self.docString.strip():
                ret_str += '\n' + format_docstring(self.docString, indent)
            if self.setter:
                ret_str += f"\n{indent_str}@{self.name}.setter\n"
                ret_str += indent_str + f"def {self.name}(self, value{(':' + self.type) if self.type else ''}): ..."
            return ret_str
        def __str__(self):
            return self.get_string()

    class ClassStub:
        def __init__(self, name: str, functions: list[FunctionStub], properties: list[PropertyStub], child_classes: list, parent_class: str = None, docString: str = ""):
            self.name = name
            self.functions = functions
            self.properties = properties
            self.child_classes: list[ClassStub] = child_classes
            self.parent_class = parent_class
            self.docString = docString
        def get_string(self, indent = 0):
            indent_str = "    " * indent
            ret_str: str = indent_str + f"class {self.name}({self.parent_class}):"
            if PRINT_DOC_STRINGS and self.docString and self.docString.strip():
                ret_str += '\n' + format_docstring(self.docString, indent + 1)
            for child_class in self.child_classes:
                ret_str += '\n' + child_class.get_string(indent + 1)
            for func in self.functions:
                ret_str += '\n' + func.get_string(indent + 1)
            for prop in self.properties:
                ret_str += '\n' + prop.get_string(indent + 1)
            if not '\n' in ret_str:
                ret_str += '\n' + "    " * (indent+1) + 'pass'
            return ret_str
        def __str__(self):
            return self.get_string()
    class_map: dict[str, ClassStub] = {}
    global_func_map: dict[str, FunctionStub] = {}
    def generate_function_stubs_from_docstrings(class_name, function_name, obj, doc: str, indent = 0) -> list[FunctionStub]:
        """
        The docstrings now look like this:
        EvaluateExpression(SBValue self, char const * expr) -> SBValue
        EvaluateExpression(SBValue self, char const * expr, SBExpressionOptions options) -> SBValue
        EvaluateExpression(SBValue self, char const * expr, SBExpressionOptions options, char const * name) -> SBValue
        
        Given the above, we need to make them look like this:
        def EvaluateExpression(self, expr: str) -> SBValue: ...
        def EvaluateExpression(self, expr: str, options: SBExpressionOptions) -> SBValue: ...
        def EvaluateExpression(self, expr: str, options: SBExpressionOptions, name: str) -> SBValue: ...
        """
        new_doc = __process_function_doc_strings(function_name, doc)
        func_defs:list[FunctionStub] = []
        if not new_doc:
            return []
        lines = new_doc.split('\n')
        lines_to_remove = []
        for line in lines:
            if '(make an event that contains a C string)' in line:
                for l in line.split('(make an event that contains a C string)'):
                    lines.append(l.strip())
                    # remove the original line
                lines_to_remove.append(line)
            elif line == '':
                lines_to_remove.append(line)
        for line in lines_to_remove:
            lines.remove(line)
        # for line in lines:
        #     # remove the line from the docstring
        #     doc = doc.replace(line.strip(), '')
        doc = doc.strip()
        for line in lines:
            # split the line into the function signature and the return type
            comps = line.split(' -> ')
            if len(comps) == 1:
                return_type = ''
            else:
                return_type = get_python_type(comps[1])
            if function_name in RETURN_TYPE_OVERRIDE_MAP:
                return_type = RETURN_TYPE_OVERRIDE_MAP[function_name]
            # TODO: figure out a way to handle varargs gracefully; right now all we do is just get the return_type then call the other function to get the arg types
            if (len(lines) > 1):
                func_def = get_function_def_from_inspector(class_name, obj, function_name, indent)
                func_def.return_type = return_type
                func_defs.append(func_def)
                return func_defs

            signature = comps[0]
            # split the signature into the function name and the arguments
            new_function_name, arg_block = signature.split('(')
            if new_function_name != function_name:
                print(f'function name {new_function_name} does not match {function_name}')
            elif not function_name:
                print('function name is empty')
            arg_block = arg_block.strip(')').strip('):')
            # split the arguments into individual arguments
            args = arg_block.split(', ')
            new_args = []
            arg_defs = []
            for i, arg in enumerate(args):
                # split the argument into the type and the name
                arg_components = arg.split(' ')
                arg_name = arg_components[-1]
                default_val = None
                # check if the arg_name has a default value
                # combine the rest back into thet ype
                arg_type = get_python_type(' '.join(arg_components[:-1]))
                if '=' in arg_name:
                    arg_name, default_val = arg_name.split('=')
                if default_val:
                    if default_val.startswith('e') or default_val.startswith('k'):
                        # check the enum dict to see if the default value is in there
                        # TODO: eventually get enums working
                        # for enum_name, enum_values in enum_defs.items():
                        # if default_val in enum_values:
                        # default_val = enum_name + '.' + default_val + '.value'
                        pass
                    if arg_type == 'int':
                        # remove the 'U' from the default value
                        default_val = default_val.strip('LL').strip('U')
                arg_defs.append(ArgDef(arg_name, arg_type, default_val))
            func_def = FunctionStub(function_name, arg_defs, return_type, doc)
            func_defs.append(func_def)

        # check if we can compress the function defs into one
        # if len(func_defs) > 1:
        #     """
        #         usually the case is something like this::
        #         def GetChildAtIndex(self: SBValue, idx: int) -> SBValue: ...
        #         def GetChildAtIndex(self: SBValue, idx: int, use_dynamic: int, can_create_synthetic: bool) -> SBValue: ...
        #         def GetChildMemberWithName(self: SBValue, name: str) -> SBValue: ...
        #         def GetChildMemberWithName(self: SBValue, name: str, use_dynamic: int) -> SBValue: ...

        #         if their argument names match, then we can compress them into one function, by setting the default values for the extra arguments to `None`:
        #         def GetChildAtIndex(self: SBValue, idx: int, use_dynamic: int = None, can_create_synthetic: bool = None) -> SBValue: ...
        #         def GetChildMemberWithName(self: SBValue, name: str, use_dynamic: int = None) -> SBValue: ...
        #     """
        #     to_remove = []
        #     for i, func_def in enumerate(func_defs):
        #         if i in to_remove:
        #             continue
        #         for j, other_func_def in enumerate(func_defs):
        #             if i == j or j in to_remove:
        #                 continue
        #             if func_def.name == other_func_def.name:
        #                 # get the shorter and longer arg lists
        #                 shorter_func_def_index: int
        #                 if (len(func_def.args) < len(other_func_def.args)):
        #                     shorter_func_def_index = i
        #                 else:
        #                     shorter_func_def_index = j
        #                 try:
        #                     shorter_func_def = func_defs[shorter_func_def_index]
        #                 except Exception as e:
        #                     print(f'func_defs length = {len(func_defs)}, shorter_func_def_index = {shorter_func_def_index}, i = {i}, j = {j}, func_def = {func_def}, other_func_def = {other_func_def}')
        #                     raise e
        #                 longer_func_def = func_def if len(func_def.args) > len(other_func_def.args) else other_func_def
        #                 if len(shorter_func_def.args) == len(longer_func_def.args):
        #                     continue
        #                 diff = len(longer_func_def.args) - len(shorter_func_def.args)
        #                 # check if the shorter list is a subset of the longer list
        #                 is_subset = True
        #                 for argidx, arg in enumerate(shorter_func_def.args):
        #                     if arg.name != longer_func_def.args[argidx].name:
        #                         is_subset = False
        #                         break
        #                 if not is_subset:
        #                     continue
        #                 # we add the `None` default values to the longer list
        #                 # print('adding default values ', diff)
        #                 for argidx in range(len(longer_func_def.args) - diff, len(longer_func_def.args)):
        #                     if longer_func_def.name == 'CreateValueFromExpression':
        #                         print(f'adding None to {longer_func_def.args[argidx].name}')
        #                         print(f'diff = {diff}, argidx = {argidx}, len(longer_func_def.args) = {len(longer_func_def.args)}, len(shorter_func_def.args) = {len(shorter_func_def.args)}')
        #                     # print(f'adding None to {longer_func_def.args[argidx].name}')
        #                     if not longer_func_def.args[argidx].type.startswith('Optional'):
        #                         longer_func_def.args[argidx].type = 'Optional[' + longer_func_def.args[argidx].type + ']'
        #                     longer_func_def.args[argidx].default_val = 'None'
        #                 # we remove the shorter list from the function defs
        #                 to_remove.append(shorter_func_def_index)
        #     func_defs = [func_def for i, func_def in enumerate(func_defs) if i not in to_remove]
        return func_defs

    ANY_OBJECTS = [
        "ScriptObjectPtr",
        "FileSP"
    ]

    def create_enum_typings(module):
        for enum_name, enum_values in ENUM_DICT.items():
            enum_start_to_type_map[enum_values[0]] = enum_name
            enum_defs[enum_name] = []

        source = inspect.getsource(module)
        source_lines = source.split('\n')
        start_index = 0
        for i, line in enumerate(source_lines):
            # we have to continue until we find the start of the enum defs
            # we will know it because there will be a line with no white space at the start, and starts with the letter 'e' followed immediately by an uppercase letter
            if line.strip() == '':
                continue
            if line[0] == 'e' and line[1].isupper():
                start_index = i
                break
        # now we have the start index, we can start processing the enum defs
        current_enum_type = ''
        for i in range(start_index, len(source_lines)):
            line = source_lines[i]
            if line.strip() == '':
                continue
            if line.startswith('class SB'):
                # we've reached the end
                break
            # we use the enum_start_to_type_map to get the type of the enum
            enum_decl = line.split('=')[0].strip()
            if enum_decl in enum_start_to_type_map:
                current_enum_type = enum_start_to_type_map[enum_decl]
                enum_defs[current_enum_type] = []
            enum_defs[current_enum_type].append(line.split('=')[0].strip())
        return enum_defs

    def create_enum_typings_file(module):
        enum_defs = create_enum_typings(module)
        enum_str = 'from enum import Enum\n\n' + 'import lldb' + '\n\n'
        """
        enum types are like this:
        ```
        class StateType(Enum):
            eStateInvalid = lldb.eStateInvalid
            eStateUnloaded = lldb.eStateUnloaded
            eStateConnected = lldb.eStateConnected
        ```
        if the enum type is in FLAG_TYPE_ENUMS, then we need to add the IntFlag mixin, like so:
        ```
        class LaunchFlags(IntFlag):
            eLaunchFlagNone = lldb.eLaunchFlagNone
            eLaunchFlagExec = lldb.eLaunchFlagExec
            eLaunchFlagDebug = lldb.eLaunchFlagDebug
        ```
        """
        for enum_name, enum_values in enum_defs.items():
            if len(enum_values) == 0:
                continue
            if enum_name in FLAG_TYPE_ENUMS:
                enum_str += f'class {enum_name}(IntFlag):\n'
            else:
                enum_str += f'class {enum_name}(Enum):\n'
            for enum_value in enum_values:
                enum_str += f'    {enum_value} = lldb.{enum_value}\n'
            enum_str += '\n'
        return enum_str

    def write_enum_typings_file(module):
        enum_str = create_enum_typings_file(module)
        import os
        # save it to /Users/nikita/Workspace/lldb-qt-formatters/test.py
        __directory =  os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(__directory, "typings", 'lldb_enums.pyi'), 'w') as f:
            f.write(enum_str)
            f.close()

    def get_preamble():
        return_str = 'from lldb_enums import *\nfrom typing import Any, Callable, List, Tuple, Optional\n\n\n'
        # get every single enum value that we have and declare it like `enum_value: int`
        for enum_name, enum_values in enum_defs.items():
            return_str += f"\n# {enum_name} enums:\n"
            for enum_value in enum_values:
                return_str += f"{enum_value}: int\n"
        return_str += '\nSBPlatformLocateModuleCallback = Callable[[Any, SBModuleSpec, SBFileSpec, SBFileSpec], SBError]\n\n'
        return_str += 'LogOutputCallback = Callable[[str, Any], None]\n\n'
        return_str += 'SBDebuggerDestroyCallback = Callable[[int, Any], None]\n\n'
        format_str = 'class {0}(object):\n    pass\n\n'
        for obj in ANY_OBJECTS:
            return_str += format_str.format(obj)
        return return_str

    def dump_class(child, indent = 0) -> ClassStub:
        attrs = inspect.classify_class_attrs(child[1])
        # for attr in attrs:
        #     if attr.kind == 'data':
        #         print(attr)
        doc = inspect.getdoc(child[1])
        # get the parent class, if any
        inspect.getclasstree([child[1]])
        class_name = child[0]
        parent_classes = inspect.getclasstree([child[1]])
        # get the last parent class
        parent_class = parent_classes[-1][-1][-1][0]
        # print(f'class_name = {class_name}')
        # print(f'parent_classes = {parent_classes}')
        # print(f'parent_class = {parent_class}')
        # print()
        class_def = ClassStub(class_name, [], [], [], str(parent_class.__name__), doc)
        for grandchild in inspect.getmembers(child[1], __is_relevant):
            # check if it is a function
            if inspect.isfunction(grandchild[1]) or inspect.ismethod(grandchild[1]):
                class_def.functions.extend(dump_class_function(child[0], grandchild, indent + 1))
            elif inspect.isclass(grandchild[1]):
                child_class = dump_class(grandchild, indent + 1)
                class_def.child_classes.append(child_class)
            else:
                if isinstance(grandchild[1], property):
                    prop: property = grandchild[1]
                    prop_doc = inspect.getdoc(prop)
                    getter = prop.fget.__name__ if prop.fget else None
                    setter = prop.fset.__name__ if prop.fset else None
                    deleter = prop.fdel.__name__ if prop.fdel else None
                    prop = PropertyStub(grandchild[0], None, getter, setter, deleter, prop_doc)
                    class_def.properties.append(prop)
                    # print(grandchild[0], str(grandchild[1]))
        for function in class_def.functions:
            # now we need to check if the function is a static method or a class method
            for attr in attrs:
                if attr.name == function.name:
                    if attr.kind == 'static method':
                        function.is_static = True
                    elif attr.kind == 'class method':
                        function.is_class_method = True
        # now, we need to get the proper types for the properties by cross referencing the property getter with the return type of the function
        for proper in class_def.properties:
            if proper.getter:
                # find the function that matches the getter in the class_map
                for func in class_def.functions:
                    if func.name == proper.getter:
                        proper.type = func.return_type
                # print(f"Property {proper.name} has type {proper.type}")
        return class_def
    def get_function_def_from_inspector(class_name, obj, name, indent = 0):
        """Get the function signature"""
        args = inspect.getfullargspec(obj)
        defaults = args.defaults
        arg_defs = []
        for i, arg in enumerate(args.args):
            arg_name = arg
            arg_type = ''
            default_val = None
            if defaults:
                if i > len(args.args) - len(defaults):
                    default_val = defaults[i - (len(args.args) - len(defaults))]

            arg_defs.append(ArgDef(arg_name, arg_type, default_val))
        # check for var args
        if args.varargs:
            arg_defs.append(ArgDef('*' + args.varargs, ''))
        func_def : FunctionStub = FunctionStub(name, arg_defs, '', inspect.getdoc(obj))
        return func_def

    def dump_class_function(class_name, grandchild, indent = 1) -> list[FunctionStub]:
        doc = inspect.getdoc(grandchild[1])
        funcs = []
        if doc:
            funcs = generate_function_stubs_from_docstrings(class_name, grandchild[0], grandchild[1], doc, indent)
        if len(funcs) == 0:
            funcs = [get_function_def_from_inspector(class_name, grandchild[1], grandchild[0], indent)]
        return funcs

    def create_typings_file(module):
        for child in inspect.getmembers(module, __is_relevant):
            if inspect.isclass(child[1]):
                class_map[child[0]] = dump_class(child)
            else:
                global_func_map[child[0]] = get_function_def_from_inspector("", child[1], child[0])

        # now throw that away
        return_str = get_preamble()
        for method in global_func_map.values():
            return_str += method.get_string(0) + "\n"
        return_str += "\n\n\n\n"
        for class_def in class_map.values():
            return_str += class_def.get_string(0) + "\n\n"
        return return_str

        return_str += "\n\n\n\n # All the non-lldb seen in the above functions:\n"
        for arg_type in non_lldb_types:
            return_str += f"# {arg_type}\n"

        return_str += "\n\n\n\n # All the lldb typedefs seen in the above functions:\n"
        for lldb_typedef in lldb_typedefs:
            return_str += f"# {lldb_typedef}\n"

        return_str += "\n\n\n\n # All the lldb types seen in the above functions:\n"
        for lldb_type in lldb_types:
            return_str += f"# {lldb_type}\n"

        return_str += "\n\n\n\n # All the types we didn't handle:\n"
        for failed_type in failed_types:
            return_str += f"# {failed_type}\n"
        return return_str

    def write_typing_file(module):
        import os
        # save it to /Users/nikita/Workspace/lldb-qt-formatters/test.py
        __directory =  os.path.dirname(os.path.realpath(__file__))
        print(__directory)
        with open(os.path.join(__directory, "typings", 'lldb.pyi'), 'w') as f:
            f.write(create_typings_file(module))
            f.close()

    import lldb
    write_enum_typings_file(lldb)
    write_typing_file(lldb)


__LLDB_DUMPER()
