# Habit Engine

Habit Engine, BEAST OS alışkanlık yaşam döngüsünü ve tamamlanma kayıtlarını yönetir.

## Özellikler

- Immutable habit modeli
- Günlük ve haftalık frekans
- Active, paused ve archived durumları
- Aynı gün çift kayıt koruması
- Güncel ve en uzun seri hesaplama
- Tamamlanma oranı analizi
- Thread-safe repository
- Domain event üretimi
- Durum bazlı listeleme

## Kullanım

```python
from datetime import date
from beastos.domains.habits import HabitService, InMemoryHabitRepository

service = HabitService(InMemoryHabitRepository())
habit = service.create_habit(name="Read 20 pages")
service.complete(habit.id, date.today())
```
