# Dependency Injection Container

BEAST OS çekirdek servisleri `ServiceContainer` üzerinden kaydedilir ve çözülür.

## Desteklenen yaşam döngüleri

- `Lifetime.SINGLETON`: İlk çözümlemede oluşturulur ve yeniden kullanılır.
- `Lifetime.TRANSIENT`: Her çözümlemede yeni örnek oluşturulur.

## Örnek

```python
from beastos.core.container import Lifetime, ServiceContainer

container = ServiceContainer()
container.register_type(Clock, SystemClock, lifetime=Lifetime.SINGLETON)
container.register_type(DailyReviewService)
review = container.resolve(DailyReviewService)
```

Constructor injection yalnızca açık tip açıklamalarını kabul eder. Kayıtsız servisler ve dairesel bağımlılıklar açıklayıcı istisnalar üretir.
