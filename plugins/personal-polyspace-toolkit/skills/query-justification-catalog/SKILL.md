---
name: query-justification-catalog
description: Queries a Polyspace justification catalog for approved C finding wording.
license: MathWorks restricted BSD-3-Clause derivative
---
# Query Justification Catalog

With MCP, call `query_justification_catalog` using exact comma-separated `FAMILY:ACRONYM` values and
an absolute `catalog_file_path`. Otherwise read `catalog-schema.md` and match deterministically.

Return all matching entries with their status and constraints. A catalog result supplies approved
wording only; invoke `justify-findings` and obtain explicit approval before inserting it.
