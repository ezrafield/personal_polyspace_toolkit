# MCP Notes

The only product-required MCP server is the official per-user Polyspace server installed by
`polyspace-toolkit setup`. Its five compatible tools are documented in `docs/agent/MCPS.md`.

Do not commit real client configuration or secrets here. Codex and Claude registrations are managed
at user scope. Qwen Code uses the manual non-secret example under `examples/`.

Semble, Serena, RTK, documentation, and repository connectors are optional development aids. They do
not participate in product correctness and must fail open to local scripts and exact `rg` searches.
