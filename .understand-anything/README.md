# Understand Anything

This directory documents the local source-code knowledge graph workflow.

Generated graph outputs are ignored by default. The committed files here are setup and policy files only.

## Generate The Graph

Use the installed Understand Anything runtime:

```bash
/understand
```

Or use the project command placeholder:

```bash
make understand
```

## Search The Graph

```bash
make understand-search QUERY="api route"
```

## Open Dashboard

```bash
make understand-dashboard
```

## Committed Files

- `README.md`
- `.understandignore`
- `config.example.json`

## Ignored Generated Files

- `knowledge-graph.json`
- `meta.json`
- `intermediate/`
- `tmp/`
- `*knowledge-graph*.json`

Commit generated graph files only if the team explicitly decides the benefits outweigh repository noise.
