# Daily Planner Engine

Daily Planner Engine, BEAST OS içindeki zaman bloklarını ve günlük planlama
yaşam döngüsünü yönetir.

## Özellikler

- Timezone-aware zaman blokları
- Focus, task, break, habit ve goal blok tipleri
- Zaman çakışması tespiti
- Günlük ve haftalık tekrar kuralları
- Immutable planner day modeli
- Thread-safe repository
- Blok ekleme, tamamlama ve silme eventleri
- Günlük başarı skoru
- Focus ve toplam planlanan süre analizi
- Tarih aralığı sorguları

## Kullanım

```python
from datetime import datetime, timezone
from beastos.domains.planner import (
    InMemoryPlannerRepository,
    PlannerService,
    TimeBlock,
)

service = PlannerService(InMemoryPlannerRepository())
block = TimeBlock.create(
    title="Deep Work",
    start=datetime(2026, 8, 3, 9, tzinfo=timezone.utc),
    end=datetime(2026, 8, 3, 11, tzinfo=timezone.utc),
)
service.add_block(block)
```
