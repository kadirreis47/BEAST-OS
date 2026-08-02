from __future__ import annotations
class ServiceContainer:
    def __init__(self): self._s={}
    def register_singleton(self,k,v): self._s[k]=v
    def resolve(self,k): return self._s[k]
