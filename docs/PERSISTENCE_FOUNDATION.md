# Persistence Foundation

EPIC 1 / BUILD #041, BEAST OS için ortak SQLite persistence standardını
oluşturur.

## Bileşenler

- `SQLiteDatabase`: bağlantı, WAL, foreign key ve transaction yönetimi
- `MigrationManager`: sıralı migration çalıştırma ve checksum doğrulama
- `SQLiteRepository`: repository taban sınıfı
- `SQLiteUnitOfWork`: transaction sınırı
- `CORE_MIGRATIONS`: Goal, Habit ve Planner tabloları

## Kullanım

```python
from beastos.storage.sqlite import SQLiteDatabase, MigrationManager
from beastos.storage.sqlite.schema import CORE_MIGRATIONS

database = SQLiteDatabase(".beast/beast.db")
MigrationManager(database, CORE_MIGRATIONS).migrate()
```

## Güvenlik

Uygulanmış migration SQL'i değiştirilirse checksum doğrulaması migration
çalışmasını durdurur. Böylece sessiz şema bozulmaları önlenir.
