from pathlib import Path

from beastos.quality import (
    ArchitectureContract,
    validate_architecture,
)
from beastos.quality.runner import run_quality_gate


def write_module(
    root: Path,
    relative: str,
    content: str,
) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_valid_architecture_passes(tmp_path: Path):
    write_module(
        tmp_path,
        "beastos/domains/goals/service.py",
        "from dataclasses import dataclass\n",
    )

    report = validate_architecture(
        ArchitectureContract(source_root=tmp_path)
    )

    assert report.passed is True
    assert report.checked_files == 1


def test_forbidden_import_is_reported(tmp_path: Path):
    write_module(
        tmp_path,
        "beastos/domains/goals/service.py",
        "from beastos.presentation.dashboard import DashboardBuilder\n",
    )

    report = validate_architecture(
        ArchitectureContract(source_root=tmp_path)
    )

    assert report.passed is False
    assert report.violations[0].rule == "dependency-boundary"


def test_large_module_is_reported(tmp_path: Path):
    write_module(
        tmp_path,
        "beastos/application/large.py",
        "\n".join("value = 1" for _ in range(6)),
    )

    report = validate_architecture(
        ArchitectureContract(
            source_root=tmp_path,
            maximum_module_lines=5,
        )
    )

    assert report.passed is False
    assert report.violations[0].rule == "module-size"


def test_syntax_error_is_reported(tmp_path: Path):
    write_module(
        tmp_path,
        "beastos/core/broken.py",
        "def broken(:\n",
    )

    report = validate_architecture(
        ArchitectureContract(source_root=tmp_path)
    )

    assert report.passed is False
    assert report.violations[0].rule == "syntax"


def test_runner_returns_success_for_clean_tree(
    tmp_path: Path,
    capsys,
):
    write_module(
        tmp_path,
        "beastos/core/example.py",
        "VALUE = 1\n",
    )

    exit_code = run_quality_gate(tmp_path)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "PASSED" in output
