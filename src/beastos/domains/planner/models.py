
from dataclasses import dataclass, field
from datetime import date,time
from enum import StrEnum

class BlockType(StrEnum):
    FOCUS="focus"
    TASK="task"
    BREAK="break"

@dataclass(slots=True,frozen=True)
class TimeBlock:
    start: time
    end: time
    title:str
    type:BlockType=BlockType.TASK
    completed:bool=False

@dataclass(slots=True)
class PlannerDay:
    day:date
    blocks:list[TimeBlock]=field(default_factory=list)
    def score(self)->float:
        if not self.blocks:return 0.0
        done=sum(b.completed for b in self.blocks)
        return round(done/len(self.blocks)*100,2)
