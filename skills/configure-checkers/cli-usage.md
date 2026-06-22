# Direct Checker Configuration

Prefer the Polyspace checker selection UI or an existing team-owned XML file. A minimal file uses
the schema shipped with the installed Polyspace release:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<polyspace_checkers_selection revision="2.0">
  <!-- Add only explicitly selected C checker groups using installed documentation. -->
</polyspace_checkers_selection>
```

Do not guess internal checker identifiers. Use installed documentation or the MCP configuration
tool to populate the file.
