# Domain Event Pipeline

BEAST OS domain modülleri arasındaki senkron, süreç içi olay iletişimini sağlar.

## Özellikler

- Immutable ve UTC zaman damgalı `DomainEvent`
- Correlation ve causation kimlikleri
- Thread-safe handler kaydı
- Base-event aboneliği ile alt sınıf olaylarını dinleme
- Middleware pipeline
- Duplicate handler koruması
- Handler kaldırma ve sayaç API'si
- Fail-fast veya toplu hata raporlama
- Immutable metadata snapshot'ı

## Kullanım

```python
from dataclasses import dataclass
from beastos.core.events import DomainEvent, DomainEventPipeline

@dataclass(frozen=True, slots=True, kw_only=True)
class GoalCompleted(DomainEvent):
    goal_id: str

pipeline = DomainEventPipeline()
pipeline.subscribe(GoalCompleted, lambda event: print(event.goal_id))
pipeline.publish(GoalCompleted(goal_id="goal-42"))
```
