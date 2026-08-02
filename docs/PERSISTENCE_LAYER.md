# Persistence Layer

BEAST OS kalıcı verileri SQLite üzerinde migration tabanlı olarak saklar.

## Sağlanan Bileşenler

- `Database`: bağlantı, WAL modu, foreign key kontrolü ve transaction yönetimi
- `schema_migrations`: uygulanmış migration sürümlerinin kaydı
- `DailyMetricRepository`: tarih bazlı ölçüm upsert ve aralık sorguları
- `HabitLogRepository`: zaman sıralı alışkanlık kayıtları

## Kullanım

```python
from datetime import date
from beastos.storage import Database, DailyMetric, DailyMetricRepository

database = Database("data/beast.db")
database.migrate()

metrics = DailyMetricRepository(database)
metrics.upsert(DailyMetric(date.today(), "weight", 81.6, "kg"))
```

Migration dosyaları sürüm sırasına göre yalnızca bir kez uygulanır. Yazma işlemleri atomik transaction içinde çalışır; hata halinde rollback yapılır.
