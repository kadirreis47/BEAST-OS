# Command Bus

BEAST OS komut yazma işlemlerini tek bir senkron dispatch katmanından geçirir.

## Özellikler

- Komut türü başına tek handler
- Thread-safe kayıt ve çözümleme
- Handler değiştirme ve kaldırma
- Sıralı middleware pipeline
- UTC zaman damgalı ve benzersiz kimlikli komutlar
- Açık exception hiyerarşisi

## Kullanım

```python
from dataclasses import dataclass
from beastos.core.commands import Command, CommandBus

@dataclass(frozen=True, slots=True, kw_only=True)
class CompleteHabit(Command):
    habit_id: str

class CompleteHabitHandler:
    def handle(self, command: CompleteHabit) -> None:
        ...

bus = CommandBus()
bus.register(CompleteHabit, CompleteHabitHandler())
bus.dispatch(CompleteHabit(habit_id="morning-run"))
```

Komutlar sistem durumunu değiştiren işlemler içindir. Veri okuma işlemleri ayrı Query Bus katmanında tutulmalıdır.
