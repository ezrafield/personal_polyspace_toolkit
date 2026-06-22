---
name: configure-checkers
description: Creates a Polyspace checker selection from explicit MISRA C, CERT C, CWE, or defect profiles.
license: MathWorks restricted BSD-3-Clause derivative
---
# Configure C Checkers

Read the non-empty `profiles` array in `.polyspace-toolkit.json`. Never infer a standard.

With MCP, call `configure_checkers_for_polyspace` with the configured XML output path and only the
selected parameters:

- `misra_c_2012: "all"`
- `misra_c_2023: "all"`
- `cert_c: "all"`
- `cwe: "all"`
- `polyspace_defects: "all"`

Use `launch_checkers_selection_ui` only when explicitly requested; it is mutually exclusive with
profile parameters. For `custom`, require an existing user-owned checkers file.

If MCP is unavailable, follow `cli-usage.md`. Validate that the resulting XML exists before analysis.
