
from .scores import AnalyticsSnapshot

def generate(snapshot:AnalyticsSnapshot)->list[str]:
    tips=[]
    if snapshot.goal_score<60:
        tips.append("Goal completion is below target.")
    if snapshot.habit_score<70:
        tips.append("Increase daily habit consistency.")
    if snapshot.focus_score<50:
        tips.append("Schedule longer focus sessions.")
    if snapshot.planner_completion<70:
        tips.append("Finish more planned blocks.")
    if not tips:
        tips.append("Excellent consistency.")
    return tips
