
from .models import PlannerDay,TimeBlock
class PlannerService:
    def add_block(self,planner:PlannerDay,block:TimeBlock)->None:
        planner.blocks.append(block)
    def completed(self,planner:PlannerDay):
        return [b for b in planner.blocks if b.completed]
