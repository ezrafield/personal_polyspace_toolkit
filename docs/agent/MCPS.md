# Polyspace MCP

The toolkit consumes the official per-user Polyspace MCP server binary. It does not implement or
redistribute the server.

Compatible tool names:

1. `run_polyspace_as_you_code`
2. `configure_build_options_for_polyspace`
3. `configure_checkers_for_polyspace`
4. `get_polyspace_documentation`
5. `query_justification_catalog`

Tool names are a compatibility contract. Validate argument details against the tested server release
and installed Polyspace documentation before changing a skill.

The server is registered at user scope for Codex and Claude. Qwen registration is manual and keeps
`trust` false. Telemetry is disabled by default for every generated server command.
