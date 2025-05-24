# noinspection PyUnresolvedReferences
from importlib import reload
import godot_formatters.godot_providers

# we have to force reload the dependent modules to make lldb update the providers if we're re-loading the module
godot_formatters.godot_providers = reload(godot_formatters.godot_providers)
from godot_formatters.godot_providers import *

import godot_formatters.godot_types

reload(godot_formatters.godot_types)
from godot_formatters.godot_types import *


import godot_formatters.utils

reload(godot_formatters.utils)
from godot_formatters.utils import *

import godot_formatters.options

reload(godot_formatters.options)
from godot_formatters.options import *


import godot_formatters.registration

reload(godot_formatters.registration)
from godot_formatters.registration import *

from godot_formatters.registration import SetOptsCommand, GetOptsCommand, ReloadCommand

from lldb import SBDebugger


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
