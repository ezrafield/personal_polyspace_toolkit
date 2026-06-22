# Direct C Analysis

Use `polyspace-as-you-code` for R2026a and later or `polyspace-bug-finder-access` for older
supported releases. Find the executable below `<polyspace-root>/polyspace/bin/`.

```sh
polyspace-as-you-code -sources source.c \
  -checkers-selection-file checkers.xml \
  -options-file build-options.txt \
  -results-dir .polyspace/results
```

Use the installed executable's `-help` output as the source of truth for release-specific options.
Export results only to a temporary or explicitly configured result directory. Do not analyze a
header or a non-C source as a standalone translation unit.
