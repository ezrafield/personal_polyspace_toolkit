---
name: run-analysis
description: Runs Polyspace as You Code on C translation units for defects and selected C coding standards.
license: MathWorks restricted BSD-3-Clause derivative
---
# Run Polyspace Analysis

## Resolve configuration

1. Prefer `.polyspace-toolkit.json` and resolve paths relative to that file.
2. Otherwise inspect existing Polyspace IDE configuration, `compile_commands.json`, or the build
   system, then ask for missing choices.
3. Require a checkers XML file created from an explicitly selected profile.
4. Accept only a `.c` source file. Headers must be analyzed through a containing translation unit.

## MCP path

When available, call `run_polyspace_as_you_code` with absolute paths:

- `source_file_path` (required)
- `checkers_file_path`
- `build_options_file_path`
- `polyspace_options_file_path`
- `baseline_folder_path_to_use`
- `baseline_folder_path_to_store`

## Direct path

If the MCP server is unavailable, read `cli-usage.md` and use the installed binary. On compilation
failure, read only the relevant section of `polyspace_err.log`, repair build configuration, and retry.

If remediation was requested, invoke `fix-findings`; do not improvise a shortened fix workflow.
