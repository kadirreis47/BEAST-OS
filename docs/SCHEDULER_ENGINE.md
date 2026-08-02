# Scheduler Engine

BEAST OS Scheduler; kalıcı, yeniden başlatılabilir ve deterministik görev çalıştırma altyapısıdır.

## Özellikler

- SQLite tabanlı kalıcı görev deposu
- Timezone-aware UTC zamanlama
- Tekrarlanan interval görevleri
- Üstel gecikmeli ve üst sınırlandırılmış retry politikası
- Başarısız görevleri otomatik devre dışı bırakma
- Thread-safe handler registry
- Aynı process içinde eşzamanlı `run_due` çağrılarını engelleme
- WAL modu ve indeksli due-task sorgusu

## Kullanım

```python
from datetime import UTC, datetime
from beastos.scheduler import (
    IntervalSchedule,
    ScheduledTask,
    SchedulerEngine,
    SQLiteTaskStore,
    TaskRegistry,
)

registry = TaskRegistry()
registry.register("daily_review", lambda payload: print(payload))
store = SQLiteTaskStore("beast.db")
engine = SchedulerEngine(registry, store)

engine.schedule(
    ScheduledTask(
        task_id="daily-review",
        handler_name="daily_review",
        schedule=IntervalSchedule(86_400),
        payload={"scope": "day"},
        next_run_at=datetime.now(UTC),
    )
)

engine.run_due()
```

Görev handler'ları idempotent tasarlanmalıdır. Çoklu process dağıtık kilitleme bu sürümün kapsamı dışındadır.
