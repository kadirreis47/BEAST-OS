# Goal Engine

Goal Engine, BEAST OS hedef yaşam döngüsünü yöneten domain katmanıdır.

## Durumlar

`draft -> active -> paused -> active -> completed -> archived`

## Özellikler

- Immutable goal modeli
- 0-100 ilerleme doğrulaması
- Öncelik ve hedef tarih desteği
- Gecikmiş hedef tespiti
- Thread-safe repository
- Domain event üretimi
- Durum filtreleme
- Tamamlanma ve gecikme istatistikleri

## Kullanım

```python
from beastos.domains.goals import GoalService, InMemoryGoalRepository

service = GoalService(InMemoryGoalRepository())
goal = service.create_goal(title="Launch BEAST OS")
service.update_progress(goal.id, 25)
```
