class HabitError(Exception):
    """Base habit-domain exception."""


class HabitNotFoundError(HabitError):
    pass


class InvalidHabitTransitionError(HabitError):
    pass


class DuplicateHabitCompletionError(HabitError):
    pass
