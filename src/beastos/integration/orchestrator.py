
from .event_router import EventRouter
from .policies import DEFAULT_POLICIES

class IntegrationOrchestrator:
    def __init__(self,router:EventRouter):
        self.router=router

    def install_default_policies(self):
        for policy in DEFAULT_POLICIES:
            self.router.subscribe(policy.trigger,lambda payload,a=policy.action:(a,payload))
