"""Poller Error Classes."""

class PollerError(Exception):
    """Base Exception class for all errors raised by the poller."""
    pass

class PollerStartupError(PollerError):
    """Poller failed to start."""
    pass

class PollerAPIError(PollerError):
    """Poller had an API communication failure."""
    pass

class PollerValidationError(PollerError):
    """Poller failed to validate a completed form."""
    pass

class PollerDeleteError(PollerAPIError):
    """Poller failed to delete a form over the API."""
    pass

class PollerWorkflowSaveError(PollerError):
    """Poller failed to save a workflow."""
    pass

class PollerWorkflowInstanceDeletedError(PollerError):
    """Associated workflow instance deleted."""
    pass

class PollerFormInError(PollerError):
    """Poller encountered a form in an error state."""
    pass

