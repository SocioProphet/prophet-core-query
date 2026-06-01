#!/usr/bin/env python3
"""Validate WallGuard query context examples."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "wallguard-query-context.schema.json"
EXAMPLE_DIR = ROOT / "examples" / "wallguard-query-context"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(instance: dict, schema: dict, *, source_label: str) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        lines = [f"{source_label} failed schema validation:"]
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            lines.append(f" - {location}: {error.message}")
        raise ValueError("\n".join(lines))


def semantic_diagnostics(record: dict) -> list[str]:
    diagnostics: list[str] = []
    decision = record["assembly_decision"]
    assembled = record["assembled"]
    reason = record["reason_code"]
    active_wall = record["active_wall_ref"]

    if record["assembly_phase"] != "pre_context_assembly":
        diagnostics.append("WallGuard query checks must occur before context assembly")

    if decision == "assemble":
        if not assembled:
            diagnostics.append("assemble decision requires assembled=true")
        if reason != "same_wall_allowed":
            diagnostics.append("assemble decision requires same_wall_allowed reason")
        for key in ("context_pack_refs", "catalog_visibility_refs", "retrieval_filter_refs", "memory_gate_refs"):
            for ref in record.get(key, []):
                if "client-b" in ref or "matter-y" in ref or "cross-wall" in ref:
                    diagnostics.append(f"assemble decision contains cross-wall ref in {key}: {ref}")
    else:
        if assembled:
            diagnostics.append("non-assemble decision requires assembled=false")
        if reason == "same_wall_allowed":
            diagnostics.append("non-assemble decision must not use same_wall_allowed")

    if active_wall == "unknown" and decision == "assemble":
        diagnostics.append("unknown active wall cannot assemble context")

    if decision in {"deny", "quarantine", "fail_closed"}:
        if not record.get("receipt_refs"):
            diagnostics.append("denied/quarantined/fail-closed query context requires receipt refs")
        if not record.get("wall_decision_refs"):
            diagnostics.append("denied/quarantined/fail-closed query context requires wall decision refs")

    if not any(ref.startswith("policy-fabric://") for ref in record.get("policy_refs", [])):
        diagnostics.append("policy_refs must include a Policy Fabric ref")
    if not all(ref.startswith("wallguard-receipt://") for ref in record.get("receipt_refs", [])):
        diagnostics.append("receipt_refs must be WallGuard receipt refs")

    return diagnostics


def expected_result(path: Path) -> str:
    return "fail" if ".rejected." in path.name else "pass"


def main() -> int:
    schema = load_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    examples = sorted(EXAMPLE_DIR.glob("*.json"))
    if not examples:
        raise SystemExit("No WallGuard query context examples found")

    results = []
    for path in examples:
        record = load_json(path)
        validate_schema(record, schema, source_label=str(path.relative_to(ROOT)))
        diagnostics = semantic_diagnostics(record)
        actual = "fail" if diagnostics else "pass"
        expected = expected_result(path)
        result = {"example": path.name, "expected": expected, "actual": actual, "diagnostics": diagnostics}
        results.append(result)
        if actual != expected:
            raise ValueError(json.dumps(result, indent=2))

    print(json.dumps({"ok": True, "checked": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
