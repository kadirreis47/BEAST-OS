
from dataclasses import dataclass

@dataclass(slots=True,frozen=True)
class LifeState:
    goals_total:int
    goals_completed:int
    habits_completed_today:int
    planner_completion:float
    focus_minutes:int

    @property
    def productivity_score(self)->float:
        goal_score=(self.goals_completed/max(self.goals_total,1))*40
        planner=self.planner_completion*0.4
        habit=min(self.habits_completed_today*4,20)
        focus=min(self.focus_minutes/12,20)
        return round(goal_score+planner+habit+focus,2)
