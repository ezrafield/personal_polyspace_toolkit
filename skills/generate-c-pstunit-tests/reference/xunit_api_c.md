# PSTUnit C API Reference

Define tests with `PST_TEST(suite, name)`. Use `PST_VERIFY_*` when execution may continue after a
failure and `PST_ASSERT_*` when the test must stop. Consult the installed `pstunit.h` for the exact
typed comparison macros supported by the installed release.

Every C test must be registered:

```c
#include "pstunit.h"

PST_TEST(example, returns_expected_value)
{
    PST_VERIFY_EQ_INT(42, function_under_test());
}

int main(int argc, char **argv)
{
    PST_ADD_TEST(example, returns_expected_value);
    return PST_MAIN(argc, argv);
}
```

Build example for R2026b+:

```sh
cc test_file.c <polyspace-root>/polyspace/pstest/pstunit/src/pstest.c \
  -I<polyspace-root>/polyspace/pstest/pstunit/include -o test_executable
```

Use `pstunit.c` instead of `pstest.c` on earlier supported releases. The installed header and source
remain authoritative.
