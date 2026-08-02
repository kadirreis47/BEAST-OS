class SchedulerError(Exception):
    """Base scheduler exception."""


class TaskAlreadyRegisteredError(SchedulerError):
    """Raised when a duplicate task identifier is registered."""


class TaskNotFoundError(SchedulerError):
    """Raised when a requested task does not exist."""


class InvalidScheduleError(SchedulerError):
    """Raised when a schedule definition is invalid."""
