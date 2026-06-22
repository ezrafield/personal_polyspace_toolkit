---
name: configure-build-options
description: Creates Polyspace build options for C from a build command or compilation database.
license: MathWorks restricted BSD-3-Clause derivative
---
# Configure C Build Options

Use exactly one input: a C build command or `compile_commands.json`.

With MCP, call `configure_build_options_for_polyspace` using:

- `build_options_file_path` (required)
- exactly one of `build_command` or `ccdb_file_path`
- optional `extra_polyspace_configure_options_file_path`

Filter mixed compilation databases to C translation units and warn about ignored entries. Do not
rewrite the project's compilation database.

On macOS, use a compilation database because build-command tracing is blocked by System Integrity
Protection. If MCP is unavailable, follow `cli-usage.md`.
