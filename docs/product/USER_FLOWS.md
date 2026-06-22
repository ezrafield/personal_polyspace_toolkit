# User Flows

## Install
1. User runs `doctor` and reviews detected prerequisites.
2. User previews setup with `--dry-run`.
3. CLI downloads the pinned asset, verifies its digest, configures selected clients, installs skills,
   and writes ownership state.
4. User restarts the client and runs `verify`.

## Configure A C Project
1. User explicitly selects checker profiles.
2. User commits `.polyspace-toolkit.json` with project-relative paths.
3. Agent creates or validates checker and build-option files.

## Remediate Findings
1. Agent analyzes selected `.c` translation units.
2. Agent explains findings using installed-release documentation.
3. Agent applies real fixes, compiles, tests, and re-analyzes.
4. Any proposed justification is shown exactly and waits for approval.

## Generate Tests
1. Agent proposes a C PSTUnit test plan and waits for approval.
2. Agent writes and builds the test.
3. Agent shows the executable command and waits again before execution.

## Remove
1. CLI confirms current client entries and skills still match installed hashes.
2. CLI removes owned state and restores safe backups.
3. Drifted user files are left untouched and reported as conflicts.
