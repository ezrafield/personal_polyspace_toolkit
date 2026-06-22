# Direct Build Configuration

From a compilation database:

```sh
polyspace-configure -compilation-database compile_commands.json \
  -output-options-file build-options.txt -no-sources
```

From a build command on supported hosts:

```sh
polyspace-configure -build-command "make" \
  -output-options-file build-options.txt -no-sources
```

`-no-sources` is required because analysis supplies one C translation unit separately. Confirm that
the output contains the intended compiler, include paths, defines, target, and C language mode.
