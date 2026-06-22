# Justification Catalog Schema

The catalog is JSON with an `entries` array. Each entry contains the exact `family`, `acronym`,
`status`, and `text`; optional fields may narrow the match by file, function, or project condition.

```json
{
  "entries": [
    {
      "family": "Defect",
      "acronym": "INT_ZERO_DIV",
      "status": "Justified",
      "text": "Denominator validated nonzero by caller"
    }
  ]
}
```

Match family and acronym exactly. Apply optional constraints conjunctively. Do not use fuzzy matching
to justify a different finding.
