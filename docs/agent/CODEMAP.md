# Code Map

Generated from the current `src/` directory by `scripts/generate_codemap.py`.

Use this for quick orientation, then confirm with Semble, `rg`, module cards, and source reads.

## src/personal_polyspace_toolkit/
Purpose: Deterministic Polyspace discovery, setup, client integration, configuration, and state.

Files:
- `src/personal_polyspace_toolkit/__init__.py`
- `src/personal_polyspace_toolkit/c_sources.py`
- `src/personal_polyspace_toolkit/cli.py`
- `src/personal_polyspace_toolkit/clients.py`
- `src/personal_polyspace_toolkit/constants.py`
- `src/personal_polyspace_toolkit/discovery.py`
- `src/personal_polyspace_toolkit/errors.py`
- `src/personal_polyspace_toolkit/installer.py`
- `src/personal_polyspace_toolkit/project_config.py`
- `src/personal_polyspace_toolkit/releases.py`
- `src/personal_polyspace_toolkit/state.py`

Exported symbols:
- `HostPlatform`
- `OwnershipConflict`
- `PolyspaceInstallation`
- `ProjectConfig`
- `ReleaseAsset`
- `ServerSpec`
- `ToolkitError`
- `atomic_write_text`
- `backup_file`
- `binary_path`
- `c_translation_units_from_database`
- `codex_config_path`
- `desired_codex_entry`
- `detect_platform`
- `discover_polyspace`
- `doctor_report`
- `download_verified`
- `empty_state`
- `load_project_config`
- `load_state`
- `main`
- `read_polyspace_release`
- `register_claude`
- `register_codex`
- `release_asset`
- `release_key`
- `release_url`
- `save_state`
- `server_spec`
- `setup`
- `setup_plan`
- `sha256_file`
- `sha256_tree`
- `state_dir`
- `translation_units_for_header`
- `uninstall`
- `unregister_claude`
- `unregister_codex`
- `validate_supported_release`
- `verify`
- `verify_claude`
- `verify_codex`
- `verify_qwen`

Important classes/functions:
- class `HostPlatform`
- class `OwnershipConflict`
- class `PolyspaceInstallation`
- class `ProjectConfig`
- class `ReleaseAsset`
- class `ServerSpec`
- class `ToolkitError`
- function `_claude_snapshot`
- function `_default_open`
- function `_install_skills`
- function `_marketplace_name_present`
- function `_parser`
- function `_print`
- function `_probe_binary`
- function `_register_claude_marketplace`
- function `_registry_candidates`
- function `_reject_cpp`
- function `_remove_skills`
- function `_require_string`
- function `_root_from_binary`
- function `_roots_from_registry`
- function `_run`
- function `_skill_destination`
- function `_skills_root`
- function `atomic_write_text`
- function `backup_file`
- function `binary_path`
- function `c_translation_units_from_database`
- function `codex_config_path`
- function `desired_codex_entry`
- function `detect_platform`
- function `discover_polyspace`
- function `doctor_report`
- function `download_verified`
- function `empty_state`
- function `load_project_config`
- function `load_state`
- function `main`
- function `read_polyspace_release`
- function `register_claude`
- function `register_codex`
- function `release_asset`
- function `release_key`
- function `release_url`
- function `save_state`
- function `server_spec`
- function `setup`
- function `setup_plan`
- function `sha256_file`
- function `sha256_tree`
- function `state_dir`
- function `translation_units_for_header`
- function `uninstall`
- function `unregister_claude`
- function `unregister_codex`
- function `validate_supported_release`
- function `verify`
- function `verify_claude`
- function `verify_codex`
- function `verify_qwen`

Public APIs:
- `src/personal_polyspace_toolkit/c_sources.py` -> `c_translation_units_from_database`, `translation_units_for_header`
- `src/personal_polyspace_toolkit/cli.py` -> `main`
- `src/personal_polyspace_toolkit/clients.py` -> `ServerSpec`, `codex_config_path`, `desired_codex_entry`, `register_claude`, `register_codex`, `server_spec`, `unregister_claude`, `unregister_codex`, `verify_claude`, `verify_codex`, `verify_qwen`
- `src/personal_polyspace_toolkit/constants.py` -> `ReleaseAsset`
- `src/personal_polyspace_toolkit/discovery.py` -> `HostPlatform`, `PolyspaceInstallation`, `detect_platform`, `discover_polyspace`, `doctor_report`, `read_polyspace_release`, `release_key`, `validate_supported_release`
- `src/personal_polyspace_toolkit/errors.py` -> `OwnershipConflict`, `ToolkitError`
- `src/personal_polyspace_toolkit/installer.py` -> `setup`, `setup_plan`, `uninstall`, `verify`
- `src/personal_polyspace_toolkit/project_config.py` -> `ProjectConfig`, `load_project_config`
- `src/personal_polyspace_toolkit/releases.py` -> `backup_file`, `download_verified`, `release_asset`, `release_url`
- `src/personal_polyspace_toolkit/state.py` -> `atomic_write_text`, `binary_path`, `empty_state`, `load_state`, `save_state`, `sha256_file`, `sha256_tree`, `state_dir`

Dependency edges:
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/clients`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/constants`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/discovery`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/errors`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/installer`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/project_config`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/releases`
- `src/personal_polyspace_toolkit` -> `src/personal_polyspace_toolkit/state`

Tests:
- `tests/integration/test_cli.py`
- `tests/integration/test_installer.py`
- `tests/unit/test_c_sources.py`
- `tests/unit/test_clients.py`
- `tests/unit/test_discovery.py`
- `tests/unit/test_project_config.py`
- `tests/unit/test_releases.py`

Risk notes:
- Public exports may be imported by other modules; confirm references before renaming.
- Public API or schema changes should be reflected in specs and tests.
- Dependency edges are import hints, not a full call graph; verify behavior in source.
