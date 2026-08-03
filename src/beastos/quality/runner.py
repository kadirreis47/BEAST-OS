from __future__ import annotations

from pathlib import Path

from .contracts import ArchitectureContract, validate_architecture


def run_quality_gate(
    source_root: str | Path = "src",
) -> int:
    contract = ArchitectureContract(
        source_root=Path(source_root),
    )
    report = validate_architecture(contract)

    print(f"Checked files: {report.checked_files}")

    if report.passed:
        print("Architecture quality gate: PASSED")
        return 0

    print("Architecture quality gate: FAILED")
    for violation in report.violations:
        location = (
            f"{violation.file}:{violation.line}"
            if violation.line is not None
            else violation.file
        )
        print(
            f"- [{violation.rule}] "
            f"{location} — {violation.detail}"
        )

    return 1


if __name__ == "__main__":
    raise SystemExit(run_quality_gate())
