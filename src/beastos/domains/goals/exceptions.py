class GoalError(Exception):
    """Base goal-domain exception."""


class GoalNotFoundError(GoalError):
    pass


class InvalidGoalTransitionError(GoalError):
    pass


class InvalidGoalProgressError(GoalError):
    pass
