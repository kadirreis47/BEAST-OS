
from __future__ import annotations

class ServiceContainer:
    def __init__(self):
        self._services={}

    def register(self,name:str,instance)->None:
        self._services[name]=instance

    def resolve(self,name:str):
        return self._services[name]

    def has(self,name:str)->bool:
        return name in self._services
