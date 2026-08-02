
from datetime import date,time
from beastos.domains.planner.models import PlannerDay,TimeBlock
from beastos.domains.planner.service import PlannerService
def test_score():
 p=PlannerDay(date.today())
 s=PlannerService()
 s.add_block(p,TimeBlock(time(9),time(10),"Deep Work",completed=True))
 s.add_block(p,TimeBlock(time(10),time(11),"Mail"))
 assert p.score()==50.0
