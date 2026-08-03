# Architecture Quality Gate

Architecture Quality Gate, BEAST OS katmanları arasındaki bağımlılık
kurallarını otomatik olarak doğrular.

## Kontroller

- Domain katmanı presentation veya CLI katmanını içe aktaramaz.
- Analytics katmanı CLI katmanını içe aktaramaz.
- Storage katmanı presentation katmanını içe aktaramaz.
- Python modülleri varsayılan olarak 500 satırı aşamaz.
- Kaynak dosyalardaki sözdizimi hataları raporlanır.

## Yerel kullanım

```powershell
python -m beastos.quality.runner src
pytest -q tests/test_architecture_quality_gate.py
```

## CI

`.github/workflows/architecture-quality.yml` her push ve pull request
üzerinde kalite kapısını çalıştırır.

## Satır sonları

`.gitattributes`, Python ve dokümantasyon dosyalarını LF biçiminde
standartlaştırır. Windows PowerShell ve batch dosyaları CRLF kullanır.
