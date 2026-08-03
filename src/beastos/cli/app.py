from __future__ import annotations

import argparse
from collections.abc import Sequence

from .commands import register_commands
from .dashboard_commands import register_dashboard_commands
from .runtime_commands import register_runtime_commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="beast")
    subparsers = parser.add_subparsers(dest="command")

    register_commands(subparsers)
    register_dashboard_commands(subparsers)
    register_runtime_commands(subparsers)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)

    if handler is None:
        parser.print_help()
        return 0

    return int(handler(args) or 0)
