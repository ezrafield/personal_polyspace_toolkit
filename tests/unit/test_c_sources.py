import json
from pathlib import Path

from personal_polyspace_toolkit.c_sources import (
    c_translation_units_from_database,
    translation_units_for_header,
)


def test_filters_mixed_compilation_database_and_resolves_header(tmp_path: Path) -> None:
    c_source = tmp_path / "main.c"
    other_source = tmp_path / "legacy.cc"
    header = tmp_path / "module.h"
    c_source.write_text('#include "module.h"\nint main(void) { return 0; }\n', encoding="utf-8")
    other_source.write_text("ignored", encoding="utf-8")
    header.write_text("int function(void);\n", encoding="utf-8")
    database = tmp_path / "compile_commands.json"
    database.write_text(
        json.dumps(
            [
                {"directory": str(tmp_path), "file": "main.c", "command": "cc -c main.c"},
                {"directory": str(tmp_path), "file": "legacy.cc", "command": "other"},
            ]
        ),
        encoding="utf-8",
    )

    units, ignored = c_translation_units_from_database(database)

    assert units == [c_source.resolve()]
    assert ignored == [other_source.resolve()]
    assert translation_units_for_header(header, units) == [c_source.resolve()]
