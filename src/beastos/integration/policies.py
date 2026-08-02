
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class AutomationPolicy:
    trigger:str
    action:str

DEFAULT_POLICIES=[
    AutomationPolicy("goal.created","planner.create_block"),
    AutomationPolicy("habit.completed","goal.update_progress"),
    AutomationPolicy("planner.completed","analytics.capture"),
    AutomationPolicy("goal.completed","planner.archive_blocks"),
]
