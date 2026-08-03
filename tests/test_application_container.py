
from beastos.application.container import ServiceContainer

def test_container():
    c=ServiceContainer()
    c.register("x",123)
    assert c.has("x")
    assert c.resolve("x")==123
