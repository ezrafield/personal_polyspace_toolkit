---
name: justify-findings
description: Proposes approval-gated Polyspace source annotations for justified findings in C code.
license: MathWorks restricted BSD-3-Clause derivative
---
# Justify C Findings

Use a source comment only when a finding is a demonstrated false positive, intentional deviation,
or prevented by a documented external constraint.

Line form:

```c
statement; /* polyspace FAMILY:ACRONYM [Justified] "specific reason" */
```

Block form:

```c
/* polyspace-begin FAMILY:ACRONYM [Justified] "specific reason" */
statements;
/* polyspace-end FAMILY:ACRONYM */
```

The family and acronym must exactly match the result. Valid statuses are `Justified`,
`Not a defect`, and `No action planned`; optional severity is `High`, `Medium`, or `Low`.

Before editing, always show:

1. Finding, message, and location.
2. Evidence that a code fix is not appropriate.
3. Proposed concise justification text.
4. Exact annotation and insertion point.

Wait for explicit approval. A justification-catalog match is pre-approved wording, not permission
to edit. Re-run analysis after insertion and confirm the finding is marked justified.
