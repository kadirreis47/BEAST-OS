# Application Bootstrap

Application Bootstrap, BEAST OS servislerini tek giriş noktasından
başlatır ve veri dizini ile SQLite veritabanını hazırlar.

## Ortam değişkenleri

```powershell
$env:BEAST_DATA_DIR = "C:\BEAST\data"
$env:BEAST_DATABASE_PATH = "C:\BEAST\data\beast.db"
```

## Kullanım

```python
from beastos.application import bootstrap_application

application = bootstrap_application()
latest = application.dashboard_repository.latest()
```

## CLI

`python -m beastos.cli dashboard` komutu en son kalıcı dashboard
snapshot kaydını okuyarak sunum modelini konsola yazar.
