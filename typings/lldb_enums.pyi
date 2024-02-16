from enum import Enum

import lldb

class StateType(Enum):
    eStateInvalid = lldb.eStateInvalid
    eStateUnloaded = lldb.eStateUnloaded
    eStateConnected = lldb.eStateConnected
    eStateAttaching = lldb.eStateAttaching
    eStateLaunching = lldb.eStateLaunching
    eStateStopped = lldb.eStateStopped
    eStateRunning = lldb.eStateRunning
    eStateStepping = lldb.eStateStepping
    eStateCrashed = lldb.eStateCrashed
    eStateDetached = lldb.eStateDetached
    eStateExited = lldb.eStateExited
    eStateSuspended = lldb.eStateSuspended
    kLastStateType = lldb.kLastStateType

class LaunchFlags(Enum):
    eLaunchFlagNone = lldb.eLaunchFlagNone
    eLaunchFlagExec = lldb.eLaunchFlagExec
    eLaunchFlagDebug = lldb.eLaunchFlagDebug
    eLaunchFlagStopAtEntry = lldb.eLaunchFlagStopAtEntry
    eLaunchFlagDisableASLR = lldb.eLaunchFlagDisableASLR
    eLaunchFlagDisableSTDIO = lldb.eLaunchFlagDisableSTDIO
    eLaunchFlagLaunchInTTY = lldb.eLaunchFlagLaunchInTTY
    eLaunchFlagLaunchInShell = lldb.eLaunchFlagLaunchInShell
    eLaunchFlagLaunchInSeparateProcessGroup = lldb.eLaunchFlagLaunchInSeparateProcessGroup
    eLaunchFlagDontSetExitStatus = lldb.eLaunchFlagDontSetExitStatus
    eLaunchFlagDetachOnError = lldb.eLaunchFlagDetachOnError
    eLaunchFlagShellExpandArguments = lldb.eLaunchFlagShellExpandArguments
    eLaunchFlagCloseTTYOnExit = lldb.eLaunchFlagCloseTTYOnExit
    eLaunchFlagInheritTCCFromParent = lldb.eLaunchFlagInheritTCCFromParent

class RunMode(Enum):
    eOnlyThisThread = lldb.eOnlyThisThread
    eAllThreads = lldb.eAllThreads
    eOnlyDuringStepping = lldb.eOnlyDuringStepping

class ByteOrder(Enum):
    eByteOrderInvalid = lldb.eByteOrderInvalid
    eByteOrderBig = lldb.eByteOrderBig
    eByteOrderPDP = lldb.eByteOrderPDP
    eByteOrderLittle = lldb.eByteOrderLittle

class Encoding(Enum):
    eEncodingInvalid = lldb.eEncodingInvalid
    eEncodingUint = lldb.eEncodingUint
    eEncodingSint = lldb.eEncodingSint
    eEncodingIEEE754 = lldb.eEncodingIEEE754
    eEncodingVector = lldb.eEncodingVector

class Format(Enum):
    eFormatDefault = lldb.eFormatDefault
    eFormatInvalid = lldb.eFormatInvalid
    eFormatBoolean = lldb.eFormatBoolean
    eFormatBinary = lldb.eFormatBinary
    eFormatBytes = lldb.eFormatBytes
    eFormatBytesWithASCII = lldb.eFormatBytesWithASCII
    eFormatChar = lldb.eFormatChar
    eFormatCharPrintable = lldb.eFormatCharPrintable
    eFormatComplex = lldb.eFormatComplex
    eFormatComplexFloat = lldb.eFormatComplexFloat
    eFormatCString = lldb.eFormatCString
    eFormatDecimal = lldb.eFormatDecimal
    eFormatEnum = lldb.eFormatEnum
    eFormatHex = lldb.eFormatHex
    eFormatHexUppercase = lldb.eFormatHexUppercase
    eFormatFloat = lldb.eFormatFloat
    eFormatOctal = lldb.eFormatOctal
    eFormatOSType = lldb.eFormatOSType
    eFormatUnicode16 = lldb.eFormatUnicode16
    eFormatUnicode32 = lldb.eFormatUnicode32
    eFormatUnsigned = lldb.eFormatUnsigned
    eFormatPointer = lldb.eFormatPointer
    eFormatVectorOfChar = lldb.eFormatVectorOfChar
    eFormatVectorOfSInt8 = lldb.eFormatVectorOfSInt8
    eFormatVectorOfUInt8 = lldb.eFormatVectorOfUInt8
    eFormatVectorOfSInt16 = lldb.eFormatVectorOfSInt16
    eFormatVectorOfUInt16 = lldb.eFormatVectorOfUInt16
    eFormatVectorOfSInt32 = lldb.eFormatVectorOfSInt32
    eFormatVectorOfUInt32 = lldb.eFormatVectorOfUInt32
    eFormatVectorOfSInt64 = lldb.eFormatVectorOfSInt64
    eFormatVectorOfUInt64 = lldb.eFormatVectorOfUInt64
    eFormatVectorOfFloat16 = lldb.eFormatVectorOfFloat16
    eFormatVectorOfFloat32 = lldb.eFormatVectorOfFloat32
    eFormatVectorOfFloat64 = lldb.eFormatVectorOfFloat64
    eFormatVectorOfUInt128 = lldb.eFormatVectorOfUInt128
    eFormatComplexInteger = lldb.eFormatComplexInteger
    eFormatCharArray = lldb.eFormatCharArray
    eFormatAddressInfo = lldb.eFormatAddressInfo
    eFormatHexFloat = lldb.eFormatHexFloat
    eFormatInstruction = lldb.eFormatInstruction
    eFormatVoid = lldb.eFormatVoid
    eFormatUnicode8 = lldb.eFormatUnicode8
    kNumFormats = lldb.kNumFormats

class DescriptionLevel(Enum):
    eDescriptionLevelBrief = lldb.eDescriptionLevelBrief
    eDescriptionLevelFull = lldb.eDescriptionLevelFull
    eDescriptionLevelVerbose = lldb.eDescriptionLevelVerbose
    eDescriptionLevelInitial = lldb.eDescriptionLevelInitial
    kNumDescriptionLevels = lldb.kNumDescriptionLevels

class ScriptLanguage(Enum):
    eScriptLanguageNone = lldb.eScriptLanguageNone
    eScriptLanguagePython = lldb.eScriptLanguagePython
    eScriptLanguageLua = lldb.eScriptLanguageLua
    eScriptLanguageUnknown = lldb.eScriptLanguageUnknown
    eScriptLanguageDefault = lldb.eScriptLanguageDefault

class RegisterKind(Enum):
    eRegisterKindEHFrame = lldb.eRegisterKindEHFrame
    eRegisterKindDWARF = lldb.eRegisterKindDWARF
    eRegisterKindGeneric = lldb.eRegisterKindGeneric
    eRegisterKindProcessPlugin = lldb.eRegisterKindProcessPlugin
    eRegisterKindLLDB = lldb.eRegisterKindLLDB
    kNumRegisterKinds = lldb.kNumRegisterKinds

class StopReason(Enum):
    eStopReasonInvalid = lldb.eStopReasonInvalid
    eStopReasonNone = lldb.eStopReasonNone
    eStopReasonTrace = lldb.eStopReasonTrace
    eStopReasonBreakpoint = lldb.eStopReasonBreakpoint
    eStopReasonWatchpoint = lldb.eStopReasonWatchpoint
    eStopReasonSignal = lldb.eStopReasonSignal
    eStopReasonException = lldb.eStopReasonException
    eStopReasonExec = lldb.eStopReasonExec
    eStopReasonPlanComplete = lldb.eStopReasonPlanComplete
    eStopReasonThreadExiting = lldb.eStopReasonThreadExiting
    eStopReasonInstrumentation = lldb.eStopReasonInstrumentation
    eStopReasonProcessorTrace = lldb.eStopReasonProcessorTrace
    eStopReasonFork = lldb.eStopReasonFork
    eStopReasonVFork = lldb.eStopReasonVFork
    eStopReasonVForkDone = lldb.eStopReasonVForkDone

class ReturnStatus(Enum):
    eReturnStatusInvalid = lldb.eReturnStatusInvalid
    eReturnStatusSuccessFinishNoResult = lldb.eReturnStatusSuccessFinishNoResult
    eReturnStatusSuccessFinishResult = lldb.eReturnStatusSuccessFinishResult
    eReturnStatusSuccessContinuingNoResult = lldb.eReturnStatusSuccessContinuingNoResult
    eReturnStatusSuccessContinuingResult = lldb.eReturnStatusSuccessContinuingResult
    eReturnStatusStarted = lldb.eReturnStatusStarted
    eReturnStatusFailed = lldb.eReturnStatusFailed
    eReturnStatusQuit = lldb.eReturnStatusQuit

class ExpressionResults(Enum):
    eExpressionCompleted = lldb.eExpressionCompleted
    eExpressionSetupError = lldb.eExpressionSetupError
    eExpressionParseError = lldb.eExpressionParseError
    eExpressionDiscarded = lldb.eExpressionDiscarded
    eExpressionInterrupted = lldb.eExpressionInterrupted
    eExpressionHitBreakpoint = lldb.eExpressionHitBreakpoint
    eExpressionTimedOut = lldb.eExpressionTimedOut
    eExpressionResultUnavailable = lldb.eExpressionResultUnavailable
    eExpressionStoppedForDebug = lldb.eExpressionStoppedForDebug
    eExpressionThreadVanished = lldb.eExpressionThreadVanished
    eSearchDepthInvalid = lldb.eSearchDepthInvalid

class SearchDepth(Enum):
    eSearchDepthTarget = lldb.eSearchDepthTarget
    eSearchDepthModule = lldb.eSearchDepthModule
    eSearchDepthCompUnit = lldb.eSearchDepthCompUnit
    eSearchDepthFunction = lldb.eSearchDepthFunction
    eSearchDepthBlock = lldb.eSearchDepthBlock
    eSearchDepthAddress = lldb.eSearchDepthAddress
    kLastSearchDepthKind = lldb.kLastSearchDepthKind

class ConnectionStatus(Enum):
    eConnectionStatusSuccess = lldb.eConnectionStatusSuccess
    eConnectionStatusEndOfFile = lldb.eConnectionStatusEndOfFile
    eConnectionStatusError = lldb.eConnectionStatusError
    eConnectionStatusTimedOut = lldb.eConnectionStatusTimedOut
    eConnectionStatusNoConnection = lldb.eConnectionStatusNoConnection
    eConnectionStatusLostConnection = lldb.eConnectionStatusLostConnection
    eConnectionStatusInterrupted = lldb.eConnectionStatusInterrupted

class ErrorType(Enum):
    eErrorTypeInvalid = lldb.eErrorTypeInvalid
    eErrorTypeGeneric = lldb.eErrorTypeGeneric
    eErrorTypeMachKernel = lldb.eErrorTypeMachKernel
    eErrorTypePOSIX = lldb.eErrorTypePOSIX
    eErrorTypeExpression = lldb.eErrorTypeExpression
    eErrorTypeWin32 = lldb.eErrorTypeWin32

class ValueType(Enum):
    eValueTypeInvalid = lldb.eValueTypeInvalid
    eValueTypeVariableGlobal = lldb.eValueTypeVariableGlobal
    eValueTypeVariableStatic = lldb.eValueTypeVariableStatic
    eValueTypeVariableArgument = lldb.eValueTypeVariableArgument
    eValueTypeVariableLocal = lldb.eValueTypeVariableLocal
    eValueTypeRegister = lldb.eValueTypeRegister
    eValueTypeRegisterSet = lldb.eValueTypeRegisterSet
    eValueTypeConstResult = lldb.eValueTypeConstResult
    eValueTypeVariableThreadLocal = lldb.eValueTypeVariableThreadLocal

class InputReaderGranularity(Enum):
    eInputReaderGranularityInvalid = lldb.eInputReaderGranularityInvalid
    eInputReaderGranularityByte = lldb.eInputReaderGranularityByte
    eInputReaderGranularityWord = lldb.eInputReaderGranularityWord
    eInputReaderGranularityLine = lldb.eInputReaderGranularityLine
    eInputReaderGranularityAll = lldb.eInputReaderGranularityAll

class SymbolContextItem(Enum):
    eSymbolContextTarget = lldb.eSymbolContextTarget
    eSymbolContextModule = lldb.eSymbolContextModule
    eSymbolContextCompUnit = lldb.eSymbolContextCompUnit
    eSymbolContextFunction = lldb.eSymbolContextFunction
    eSymbolContextBlock = lldb.eSymbolContextBlock
    eSymbolContextLineEntry = lldb.eSymbolContextLineEntry
    eSymbolContextSymbol = lldb.eSymbolContextSymbol
    eSymbolContextEverything = lldb.eSymbolContextEverything
    eSymbolContextVariable = lldb.eSymbolContextVariable
    eSymbolContextLastItem = lldb.eSymbolContextLastItem

class Permissions(Enum):
    ePermissionsWritable = lldb.ePermissionsWritable
    ePermissionsReadable = lldb.ePermissionsReadable
    ePermissionsExecutable = lldb.ePermissionsExecutable

class InputReaderAction(Enum):
    eInputReaderActivate = lldb.eInputReaderActivate
    eInputReaderAsynchronousOutputWritten = lldb.eInputReaderAsynchronousOutputWritten
    eInputReaderReactivate = lldb.eInputReaderReactivate
    eInputReaderDeactivate = lldb.eInputReaderDeactivate
    eInputReaderGotToken = lldb.eInputReaderGotToken
    eInputReaderInterrupt = lldb.eInputReaderInterrupt
    eInputReaderEndOfFile = lldb.eInputReaderEndOfFile
    eInputReaderDone = lldb.eInputReaderDone

class BreakpointEventType(Enum):
    eBreakpointEventTypeInvalidType = lldb.eBreakpointEventTypeInvalidType
    eBreakpointEventTypeAdded = lldb.eBreakpointEventTypeAdded
    eBreakpointEventTypeRemoved = lldb.eBreakpointEventTypeRemoved
    eBreakpointEventTypeLocationsAdded = lldb.eBreakpointEventTypeLocationsAdded
    eBreakpointEventTypeLocationsRemoved = lldb.eBreakpointEventTypeLocationsRemoved
    eBreakpointEventTypeLocationsResolved = lldb.eBreakpointEventTypeLocationsResolved
    eBreakpointEventTypeEnabled = lldb.eBreakpointEventTypeEnabled
    eBreakpointEventTypeDisabled = lldb.eBreakpointEventTypeDisabled
    eBreakpointEventTypeCommandChanged = lldb.eBreakpointEventTypeCommandChanged
    eBreakpointEventTypeConditionChanged = lldb.eBreakpointEventTypeConditionChanged
    eBreakpointEventTypeIgnoreChanged = lldb.eBreakpointEventTypeIgnoreChanged
    eBreakpointEventTypeThreadChanged = lldb.eBreakpointEventTypeThreadChanged
    eBreakpointEventTypeAutoContinueChanged = lldb.eBreakpointEventTypeAutoContinueChanged

class WatchpointEventType(Enum):
    eWatchpointEventTypeInvalidType = lldb.eWatchpointEventTypeInvalidType
    eWatchpointEventTypeAdded = lldb.eWatchpointEventTypeAdded
    eWatchpointEventTypeRemoved = lldb.eWatchpointEventTypeRemoved
    eWatchpointEventTypeEnabled = lldb.eWatchpointEventTypeEnabled
    eWatchpointEventTypeDisabled = lldb.eWatchpointEventTypeDisabled
    eWatchpointEventTypeCommandChanged = lldb.eWatchpointEventTypeCommandChanged
    eWatchpointEventTypeConditionChanged = lldb.eWatchpointEventTypeConditionChanged
    eWatchpointEventTypeIgnoreChanged = lldb.eWatchpointEventTypeIgnoreChanged
    eWatchpointEventTypeThreadChanged = lldb.eWatchpointEventTypeThreadChanged
    eWatchpointEventTypeTypeChanged = lldb.eWatchpointEventTypeTypeChanged

class LanguageType(Enum):
    eLanguageTypeUnknown = lldb.eLanguageTypeUnknown
    eLanguageTypeC89 = lldb.eLanguageTypeC89
    eLanguageTypeC = lldb.eLanguageTypeC
    eLanguageTypeAda83 = lldb.eLanguageTypeAda83
    eLanguageTypeC_plus_plus = lldb.eLanguageTypeC_plus_plus
    eLanguageTypeCobol74 = lldb.eLanguageTypeCobol74
    eLanguageTypeCobol85 = lldb.eLanguageTypeCobol85
    eLanguageTypeFortran77 = lldb.eLanguageTypeFortran77
    eLanguageTypeFortran90 = lldb.eLanguageTypeFortran90
    eLanguageTypePascal83 = lldb.eLanguageTypePascal83
    eLanguageTypeModula2 = lldb.eLanguageTypeModula2
    eLanguageTypeJava = lldb.eLanguageTypeJava
    eLanguageTypeC99 = lldb.eLanguageTypeC99
    eLanguageTypeAda95 = lldb.eLanguageTypeAda95
    eLanguageTypeFortran95 = lldb.eLanguageTypeFortran95
    eLanguageTypePLI = lldb.eLanguageTypePLI
    eLanguageTypeObjC = lldb.eLanguageTypeObjC
    eLanguageTypeObjC_plus_plus = lldb.eLanguageTypeObjC_plus_plus
    eLanguageTypeUPC = lldb.eLanguageTypeUPC
    eLanguageTypeD = lldb.eLanguageTypeD
    eLanguageTypePython = lldb.eLanguageTypePython
    eLanguageTypeOpenCL = lldb.eLanguageTypeOpenCL
    eLanguageTypeGo = lldb.eLanguageTypeGo
    eLanguageTypeModula3 = lldb.eLanguageTypeModula3
    eLanguageTypeHaskell = lldb.eLanguageTypeHaskell
    eLanguageTypeC_plus_plus_03 = lldb.eLanguageTypeC_plus_plus_03
    eLanguageTypeC_plus_plus_11 = lldb.eLanguageTypeC_plus_plus_11
    eLanguageTypeOCaml = lldb.eLanguageTypeOCaml
    eLanguageTypeRust = lldb.eLanguageTypeRust
    eLanguageTypeC11 = lldb.eLanguageTypeC11
    eLanguageTypeSwift = lldb.eLanguageTypeSwift
    eLanguageTypeJulia = lldb.eLanguageTypeJulia
    eLanguageTypeDylan = lldb.eLanguageTypeDylan
    eLanguageTypeC_plus_plus_14 = lldb.eLanguageTypeC_plus_plus_14
    eLanguageTypeFortran03 = lldb.eLanguageTypeFortran03
    eLanguageTypeFortran08 = lldb.eLanguageTypeFortran08
    eLanguageTypeRenderScript = lldb.eLanguageTypeRenderScript
    eLanguageTypeBLISS = lldb.eLanguageTypeBLISS
    eLanguageTypeKotlin = lldb.eLanguageTypeKotlin
    eLanguageTypeZig = lldb.eLanguageTypeZig
    eLanguageTypeCrystal = lldb.eLanguageTypeCrystal
    eLanguageTypeC_plus_plus_17 = lldb.eLanguageTypeC_plus_plus_17
    eLanguageTypeC_plus_plus_20 = lldb.eLanguageTypeC_plus_plus_20
    eLanguageTypeC17 = lldb.eLanguageTypeC17
    eLanguageTypeFortran18 = lldb.eLanguageTypeFortran18
    eLanguageTypeAda2005 = lldb.eLanguageTypeAda2005
    eLanguageTypeAda2012 = lldb.eLanguageTypeAda2012
    eLanguageTypeHIP = lldb.eLanguageTypeHIP
    eLanguageTypeAssembly = lldb.eLanguageTypeAssembly
    eLanguageTypeC_sharp = lldb.eLanguageTypeC_sharp
    eLanguageTypeMojo = lldb.eLanguageTypeMojo
    eLanguageTypeMipsAssembler = lldb.eLanguageTypeMipsAssembler
    eNumLanguageTypes = lldb.eNumLanguageTypes

class InstrumentationRuntimeType(Enum):
    eInstrumentationRuntimeTypeAddressSanitizer = lldb.eInstrumentationRuntimeTypeAddressSanitizer
    eInstrumentationRuntimeTypeThreadSanitizer = lldb.eInstrumentationRuntimeTypeThreadSanitizer
    eInstrumentationRuntimeTypeUndefinedBehaviorSanitizer = lldb.eInstrumentationRuntimeTypeUndefinedBehaviorSanitizer
    eInstrumentationRuntimeTypeMainThreadChecker = lldb.eInstrumentationRuntimeTypeMainThreadChecker
    eInstrumentationRuntimeTypeSwiftRuntimeReporting = lldb.eInstrumentationRuntimeTypeSwiftRuntimeReporting
    eNumInstrumentationRuntimeTypes = lldb.eNumInstrumentationRuntimeTypes

class DynamicValueType(Enum):
    eNoDynamicValues = lldb.eNoDynamicValues
    eDynamicCanRunTarget = lldb.eDynamicCanRunTarget
    eDynamicDontRunTarget = lldb.eDynamicDontRunTarget

class StopShowColumn(Enum):
    eStopShowColumnAnsiOrCaret = lldb.eStopShowColumnAnsiOrCaret
    eStopShowColumnAnsi = lldb.eStopShowColumnAnsi
    eStopShowColumnCaret = lldb.eStopShowColumnCaret
    eStopShowColumnNone = lldb.eStopShowColumnNone

class AccessType(Enum):
    eAccessNone = lldb.eAccessNone
    eAccessPublic = lldb.eAccessPublic
    eAccessPrivate = lldb.eAccessPrivate
    eAccessProtected = lldb.eAccessProtected
    eAccessPackage = lldb.eAccessPackage

class CommandArgumentType(Enum):
    eArgTypeAddress = lldb.eArgTypeAddress
    eArgTypeAddressOrExpression = lldb.eArgTypeAddressOrExpression
    eArgTypeAliasName = lldb.eArgTypeAliasName
    eArgTypeAliasOptions = lldb.eArgTypeAliasOptions
    eArgTypeArchitecture = lldb.eArgTypeArchitecture
    eArgTypeBoolean = lldb.eArgTypeBoolean
    eArgTypeBreakpointID = lldb.eArgTypeBreakpointID
    eArgTypeBreakpointIDRange = lldb.eArgTypeBreakpointIDRange
    eArgTypeBreakpointName = lldb.eArgTypeBreakpointName
    eArgTypeByteSize = lldb.eArgTypeByteSize
    eArgTypeClassName = lldb.eArgTypeClassName
    eArgTypeCommandName = lldb.eArgTypeCommandName
    eArgTypeCount = lldb.eArgTypeCount
    eArgTypeDescriptionVerbosity = lldb.eArgTypeDescriptionVerbosity
    eArgTypeDirectoryName = lldb.eArgTypeDirectoryName
    eArgTypeDisassemblyFlavor = lldb.eArgTypeDisassemblyFlavor
    eArgTypeEndAddress = lldb.eArgTypeEndAddress
    eArgTypeExpression = lldb.eArgTypeExpression
    eArgTypeExpressionPath = lldb.eArgTypeExpressionPath
    eArgTypeExprFormat = lldb.eArgTypeExprFormat
    eArgTypeFileLineColumn = lldb.eArgTypeFileLineColumn
    eArgTypeFilename = lldb.eArgTypeFilename
    eArgTypeFormat = lldb.eArgTypeFormat
    eArgTypeFrameIndex = lldb.eArgTypeFrameIndex
    eArgTypeFullName = lldb.eArgTypeFullName
    eArgTypeFunctionName = lldb.eArgTypeFunctionName
    eArgTypeFunctionOrSymbol = lldb.eArgTypeFunctionOrSymbol
    eArgTypeGDBFormat = lldb.eArgTypeGDBFormat
    eArgTypeHelpText = lldb.eArgTypeHelpText
    eArgTypeIndex = lldb.eArgTypeIndex
    eArgTypeLanguage = lldb.eArgTypeLanguage
    eArgTypeLineNum = lldb.eArgTypeLineNum
    eArgTypeLogCategory = lldb.eArgTypeLogCategory
    eArgTypeLogChannel = lldb.eArgTypeLogChannel
    eArgTypeMethod = lldb.eArgTypeMethod
    eArgTypeName = lldb.eArgTypeName
    eArgTypeNewPathPrefix = lldb.eArgTypeNewPathPrefix
    eArgTypeNumLines = lldb.eArgTypeNumLines
    eArgTypeNumberPerLine = lldb.eArgTypeNumberPerLine
    eArgTypeOffset = lldb.eArgTypeOffset
    eArgTypeOldPathPrefix = lldb.eArgTypeOldPathPrefix
    eArgTypeOneLiner = lldb.eArgTypeOneLiner
    eArgTypePath = lldb.eArgTypePath
    eArgTypePermissionsNumber = lldb.eArgTypePermissionsNumber
    eArgTypePermissionsString = lldb.eArgTypePermissionsString
    eArgTypePid = lldb.eArgTypePid
    eArgTypePlugin = lldb.eArgTypePlugin
    eArgTypeProcessName = lldb.eArgTypeProcessName
    eArgTypePythonClass = lldb.eArgTypePythonClass
    eArgTypePythonFunction = lldb.eArgTypePythonFunction
    eArgTypePythonScript = lldb.eArgTypePythonScript
    eArgTypeQueueName = lldb.eArgTypeQueueName
    eArgTypeRegisterName = lldb.eArgTypeRegisterName
    eArgTypeRegularExpression = lldb.eArgTypeRegularExpression
    eArgTypeRunArgs = lldb.eArgTypeRunArgs
    eArgTypeRunMode = lldb.eArgTypeRunMode
    eArgTypeScriptedCommandSynchronicity = lldb.eArgTypeScriptedCommandSynchronicity
    eArgTypeScriptLang = lldb.eArgTypeScriptLang
    eArgTypeSearchWord = lldb.eArgTypeSearchWord
    eArgTypeSelector = lldb.eArgTypeSelector
    eArgTypeSettingIndex = lldb.eArgTypeSettingIndex
    eArgTypeSettingKey = lldb.eArgTypeSettingKey
    eArgTypeSettingPrefix = lldb.eArgTypeSettingPrefix
    eArgTypeSettingVariableName = lldb.eArgTypeSettingVariableName
    eArgTypeShlibName = lldb.eArgTypeShlibName
    eArgTypeSourceFile = lldb.eArgTypeSourceFile
    eArgTypeSortOrder = lldb.eArgTypeSortOrder
    eArgTypeStartAddress = lldb.eArgTypeStartAddress
    eArgTypeSummaryString = lldb.eArgTypeSummaryString
    eArgTypeSymbol = lldb.eArgTypeSymbol
    eArgTypeThreadID = lldb.eArgTypeThreadID
    eArgTypeThreadIndex = lldb.eArgTypeThreadIndex
    eArgTypeThreadName = lldb.eArgTypeThreadName
    eArgTypeTypeName = lldb.eArgTypeTypeName
    eArgTypeUnsignedInteger = lldb.eArgTypeUnsignedInteger
    eArgTypeUnixSignal = lldb.eArgTypeUnixSignal
    eArgTypeVarName = lldb.eArgTypeVarName
    eArgTypeValue = lldb.eArgTypeValue
    eArgTypeWidth = lldb.eArgTypeWidth
    eArgTypeNone = lldb.eArgTypeNone
    eArgTypePlatform = lldb.eArgTypePlatform
    eArgTypeWatchpointID = lldb.eArgTypeWatchpointID
    eArgTypeWatchpointIDRange = lldb.eArgTypeWatchpointIDRange
    eArgTypeWatchType = lldb.eArgTypeWatchType
    eArgRawInput = lldb.eArgRawInput
    eArgTypeCommand = lldb.eArgTypeCommand
    eArgTypeColumnNum = lldb.eArgTypeColumnNum
    eArgTypeModuleUUID = lldb.eArgTypeModuleUUID
    eArgTypeSaveCoreStyle = lldb.eArgTypeSaveCoreStyle
    eArgTypeLogHandler = lldb.eArgTypeLogHandler
    eArgTypeSEDStylePair = lldb.eArgTypeSEDStylePair
    eArgTypeRecognizerID = lldb.eArgTypeRecognizerID
    eArgTypeConnectURL = lldb.eArgTypeConnectURL
    eArgTypeTargetID = lldb.eArgTypeTargetID
    eArgTypeStopHookID = lldb.eArgTypeStopHookID
    eArgTypeCompletionType = lldb.eArgTypeCompletionType
    eArgTypeLastArg = lldb.eArgTypeLastArg

class SymbolType(Enum):
    eSymbolTypeAny = lldb.eSymbolTypeAny
    eSymbolTypeInvalid = lldb.eSymbolTypeInvalid
    eSymbolTypeAbsolute = lldb.eSymbolTypeAbsolute
    eSymbolTypeCode = lldb.eSymbolTypeCode
    eSymbolTypeResolver = lldb.eSymbolTypeResolver
    eSymbolTypeData = lldb.eSymbolTypeData
    eSymbolTypeTrampoline = lldb.eSymbolTypeTrampoline
    eSymbolTypeRuntime = lldb.eSymbolTypeRuntime
    eSymbolTypeException = lldb.eSymbolTypeException
    eSymbolTypeSourceFile = lldb.eSymbolTypeSourceFile
    eSymbolTypeHeaderFile = lldb.eSymbolTypeHeaderFile
    eSymbolTypeObjectFile = lldb.eSymbolTypeObjectFile
    eSymbolTypeCommonBlock = lldb.eSymbolTypeCommonBlock
    eSymbolTypeBlock = lldb.eSymbolTypeBlock
    eSymbolTypeLocal = lldb.eSymbolTypeLocal
    eSymbolTypeParam = lldb.eSymbolTypeParam
    eSymbolTypeVariable = lldb.eSymbolTypeVariable
    eSymbolTypeVariableType = lldb.eSymbolTypeVariableType
    eSymbolTypeLineEntry = lldb.eSymbolTypeLineEntry
    eSymbolTypeLineHeader = lldb.eSymbolTypeLineHeader
    eSymbolTypeScopeBegin = lldb.eSymbolTypeScopeBegin
    eSymbolTypeScopeEnd = lldb.eSymbolTypeScopeEnd
    eSymbolTypeAdditional = lldb.eSymbolTypeAdditional
    eSymbolTypeCompiler = lldb.eSymbolTypeCompiler
    eSymbolTypeInstrumentation = lldb.eSymbolTypeInstrumentation
    eSymbolTypeUndefined = lldb.eSymbolTypeUndefined
    eSymbolTypeObjCClass = lldb.eSymbolTypeObjCClass
    eSymbolTypeObjCMetaClass = lldb.eSymbolTypeObjCMetaClass
    eSymbolTypeObjCIVar = lldb.eSymbolTypeObjCIVar
    eSymbolTypeReExported = lldb.eSymbolTypeReExported

class SectionType(Enum):
    eSectionTypeInvalid = lldb.eSectionTypeInvalid
    eSectionTypeCode = lldb.eSectionTypeCode
    eSectionTypeContainer = lldb.eSectionTypeContainer
    eSectionTypeData = lldb.eSectionTypeData
    eSectionTypeDataCString = lldb.eSectionTypeDataCString
    eSectionTypeDataCStringPointers = lldb.eSectionTypeDataCStringPointers
    eSectionTypeDataSymbolAddress = lldb.eSectionTypeDataSymbolAddress
    eSectionTypeData4 = lldb.eSectionTypeData4
    eSectionTypeData8 = lldb.eSectionTypeData8
    eSectionTypeData16 = lldb.eSectionTypeData16
    eSectionTypeDataPointers = lldb.eSectionTypeDataPointers
    eSectionTypeDebug = lldb.eSectionTypeDebug
    eSectionTypeZeroFill = lldb.eSectionTypeZeroFill
    eSectionTypeDataObjCMessageRefs = lldb.eSectionTypeDataObjCMessageRefs
    eSectionTypeDataObjCCFStrings = lldb.eSectionTypeDataObjCCFStrings
    eSectionTypeDWARFDebugAbbrev = lldb.eSectionTypeDWARFDebugAbbrev
    eSectionTypeDWARFDebugAddr = lldb.eSectionTypeDWARFDebugAddr
    eSectionTypeDWARFDebugAranges = lldb.eSectionTypeDWARFDebugAranges
    eSectionTypeDWARFDebugCuIndex = lldb.eSectionTypeDWARFDebugCuIndex
    eSectionTypeDWARFDebugFrame = lldb.eSectionTypeDWARFDebugFrame
    eSectionTypeDWARFDebugInfo = lldb.eSectionTypeDWARFDebugInfo
    eSectionTypeDWARFDebugLine = lldb.eSectionTypeDWARFDebugLine
    eSectionTypeDWARFDebugLoc = lldb.eSectionTypeDWARFDebugLoc
    eSectionTypeDWARFDebugMacInfo = lldb.eSectionTypeDWARFDebugMacInfo
    eSectionTypeDWARFDebugMacro = lldb.eSectionTypeDWARFDebugMacro
    eSectionTypeDWARFDebugPubNames = lldb.eSectionTypeDWARFDebugPubNames
    eSectionTypeDWARFDebugPubTypes = lldb.eSectionTypeDWARFDebugPubTypes
    eSectionTypeDWARFDebugRanges = lldb.eSectionTypeDWARFDebugRanges
    eSectionTypeDWARFDebugStr = lldb.eSectionTypeDWARFDebugStr
    eSectionTypeDWARFDebugStrOffsets = lldb.eSectionTypeDWARFDebugStrOffsets
    eSectionTypeDWARFAppleNames = lldb.eSectionTypeDWARFAppleNames
    eSectionTypeDWARFAppleTypes = lldb.eSectionTypeDWARFAppleTypes
    eSectionTypeDWARFAppleNamespaces = lldb.eSectionTypeDWARFAppleNamespaces
    eSectionTypeDWARFAppleObjC = lldb.eSectionTypeDWARFAppleObjC
    eSectionTypeELFSymbolTable = lldb.eSectionTypeELFSymbolTable
    eSectionTypeELFDynamicSymbols = lldb.eSectionTypeELFDynamicSymbols
    eSectionTypeELFRelocationEntries = lldb.eSectionTypeELFRelocationEntries
    eSectionTypeELFDynamicLinkInfo = lldb.eSectionTypeELFDynamicLinkInfo
    eSectionTypeEHFrame = lldb.eSectionTypeEHFrame
    eSectionTypeARMexidx = lldb.eSectionTypeARMexidx
    eSectionTypeARMextab = lldb.eSectionTypeARMextab
    eSectionTypeCompactUnwind = lldb.eSectionTypeCompactUnwind
    eSectionTypeGoSymtab = lldb.eSectionTypeGoSymtab
    eSectionTypeAbsoluteAddress = lldb.eSectionTypeAbsoluteAddress
    eSectionTypeDWARFGNUDebugAltLink = lldb.eSectionTypeDWARFGNUDebugAltLink
    eSectionTypeDWARFDebugTypes = lldb.eSectionTypeDWARFDebugTypes
    eSectionTypeDWARFDebugNames = lldb.eSectionTypeDWARFDebugNames
    eSectionTypeOther = lldb.eSectionTypeOther
    eSectionTypeDWARFDebugLineStr = lldb.eSectionTypeDWARFDebugLineStr
    eSectionTypeDWARFDebugRngLists = lldb.eSectionTypeDWARFDebugRngLists
    eSectionTypeDWARFDebugLocLists = lldb.eSectionTypeDWARFDebugLocLists
    eSectionTypeDWARFDebugAbbrevDwo = lldb.eSectionTypeDWARFDebugAbbrevDwo
    eSectionTypeDWARFDebugInfoDwo = lldb.eSectionTypeDWARFDebugInfoDwo
    eSectionTypeDWARFDebugStrDwo = lldb.eSectionTypeDWARFDebugStrDwo
    eSectionTypeDWARFDebugStrOffsetsDwo = lldb.eSectionTypeDWARFDebugStrOffsetsDwo
    eSectionTypeDWARFDebugTypesDwo = lldb.eSectionTypeDWARFDebugTypesDwo
    eSectionTypeDWARFDebugRngListsDwo = lldb.eSectionTypeDWARFDebugRngListsDwo
    eSectionTypeDWARFDebugLocDwo = lldb.eSectionTypeDWARFDebugLocDwo
    eSectionTypeDWARFDebugLocListsDwo = lldb.eSectionTypeDWARFDebugLocListsDwo
    eSectionTypeDWARFDebugTuIndex = lldb.eSectionTypeDWARFDebugTuIndex
    eSectionTypeCTF = lldb.eSectionTypeCTF

class EmulateInstructionOptions(Enum):
    eEmulateInstructionOptionNone = lldb.eEmulateInstructionOptionNone
    eEmulateInstructionOptionAutoAdvancePC = lldb.eEmulateInstructionOptionAutoAdvancePC
    eEmulateInstructionOptionIgnoreConditions = lldb.eEmulateInstructionOptionIgnoreConditions

class FunctionNameType(Enum):
    eFunctionNameTypeNone = lldb.eFunctionNameTypeNone
    eFunctionNameTypeAuto = lldb.eFunctionNameTypeAuto
    eFunctionNameTypeFull = lldb.eFunctionNameTypeFull
    eFunctionNameTypeBase = lldb.eFunctionNameTypeBase
    eFunctionNameTypeMethod = lldb.eFunctionNameTypeMethod
    eFunctionNameTypeSelector = lldb.eFunctionNameTypeSelector
    eFunctionNameTypeAny = lldb.eFunctionNameTypeAny

class BasicType(Enum):
    eBasicTypeInvalid = lldb.eBasicTypeInvalid
    eBasicTypeVoid = lldb.eBasicTypeVoid
    eBasicTypeChar = lldb.eBasicTypeChar
    eBasicTypeSignedChar = lldb.eBasicTypeSignedChar
    eBasicTypeUnsignedChar = lldb.eBasicTypeUnsignedChar
    eBasicTypeWChar = lldb.eBasicTypeWChar
    eBasicTypeSignedWChar = lldb.eBasicTypeSignedWChar
    eBasicTypeUnsignedWChar = lldb.eBasicTypeUnsignedWChar
    eBasicTypeChar16 = lldb.eBasicTypeChar16
    eBasicTypeChar32 = lldb.eBasicTypeChar32
    eBasicTypeChar8 = lldb.eBasicTypeChar8
    eBasicTypeShort = lldb.eBasicTypeShort
    eBasicTypeUnsignedShort = lldb.eBasicTypeUnsignedShort
    eBasicTypeInt = lldb.eBasicTypeInt
    eBasicTypeUnsignedInt = lldb.eBasicTypeUnsignedInt
    eBasicTypeLong = lldb.eBasicTypeLong
    eBasicTypeUnsignedLong = lldb.eBasicTypeUnsignedLong
    eBasicTypeLongLong = lldb.eBasicTypeLongLong
    eBasicTypeUnsignedLongLong = lldb.eBasicTypeUnsignedLongLong
    eBasicTypeInt128 = lldb.eBasicTypeInt128
    eBasicTypeUnsignedInt128 = lldb.eBasicTypeUnsignedInt128
    eBasicTypeBool = lldb.eBasicTypeBool
    eBasicTypeHalf = lldb.eBasicTypeHalf
    eBasicTypeFloat = lldb.eBasicTypeFloat
    eBasicTypeDouble = lldb.eBasicTypeDouble
    eBasicTypeLongDouble = lldb.eBasicTypeLongDouble
    eBasicTypeFloatComplex = lldb.eBasicTypeFloatComplex
    eBasicTypeDoubleComplex = lldb.eBasicTypeDoubleComplex
    eBasicTypeLongDoubleComplex = lldb.eBasicTypeLongDoubleComplex
    eBasicTypeObjCID = lldb.eBasicTypeObjCID
    eBasicTypeObjCClass = lldb.eBasicTypeObjCClass
    eBasicTypeObjCSel = lldb.eBasicTypeObjCSel
    eBasicTypeNullPtr = lldb.eBasicTypeNullPtr
    eBasicTypeOther = lldb.eBasicTypeOther

class TraceType(Enum):
    eTraceTypeNone = lldb.eTraceTypeNone
    eTraceTypeProcessorTrace = lldb.eTraceTypeProcessorTrace

class StructuredDataType(Enum):
    eStructuredDataTypeInvalid = lldb.eStructuredDataTypeInvalid
    eStructuredDataTypeNull = lldb.eStructuredDataTypeNull
    eStructuredDataTypeGeneric = lldb.eStructuredDataTypeGeneric
    eStructuredDataTypeArray = lldb.eStructuredDataTypeArray
    eStructuredDataTypeInteger = lldb.eStructuredDataTypeInteger
    eStructuredDataTypeFloat = lldb.eStructuredDataTypeFloat
    eStructuredDataTypeBoolean = lldb.eStructuredDataTypeBoolean
    eStructuredDataTypeString = lldb.eStructuredDataTypeString
    eStructuredDataTypeDictionary = lldb.eStructuredDataTypeDictionary
    eStructuredDataTypeSignedInteger = lldb.eStructuredDataTypeSignedInteger
    eStructuredDataTypeUnsignedInteger = lldb.eStructuredDataTypeUnsignedInteger

class TypeClass(Enum):
    eTypeClassInvalid = lldb.eTypeClassInvalid
    eTypeClassArray = lldb.eTypeClassArray
    eTypeClassBlockPointer = lldb.eTypeClassBlockPointer
    eTypeClassBuiltin = lldb.eTypeClassBuiltin
    eTypeClassClass = lldb.eTypeClassClass
    eTypeClassComplexFloat = lldb.eTypeClassComplexFloat
    eTypeClassComplexInteger = lldb.eTypeClassComplexInteger
    eTypeClassEnumeration = lldb.eTypeClassEnumeration
    eTypeClassFunction = lldb.eTypeClassFunction
    eTypeClassMemberPointer = lldb.eTypeClassMemberPointer
    eTypeClassObjCObject = lldb.eTypeClassObjCObject
    eTypeClassObjCInterface = lldb.eTypeClassObjCInterface
    eTypeClassObjCObjectPointer = lldb.eTypeClassObjCObjectPointer
    eTypeClassPointer = lldb.eTypeClassPointer
    eTypeClassReference = lldb.eTypeClassReference
    eTypeClassStruct = lldb.eTypeClassStruct
    eTypeClassTypedef = lldb.eTypeClassTypedef
    eTypeClassUnion = lldb.eTypeClassUnion
    eTypeClassVector = lldb.eTypeClassVector
    eTypeClassOther = lldb.eTypeClassOther
    eTypeClassAny = lldb.eTypeClassAny

class TemplateArgumentKind(Enum):
    eTemplateArgumentKindNull = lldb.eTemplateArgumentKindNull
    eTemplateArgumentKindType = lldb.eTemplateArgumentKindType
    eTemplateArgumentKindDeclaration = lldb.eTemplateArgumentKindDeclaration
    eTemplateArgumentKindIntegral = lldb.eTemplateArgumentKindIntegral
    eTemplateArgumentKindTemplate = lldb.eTemplateArgumentKindTemplate
    eTemplateArgumentKindTemplateExpansion = lldb.eTemplateArgumentKindTemplateExpansion
    eTemplateArgumentKindExpression = lldb.eTemplateArgumentKindExpression
    eTemplateArgumentKindPack = lldb.eTemplateArgumentKindPack
    eTemplateArgumentKindNullPtr = lldb.eTemplateArgumentKindNullPtr

class FormatterMatchType(Enum):
    eFormatterMatchExact = lldb.eFormatterMatchExact
    eFormatterMatchRegex = lldb.eFormatterMatchRegex
    eFormatterMatchCallback = lldb.eFormatterMatchCallback
    eLastFormatterMatchType = lldb.eLastFormatterMatchType

class TypeOptions(Enum):
    eTypeOptionNone = lldb.eTypeOptionNone
    eTypeOptionCascade = lldb.eTypeOptionCascade
    eTypeOptionSkipPointers = lldb.eTypeOptionSkipPointers
    eTypeOptionSkipReferences = lldb.eTypeOptionSkipReferences
    eTypeOptionHideChildren = lldb.eTypeOptionHideChildren
    eTypeOptionHideValue = lldb.eTypeOptionHideValue
    eTypeOptionShowOneLiner = lldb.eTypeOptionShowOneLiner
    eTypeOptionHideNames = lldb.eTypeOptionHideNames
    eTypeOptionNonCacheable = lldb.eTypeOptionNonCacheable
    eTypeOptionHideEmptyAggregates = lldb.eTypeOptionHideEmptyAggregates
    eTypeOptionFrontEndWantsDereference = lldb.eTypeOptionFrontEndWantsDereference

class FrameComparison(Enum):
    eFrameCompareInvalid = lldb.eFrameCompareInvalid
    eFrameCompareUnknown = lldb.eFrameCompareUnknown
    eFrameCompareEqual = lldb.eFrameCompareEqual
    eFrameCompareSameParent = lldb.eFrameCompareSameParent
    eFrameCompareYounger = lldb.eFrameCompareYounger
    eFrameCompareOlder = lldb.eFrameCompareOlder

class FilePermissions(Enum):
    eFilePermissionsUserRead = lldb.eFilePermissionsUserRead
    eFilePermissionsUserWrite = lldb.eFilePermissionsUserWrite
    eFilePermissionsUserExecute = lldb.eFilePermissionsUserExecute
    eFilePermissionsGroupRead = lldb.eFilePermissionsGroupRead
    eFilePermissionsGroupWrite = lldb.eFilePermissionsGroupWrite
    eFilePermissionsGroupExecute = lldb.eFilePermissionsGroupExecute
    eFilePermissionsWorldRead = lldb.eFilePermissionsWorldRead
    eFilePermissionsWorldWrite = lldb.eFilePermissionsWorldWrite
    eFilePermissionsWorldExecute = lldb.eFilePermissionsWorldExecute
    eFilePermissionsUserRW = lldb.eFilePermissionsUserRW
    eFileFilePermissionsUserRX = lldb.eFileFilePermissionsUserRX
    eFilePermissionsUserRWX = lldb.eFilePermissionsUserRWX
    eFilePermissionsGroupRW = lldb.eFilePermissionsGroupRW
    eFilePermissionsGroupRX = lldb.eFilePermissionsGroupRX
    eFilePermissionsGroupRWX = lldb.eFilePermissionsGroupRWX
    eFilePermissionsWorldRW = lldb.eFilePermissionsWorldRW
    eFilePermissionsWorldRX = lldb.eFilePermissionsWorldRX
    eFilePermissionsWorldRWX = lldb.eFilePermissionsWorldRWX
    eFilePermissionsEveryoneR = lldb.eFilePermissionsEveryoneR
    eFilePermissionsEveryoneW = lldb.eFilePermissionsEveryoneW
    eFilePermissionsEveryoneX = lldb.eFilePermissionsEveryoneX
    eFilePermissionsEveryoneRW = lldb.eFilePermissionsEveryoneRW
    eFilePermissionsEveryoneRX = lldb.eFilePermissionsEveryoneRX
    eFilePermissionsEveryoneRWX = lldb.eFilePermissionsEveryoneRWX
    eFilePermissionsFileDefault = lldb.eFilePermissionsFileDefault
    eFilePermissionsDirectoryDefault = lldb.eFilePermissionsDirectoryDefault

class QueueItemKind(Enum):
    eQueueItemKindUnknown = lldb.eQueueItemKindUnknown
    eQueueItemKindFunction = lldb.eQueueItemKindFunction
    eQueueItemKindBlock = lldb.eQueueItemKindBlock

class QueueKind(Enum):
    eQueueKindUnknown = lldb.eQueueKindUnknown
    eQueueKindSerial = lldb.eQueueKindSerial
    eQueueKindConcurrent = lldb.eQueueKindConcurrent

class ExpressionEvaluationPhase(Enum):
    eExpressionEvaluationParse = lldb.eExpressionEvaluationParse
    eExpressionEvaluationIRGen = lldb.eExpressionEvaluationIRGen
    eExpressionEvaluationExecution = lldb.eExpressionEvaluationExecution
    eExpressionEvaluationComplete = lldb.eExpressionEvaluationComplete

class InstructionControlFlowKind(Enum):
    eInstructionControlFlowKindUnknown = lldb.eInstructionControlFlowKindUnknown
    eInstructionControlFlowKindOther = lldb.eInstructionControlFlowKindOther
    eInstructionControlFlowKindCall = lldb.eInstructionControlFlowKindCall
    eInstructionControlFlowKindReturn = lldb.eInstructionControlFlowKindReturn
    eInstructionControlFlowKindJump = lldb.eInstructionControlFlowKindJump
    eInstructionControlFlowKindCondJump = lldb.eInstructionControlFlowKindCondJump
    eInstructionControlFlowKindFarCall = lldb.eInstructionControlFlowKindFarCall
    eInstructionControlFlowKindFarReturn = lldb.eInstructionControlFlowKindFarReturn
    eInstructionControlFlowKindFarJump = lldb.eInstructionControlFlowKindFarJump

class WatchpointKind(Enum):
    eWatchpointKindWrite = lldb.eWatchpointKindWrite
    eWatchpointKindRead = lldb.eWatchpointKindRead

class GdbSignal(Enum):
    eGdbSignalBadAccess = lldb.eGdbSignalBadAccess
    eGdbSignalBadInstruction = lldb.eGdbSignalBadInstruction
    eGdbSignalArithmetic = lldb.eGdbSignalArithmetic
    eGdbSignalEmulation = lldb.eGdbSignalEmulation
    eGdbSignalSoftware = lldb.eGdbSignalSoftware
    eGdbSignalBreakpoint = lldb.eGdbSignalBreakpoint

class PathType(Enum):
    ePathTypeLLDBShlibDir = lldb.ePathTypeLLDBShlibDir
    ePathTypeSupportExecutableDir = lldb.ePathTypeSupportExecutableDir
    ePathTypeHeaderDir = lldb.ePathTypeHeaderDir
    ePathTypePythonDir = lldb.ePathTypePythonDir
    ePathTypeLLDBSystemPlugins = lldb.ePathTypeLLDBSystemPlugins
    ePathTypeLLDBUserPlugins = lldb.ePathTypeLLDBUserPlugins
    ePathTypeLLDBTempSystemDir = lldb.ePathTypeLLDBTempSystemDir
    ePathTypeGlobalLLDBTempSystemDir = lldb.ePathTypeGlobalLLDBTempSystemDir
    ePathTypeClangDir = lldb.ePathTypeClangDir

class MemberFunctionKind(Enum):
    eMemberFunctionKindUnknown = lldb.eMemberFunctionKindUnknown
    eMemberFunctionKindConstructor = lldb.eMemberFunctionKindConstructor
    eMemberFunctionKindDestructor = lldb.eMemberFunctionKindDestructor
    eMemberFunctionKindInstanceMethod = lldb.eMemberFunctionKindInstanceMethod
    eMemberFunctionKindStaticMethod = lldb.eMemberFunctionKindStaticMethod

class MatchType(Enum):
    eMatchTypeNormal = lldb.eMatchTypeNormal
    eMatchTypeRegex = lldb.eMatchTypeRegex
    eMatchTypeStartsWith = lldb.eMatchTypeStartsWith

class TypeFlags(Enum):
    eTypeHasChildren = lldb.eTypeHasChildren
    eTypeHasValue = lldb.eTypeHasValue
    eTypeIsArray = lldb.eTypeIsArray
    eTypeIsBlock = lldb.eTypeIsBlock
    eTypeIsBuiltIn = lldb.eTypeIsBuiltIn
    eTypeIsClass = lldb.eTypeIsClass
    eTypeIsCPlusPlus = lldb.eTypeIsCPlusPlus
    eTypeIsEnumeration = lldb.eTypeIsEnumeration
    eTypeIsFuncPrototype = lldb.eTypeIsFuncPrototype
    eTypeIsMember = lldb.eTypeIsMember
    eTypeIsObjC = lldb.eTypeIsObjC
    eTypeIsPointer = lldb.eTypeIsPointer
    eTypeIsReference = lldb.eTypeIsReference
    eTypeIsStructUnion = lldb.eTypeIsStructUnion
    eTypeIsTemplate = lldb.eTypeIsTemplate
    eTypeIsTypedef = lldb.eTypeIsTypedef
    eTypeIsVector = lldb.eTypeIsVector
    eTypeIsScalar = lldb.eTypeIsScalar
    eTypeIsInteger = lldb.eTypeIsInteger
    eTypeIsFloat = lldb.eTypeIsFloat
    eTypeIsComplex = lldb.eTypeIsComplex
    eTypeIsSigned = lldb.eTypeIsSigned
    eTypeInstanceIsPointer = lldb.eTypeInstanceIsPointer

class CommandFlags(Enum):
    eCommandRequiresTarget = lldb.eCommandRequiresTarget
    eCommandRequiresProcess = lldb.eCommandRequiresProcess
    eCommandRequiresThread = lldb.eCommandRequiresThread
    eCommandRequiresFrame = lldb.eCommandRequiresFrame
    eCommandRequiresRegContext = lldb.eCommandRequiresRegContext
    eCommandTryTargetAPILock = lldb.eCommandTryTargetAPILock
    eCommandProcessMustBeLaunched = lldb.eCommandProcessMustBeLaunched
    eCommandProcessMustBePaused = lldb.eCommandProcessMustBePaused
    eCommandProcessMustBeTraced = lldb.eCommandProcessMustBeTraced

class TypeSummaryCapping(Enum):
    eTypeSummaryCapped = lldb.eTypeSummaryCapped
    eTypeSummaryUncapped = lldb.eTypeSummaryUncapped

class CommandInterpreterResult(Enum):
    eCommandInterpreterResultSuccess = lldb.eCommandInterpreterResultSuccess
    eCommandInterpreterResultInferiorCrash = lldb.eCommandInterpreterResultInferiorCrash
    eCommandInterpreterResultCommandError = lldb.eCommandInterpreterResultCommandError
    eCommandInterpreterResultQuitRequested = lldb.eCommandInterpreterResultQuitRequested

class SaveCoreStyle(Enum):
    eSaveCoreUnspecified = lldb.eSaveCoreUnspecified
    eSaveCoreFull = lldb.eSaveCoreFull
    eSaveCoreDirtyOnly = lldb.eSaveCoreDirtyOnly
    eSaveCoreStackOnly = lldb.eSaveCoreStackOnly

class TraceEvent(Enum):
    eTraceEventDisabledSW = lldb.eTraceEventDisabledSW
    eTraceEventDisabledHW = lldb.eTraceEventDisabledHW
    eTraceEventCPUChanged = lldb.eTraceEventCPUChanged
    eTraceEventHWClockTick = lldb.eTraceEventHWClockTick
    eTraceEventSyncPoint = lldb.eTraceEventSyncPoint

class TraceItemKind(Enum):
    eTraceItemKindError = lldb.eTraceItemKindError
    eTraceItemKindEvent = lldb.eTraceItemKindEvent
    eTraceItemKindInstruction = lldb.eTraceItemKindInstruction

class TraceCursorSeekType(Enum):
    eTraceCursorSeekTypeBeginning = lldb.eTraceCursorSeekTypeBeginning
    eTraceCursorSeekTypeCurrent = lldb.eTraceCursorSeekTypeCurrent
    eTraceCursorSeekTypeEnd = lldb.eTraceCursorSeekTypeEnd

class DWIMPrintVerbosity(Enum):
    eDWIMPrintVerbosityNone = lldb.eDWIMPrintVerbosityNone
    eDWIMPrintVerbosityExpression = lldb.eDWIMPrintVerbosityExpression
    eDWIMPrintVerbosityFull = lldb.eDWIMPrintVerbosityFull

class WatchpointValueKind(Enum):
    eWatchPointValueKindInvalid = lldb.eWatchPointValueKindInvalid
    eWatchPointValueKindVariable = lldb.eWatchPointValueKindVariable
    eWatchPointValueKindExpression = lldb.eWatchPointValueKindExpression

class CompletionType(Enum):
    eNoCompletion = lldb.eNoCompletion
    eSourceFileCompletion = lldb.eSourceFileCompletion
    eDiskFileCompletion = lldb.eDiskFileCompletion
    eDiskDirectoryCompletion = lldb.eDiskDirectoryCompletion
    eSymbolCompletion = lldb.eSymbolCompletion
    eModuleCompletion = lldb.eModuleCompletion
    eSettingsNameCompletion = lldb.eSettingsNameCompletion
    ePlatformPluginCompletion = lldb.ePlatformPluginCompletion
    eArchitectureCompletion = lldb.eArchitectureCompletion
    eVariablePathCompletion = lldb.eVariablePathCompletion
    eRegisterCompletion = lldb.eRegisterCompletion
    eBreakpointCompletion = lldb.eBreakpointCompletion
    eProcessPluginCompletion = lldb.eProcessPluginCompletion
    eDisassemblyFlavorCompletion = lldb.eDisassemblyFlavorCompletion
    eTypeLanguageCompletion = lldb.eTypeLanguageCompletion
    eFrameIndexCompletion = lldb.eFrameIndexCompletion
    eModuleUUIDCompletion = lldb.eModuleUUIDCompletion
    eStopHookIDCompletion = lldb.eStopHookIDCompletion
    eThreadIndexCompletion = lldb.eThreadIndexCompletion
    eWatchpointIDCompletion = lldb.eWatchpointIDCompletion
    eBreakpointNameCompletion = lldb.eBreakpointNameCompletion
    eProcessIDCompletion = lldb.eProcessIDCompletion
    eProcessNameCompletion = lldb.eProcessNameCompletion
    eRemoteDiskFileCompletion = lldb.eRemoteDiskFileCompletion
    eRemoteDiskDirectoryCompletion = lldb.eRemoteDiskDirectoryCompletion
    eTypeCategoryNameCompletion = lldb.eTypeCategoryNameCompletion
    eCustomCompletion = lldb.eCustomCompletion

