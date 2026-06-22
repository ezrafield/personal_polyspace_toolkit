---
name: find-option-documentation
description: Finds installed-release documentation for Polyspace analysis and configuration options.
license: MathWorks restricted BSD-3-Clause derivative
---
# Find Polyspace Option Documentation

1. Call `get_polyspace_documentation` for the exact option when the MCP server is available.
2. Otherwise run the relevant executable with `-help` and search the installed documentation.
3. Report the exact option spelling, accepted values, default, release applicability, and interactions.

Do not invent options or assume current online documentation matches an older installed release.
