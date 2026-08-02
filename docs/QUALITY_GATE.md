# Quality Gate

Her pull request aşağıdaki kontrolleri geçmelidir:

- Python 3.11, 3.12 ve 3.13 test matrisi
- Ruff statik analiz
- Pytest test paketi
- En az %85 satır kapsamı
- Kurulabilir `src` tabanlı Python paketi

Yerel doğrulama:

```bash
python -m pip install -e ".[dev]"
ruff check src tests
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```
