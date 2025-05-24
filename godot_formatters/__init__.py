# noinspection PyUnresolvedReferences
from importlib import reload
import godot_formatters.godot_providers

# we have to force reload the dependent modules to make lldb update the providers if we're re-loading the module
godot_formatters.godot_providers = reload(godot_formatters.godot_providers)
from godot_formatters.godot_providers import *

import godot_formatters.godot_types

reload(godot_formatters.godot_types)
from godot_formatters.godot_types import *


# fmt: off
from lldb import (SBCommandReturnObject, SBExecutionContext, SBTypeCategory, eFormatBytes, eFormatCString, eFormatUnicode32, eNoDynamicValues, eDynamicDontRunTarget, eDynamicCanRunTarget, eBasicTypeInvalid, eBasicTypeVoid, eBasicTypeChar, 
                  eBasicTypeSignedChar, eBasicTypeUnsignedChar, eBasicTypeWChar, eBasicTypeSignedWChar, eBasicTypeUnsignedWChar, eBasicTypeChar16, eBasicTypeChar32, 
                  eBasicTypeChar8, eBasicTypeShort, eBasicTypeUnsignedShort, eBasicTypeInt, eBasicTypeUnsignedInt, eBasicTypeLong, eBasicTypeUnsignedLong, eBasicTypeLongLong, 
                  eBasicTypeUnsignedLongLong, eBasicTypeInt128, eBasicTypeUnsignedInt128, eBasicTypeBool, eBasicTypeHalf, eBasicTypeFloat, eBasicTypeDouble, eBasicTypeLongDouble, 
                  eBasicTypeFloatComplex, eBasicTypeDoubleComplex, eBasicTypeLongDoubleComplex, eBasicTypeObjCID, eBasicTypeObjCClass, eBasicTypeObjCSel, eBasicTypeNullPtr, eReturnStatusSuccessFinishNoResult, eReturnStatusSuccessFinishResult, 
                  eTypeClassClass, eTypeClassEnumeration, eTypeClassPointer, eTypeOptionCascade)
from lldb import ( SBValue, SBAddress, SBData, SBType, SBTypeEnumMember, SBTypeEnumMemberList, SBSyntheticValueProvider, SBError, SBTarget, SBDebugger, SBTypeSummary, SBTypeSynthetic, SBTypeNameSpecifier)
# fmt: on


# ********************************************************
# REGISTRATION
# ********************************************************

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
