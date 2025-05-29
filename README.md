# README #

I use LLDB to debug the Godot engine, and got tired with there being no visualization for all the built-in types. Here I endeavor to make all of these types visible through the debugger.

# Installation #

Clone this repo somewhere, e.g. ~/GodotFormatters. Then add the following lines to your ~/.lldbinit, or run this line directly in the debug console:

```
command script import ~/GodotFormatters/godot_formatters
```

You can also include it in a launch.json configuration for a [lldb-dap](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.lldb-dap) debug configuration by putting it in the `initCommands` section, like so:

```json
{
    "name": "(lldb-dap) Run tests (editor DEBUG)",
    "type": "lldb-dap",
    "request": "launch",
    "program": "${workspaceFolder}/bin/<godot_bin>",
    "args": [
        "--test"
    ],
    "initCommands": [
        "command script import ~/GodotFormatters/godot_formatters"
    ],
    "cwd": "${workspaceFolder}"
}
```

It's also possible to use it with the official Microsoft C++ extension debugger (i.e. `cppdbg`), but it is generally recommended to use lldb-dap instead:
```json
{
    "name": "(lldb) Run tests (editor DEBUG)",
    "type": "cppdbg",
    "request": "launch",
    "program": "${workspaceFolder}/bin/<godot_bin>",
    "args": [
        "--test"
    ],
    "MIMode": "lldb",
    "setupCommands": [
        {
            "text": "command script import ~/GodotFormatters/godot_formatters",
            "description": "Godot Visualizers"
        },
        {
            "text": "godot-formatter set-opts --midebugger-compat=True",
            "description": "Set MIDebugger compatibility"
        }
    ],
    "cwd": "${workspaceFolder}"
}
```