# Manual Qwen Code Setup

Qwen Code support is configuration-only. This repository intentionally ships no Qwen extension and
never writes `~/.qwen/settings.json`.

## 1. Configure The Local Model

Merge `examples/qwen-settings.local.example.json` into your user settings. Replace:

- `REPLACE_WITH_OPENAI_COMPATIBLE_BASE_URL` with the later-provided localhost URL, including `/v1`
  when required by the server.
- `REPLACE_WITH_LOCAL_MODEL_ID` with the exact model ID returned by the endpoint.
- Export `LOCAL_QWEN_API_KEY` in the shell or Qwen user environment. Use a harmless placeholder only
  when the localhost server requires no authentication but the client requires a non-empty value.

Keep model-provider configuration at user scope; project-level provider arrays replace user arrays.
Never commit a real API key.

## 2. Configure Polyspace MCP

Merge the `mcpServers.polyspace` entry from the example. Use absolute paths. Keep `trust` false and
the 600,000 millisecond timeout. Omit `--polyspace-root` only when installer-registry autodiscovery is
known to work.

## 3. Install Skills Manually

Copy or link each directory below this repository's `skills/` folder into `~/.qwen/skills/`. Do not
replace an existing same-named skill without reviewing it first.

## 4. Verify

Restart Qwen Code, select the configured model, inspect `qwen mcp list`, and use `/skills` to confirm
the catalog. Then ask for a read-only Polyspace documentation lookup before allowing analysis.

Qwen Code's upstream documentation describes
[local OpenAI-compatible providers](https://github.com/QwenLM/qwen-code/blob/main/docs/users/configuration/model-providers.md#local-self-hosted-models-via-openai-compatible-api),
[MCP configuration](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/mcp.md), and
[skills](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/skills.md).
