# Query Bus

BEAST OS Query Bus, sistem durumunu değiştirmeyen okuma operasyonlarını tek bir dağıtım katmanında toplar.

## Özellikler

- Query türüne göre tek handler kaydı
- Thread-safe kayıt ve çözümleme
- Generic dönüş tipi
- Middleware pipeline
- Handler değiştirme ve kaldırma
- Açık hata hiyerarşisi
- UUID ve UTC zaman damgalı immutable query modeli

## Kullanım

```python
from dataclasses import dataclass
from beastos.core.query import Query, QueryBus

@dataclass(frozen=True, slots=True, kw_only=True)
class GetDailyScore(Query[int]):
    user_id: int

bus = QueryBus()
bus.register(GetDailyScore, lambda query: 87)
score = bus.ask(GetDailyScore(user_id=1))
```

Query handler'ları veri okumalıdır. Durum değiştiren işlemler Command Bus üzerinden yürütülmelidir.
