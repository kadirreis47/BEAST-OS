# Configuration System

BEAST OS yapılandırması düşük öncelikten yüksek önceliğe doğru kaynaklar eklenerek oluşturulur. Son eklenen kaynak önceki değerleri recursive olarak ezer.

```python
from beastos.core.config import ConfigurationLoader, EnvironmentSource, TomlSource

settings = (
    ConfigurationLoader()
    .add_source(TomlSource("config/default.toml"))
    .add_source(TomlSource("config/local.toml", optional=True))
    .add_source(EnvironmentSource(prefix="BEAST_"))
    .require("database.url", "security.secret")
    .load()
)

workers = settings.get_value("runtime.workers", int, default=4)
```

## Ortam değişkenleri

Çift alt çizgi iç içe alan oluşturur:

```text
BEAST_DATABASE__PORT=5432
BEAST_FEATURES__ENABLED=true
```

Değerler JSON kurallarıyla ayrıştırılır. Sayılar, boolean, null, dizi ve nesneler gerçek tipleriyle yüklenir; diğer değerler string kalır.

## Güvenlik

`Settings.redacted()`; anahtar adında `password`, `secret`, `token`, `api_key` veya `private_key` bulunan değerleri maskeler. Ham ayarlar loglanmamalıdır.

## Davranış garantileri

- Kaynak sırası deterministiktir.
- Ayar snapshot'ı immutable ve giriş verisinden bağımsızdır.
- Eksik zorunlu alanlar tek hatada topluca bildirilir.
- JSON/TOML okuma hataları domain exception olarak sunulur.
- Runtime bağımlılığı yoktur; yalnızca Python standard library kullanılır.
