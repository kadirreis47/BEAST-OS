
from collections import defaultdict
from collections.abc import Callable

class EventRouter:
    def __init__(self):
        self._routes=defaultdict(list)

    def subscribe(self,event:str,handler:Callable):
        self._routes[event].append(handler)

    def publish(self,event:str,payload):
        for handler in tuple(self._routes[event]):
            handler(payload)
