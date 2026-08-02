from src.beastos.core.service_container import ServiceContainer

def test_sc():
 c=ServiceContainer();o=object();c.register_singleton("x",o);assert c.resolve("x") is o
