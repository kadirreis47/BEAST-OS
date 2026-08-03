# Dashboard ViewModel

Dashboard ViewModel, Analytics Engine çıktısını CLI, API, desktop ve web
arayüzlerinin kullanabileceği kararlı bir sunum modeline dönüştürür.

## Üretilen kartlar

- Productivity
- Goals
- Habits
- Planner
- Focus

## Özellikler

- Immutable dashboard state
- Trend hesaplama
- Progress doğrulama
- Insight taşıma
- Dictionary serialization
- UI katmanından bağımsız yapı

## Kullanım

```python
from beastos.analytics.scores import AnalyticsSnapshot
from beastos.presentation.dashboard import DashboardBuilder

snapshot = AnalyticsSnapshot(
    goals_completed=4,
    goals_total=5,
    habits_completed=6,
    habits_target=8,
    planner_completion=80,
    focus_minutes=240,
)

state = DashboardBuilder().build(snapshot)
```
