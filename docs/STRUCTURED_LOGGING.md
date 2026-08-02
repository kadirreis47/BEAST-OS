# Structured Logging

BEAST OS çekirdeği, standart kütüphane tabanlı JSON loglama kullanır.

## Özellikler

- UTC ISO-8601 zaman damgası
- `contextvars` ile request/job/user bağlamı
- İç içe sözlüklerde hassas alan maskeleme
- Exception serialization
- JSON ve düz metin çıktı
- Tekrarlanan yapılandırmada handler çoğalmasını engelleme

## Kullanım

```python
from beastos.core.logging import configure_logging, get_logger, logging_context

configure_logging()
logger = get_logger("scheduler")

with logging_context(request_id="req-42", job_id="daily-review"):
    logger.info("job_started", extra={"event_data": {"attempt": 1}})
```

Hassas alanlar (`password`, `token`, `api_key`, `secret`, `authorization`) otomatik olarak maskelenir.
