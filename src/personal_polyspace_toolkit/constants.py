"""Stable product constants and the tested MCP release manifest."""

from __future__ import annotations

from dataclasses import dataclass

GITHUB_REPOSITORY = "mathworks/polyspace-agentic-toolkit"
DEFAULT_MCP_VERSION = "v1.1.1"
STATE_SCHEMA_VERSION = 1
PROJECT_SCHEMA_VERSION = 1

SUPPORTED_PROFILES = frozenset(
    {
        "misra-c-2012",
        "misra-c-2023",
        "cert-c",
        "cwe",
        "polyspace-defects",
        "custom",
    }
)


@dataclass(frozen=True)
class ReleaseAsset:
    """A verified binary asset for one OS and architecture."""

    name: str
    sha256: str


TESTED_RELEASES: dict[str, dict[tuple[str, str], ReleaseAsset]] = {
    "v1.1.1": {
        ("linux", "x86_64"): ReleaseAsset(
            "polyspace-mcp-server-glnxa64",
            "8cb892bf1045f6f1aab20438bee44394965713d5d66f709638b1d20f1be6e7e3",
        ),
        ("macos", "arm64"): ReleaseAsset(
            "polyspace-mcp-server-maca64",
            "de914e0c0ccab7106b02be38eb20d1eb018cc345c7ec82f8555bc019eedf3feb",
        ),
        ("macos", "x86_64"): ReleaseAsset(
            "polyspace-mcp-server-maci64",
            "0d2ca6b8025bac83efc8a2a775b2d48bb962fe8f30b55fe474cdd34c4c7f9f94",
        ),
        ("windows", "x86_64"): ReleaseAsset(
            "polyspace-mcp-server-win64.exe",
            "affe106247b5a1830b02379afa07738a203523bfd51bf3d3404ae3b8af1b257e",
        ),
    }
}

MCP_TOOL_NAMES = (
    "run_polyspace_as_you_code",
    "configure_build_options_for_polyspace",
    "configure_checkers_for_polyspace",
    "get_polyspace_documentation",
    "query_justification_catalog",
)

PRODUCT_SKILLS = (
    "toolkit-setup",
    "c-compliance-loop",
    "run-analysis",
    "fix-findings",
    "justify-findings",
    "configure-build-options",
    "configure-checkers",
    "find-checker-documentation",
    "find-option-documentation",
    "query-justification-catalog",
    "generate-c-pstunit-tests",
)
