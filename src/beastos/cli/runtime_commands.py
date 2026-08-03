
from beastos.runtime.doctor import run_doctor
from beastos.runtime.health import collect_health
from beastos.runtime.version import get_version

def register_runtime_commands(sub):
    version=sub.add_parser("version")
    version.set_defaults(handler=lambda _a: print(f"BEAST OS {get_version()}") or 0)
    health=sub.add_parser("health")
    health.set_defaults(handler=_health)
    doctor=sub.add_parser("doctor")
    doctor.add_argument("--data-dir",default=".beast")
    doctor.set_defaults(handler=_doctor)

def _health(_args):
    report=collect_health()
    for item in report.items:
        print(f"[{'OK' if item.healthy else 'FAIL'}] {item.name}: {item.message}")
    return 0 if report.healthy else 1

def _doctor(args):
    report=run_doctor(args.data_dir)
    print(f"BEAST OS {report.version}")
    for check in report.environment:
        print(f"[{'OK' if check.passed else 'FAIL'}] {check.name}: {check.message}")
    return 0 if report.healthy else 1
