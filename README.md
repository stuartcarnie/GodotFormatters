# README #

I use LLDB to debug the Godot engine, and got tired with there being no visualization for all the built-in types. Here I endeavor to make all of these types visible through the debugger.

# Installation #

Clone this repo somewhere, e.g. ~/GodotFormatters. Then add the following lines to your ~/.lldbinit, or run this line directly in the debug console:

```
command script import ~/GodotFormatters/lldb_godot_formatters.py
```

You can also include it in a launch.json configuration for a [codelldb](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) debug configuration by putting it in the `initCommands` section, like so:

```json
{
    "name": "(codelldb) Run tests (editor DEBUG)",
    "type": "lldb",
    "request": "launch",
    "program": "${workspaceFolder}/bin/<godot_bin>",
    "args": [
        "--test"
    ],
    "initCommands": [
        "command script import ~/GodotFormatters/lldb_godot_formatters.py"
    ],
    "cwd": "${workspaceFolder}"
}
```

It's also possible to use it with the official Microsoft C++ extension debugger (i.e. `cppdbg`), but it is generally recommended to use codelldb instead:
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
            "text": "command script import ~/GodotFormatters/lldb_godot_formatters.py",
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