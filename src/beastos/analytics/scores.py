
from dataclasses import dataclass

@dataclass(slots=True,frozen=True)
class AnalyticsSnapshot:
    goals_completed:int
    goals_total:int
    habits_completed:int
    habits_target:int
    planner_completion:float
    focus_minutes:int

    @property
    def goal_score(self)->float:
        return round((self.goals_completed/max(self.goals_total,1))*100,2)

    @property
    def habit_score(self)->float:
        return round((self.habits_completed/max(self.habits_target,1))*100,2)

    @property
    def focus_score(self)->float:
        return min(round(self.focus_minutes/3,2),100)

    @property
    def productivity(self)->float:
        return round(
            self.goal_score*0.35+
            self.habit_score*0.25+
            self.planner_completion*0.20+
            self.focus_score*0.20,2
        )
