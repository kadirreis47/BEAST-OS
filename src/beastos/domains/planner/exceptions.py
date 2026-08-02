class PlannerError(Exception):
    """Base planner-domain exception."""


class PlannerDayNotFoundError(PlannerError):
    pass


class TimeBlockNotFoundError(PlannerError):
    pass


class TimeBlockConflictError(PlannerError):
    pass


class InvalidTimeBlockError(PlannerError):
    pass
