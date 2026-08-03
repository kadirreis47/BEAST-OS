from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import ast


@dataclass(frozen=True, slots=True)
class ArchitectureContract:
    source_root: Path
    forbidden_imports: tuple[tuple[str, str], ...] = (
        ("beastos.domains", "beastos.presentation"),
        ("beastos.domains", "beastos.cli"),
        ("beastos.analytics", "beastos.cli"),
        ("beastos.storage", "beastos.presentation"),
    )
    maximum_module_lines: int = 500


@dataclass(frozen=True, slots=True)
class ArchitectureViolation:
    file: str
    rule: str
    detail: str
    line: int | None = None


@dataclass(frozen=True, slots=True)
class QualityReport:
    checked_files: int
    violations: tuple[ArchitectureViolation, ...]

    @property
    def passed(self) -> bool:
        return not self.violations


def validate_architecture(
    contract: ArchitectureContract,
) -> QualityReport:
    python_files = sorted(contract.source_root.rglob("*.py"))
    violations: list[ArchitectureViolation] = []

    for path in python_files:
        relative = path.relative_to(contract.source_root).as_posix()
        module_name = _module_name(contract.source_root, path)
        source = path.read_text(encoding="utf-8")

        violations.extend(
            _validate_module_size(
                relative,
                source,
                contract.maximum_module_lines,
            )
        )
        violations.extend(
            _validate_import_boundaries(
                relative,
                module_name,
                source,
                contract.forbidden_imports,
            )
        )

    return QualityReport(
        checked_files=len(python_files),
        violations=tuple(violations),
    )


def _module_name(source_root: Path, path: Path) -> str:
    relative = path.relative_to(source_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _validate_module_size(
    relative: str,
    source: str,
    maximum_lines: int,
) -> list[ArchitectureViolation]:
    line_count = len(source.splitlines())
    if line_count <= maximum_lines:
        return []
    return [
        ArchitectureViolation(
            file=relative,
            rule="module-size",
            detail=(
                f"module contains {line_count} lines; "
                f"maximum is {maximum_lines}"
            ),
        )
    ]


def _validate_import_boundaries(
    relative: str,
    module_name: str,
    source: str,
    forbidden_imports: tuple[tuple[str, str], ...],
) -> list[ArchitectureViolation]:
    try:
        tree = ast.parse(source, filename=relative)
    except SyntaxError as exc:
        return [
            ArchitectureViolation(
                file=relative,
                rule="syntax",
                detail=exc.msg,
                line=exc.lineno,
            )
        ]

    violations: list[ArchitectureViolation] = []
    imported_modules = _collect_imports(tree)

    for source_prefix, forbidden_prefix in forbidden_imports:
        if not module_name.startswith(source_prefix):
            continue
        for imported_module, line in imported_modules:
            if imported_module.startswith(forbidden_prefix):
                violations.append(
                    ArchitectureViolation(
                        file=relative,
                        rule="dependency-boundary",
                        detail=(
                            f"{module_name} must not import "
                            f"{imported_module}"
                        ),
                        line=line,
                    )
                )

    return violations


def _collect_imports(
    tree: ast.AST,
) -> list[tuple[str, int]]:
    imports: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(
                (alias.name, node.lineno)
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, node.lineno))

    return imports
