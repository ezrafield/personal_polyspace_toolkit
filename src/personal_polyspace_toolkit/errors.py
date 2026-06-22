"""Domain errors surfaced by the command-line interface."""


class ToolkitError(RuntimeError):
    """A user-actionable toolkit failure."""


class OwnershipConflict(ToolkitError):
    """A target exists but is not safely owned by this toolkit."""
