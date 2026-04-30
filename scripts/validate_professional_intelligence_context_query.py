#!/usr/bin/env python3
"""Validate Professional Intelligence context-query example."""

from __future__ import annotations

from pathlib import Path
import json

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "professional-intelligence-context-query.schema.json"
EXAMPLE = ROOT / "examples" / "professional-intelligence" / "context-query.example.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    schema = load_json(SCHEMA)
    example = load_json(EXAMPLE)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
    if errors:
        print("Professional Intelligence context query failed validation:")
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            print(f" - {location}: {error.message}")
        return 1

    required_sources = {"sherlock-search", "memory-mesh", "policy-fabric", "contractforge"}
    observed_sources = {step["source"] for step in example["queryPlan"]}
    missing = sorted(required_sources - observed_sources)
    if missing:
        print(f"Context query is missing required sources: {missing}")
        return 1

    for step in example["queryPlan"]:
        if not step.get("evidenceRequired"):
            print(f"Query plan step {step['stepId']} must require evidence")
            return 1
        if not step.get("inputRefs"):
            print(f"Query plan step {step['stepId']} must include inputRefs")
            return 1

    outputs = example["outputs"]
    if not outputs.get("contextPackRefs") or not outputs.get("workroomRefs") or not outputs.get("evidenceRefs"):
        print("Context query outputs must include contextPackRefs, workroomRefs, and evidenceRefs")
        return 1

    print("Professional Intelligence context query validates against schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
