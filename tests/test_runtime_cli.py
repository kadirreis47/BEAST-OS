
from beastos.cli.app import build_parser
from beastos.runtime.health import collect_health

def test_runtime_commands():
    parser=build_parser()
    assert parser.parse_args(["version"]).command=="version"
    assert parser.parse_args(["health"]).command=="health"
    assert parser.parse_args(["doctor"]).command=="doctor"

def test_health():
    assert collect_health().healthy is True
