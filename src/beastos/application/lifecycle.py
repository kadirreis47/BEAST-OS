
from __future__ import annotations

class ApplicationLifecycle:
    def __init__(self):
        self._started=False

    def start(self):
        self._started=True

    def stop(self):
        self._started=False

    @property
    def running(self)->bool:
        return self._started
