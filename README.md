# README #

I use LLDB to debug the Godot engine, and got tired with there being no visualisation for all the built-in types. Here I endeavour to make all of these types visible through the debugger.

# Installation #

Clone this repo somewhere, e.g. ~/GodotFormatters. Then add the following lines to your ~/.lldbinit, or run this line directly in the debug console:

```
command script import ~/GodotFormatters/GodotFormatters.py
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
        "command script import ~/GodotFormatters/GodotFormatters.py"
    ],
    "cwd": "${workspaceFolder}"
}
```