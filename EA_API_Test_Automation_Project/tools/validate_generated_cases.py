"""Validate test cases supplied by an AI assistant or written manually.

Usage:
  python tools/validate_generated_cases.py examples/ai_generated_test_cases.json
This tool validates structure and basic quality; it does not prove a test case is correct.
"""
import json
import sys
from pathlib import Path

REQUIRED = {"id", "endpoint", "method", "scenario", "expected_status", "expected_result"}

def validate(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: unable to read valid JSON: {exc}")
        return 2

    if not isinstance(data, list) or not data:
        print("FAIL: top-level value must be a non-empty JSON array")
        return 2

    errors, seen_ids, seen_scenarios = [], set(), set()
    for index, case in enumerate(data):
        prefix = f"case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        missing = REQUIRED - set(case)
        if missing:
            errors.append(f"{prefix}: missing fields {sorted(missing)}")
            continue
        if not isinstance(case["id"], str) or not case["id"].strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif case["id"] in seen_ids:
            errors.append(f"{prefix}: duplicate id {case['id']}")
        seen_ids.add(case["id"])
        if case["method"] not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            errors.append(f"{prefix}: unsupported HTTP method")
        if not isinstance(case["endpoint"], str) or not case["endpoint"].startswith("/"):
            errors.append(f"{prefix}: endpoint must start with '/'")
        if not isinstance(case["expected_status"], int) or not 100 <= case["expected_status"] <= 599:
            errors.append(f"{prefix}: expected_status must be an HTTP status integer")
        if not isinstance(case["scenario"], str) or not case["scenario"].strip():
            errors.append(f"{prefix}: scenario must be descriptive")
        scenario_key = (case.get("method"), case.get("endpoint"), case.get("scenario"))
        if scenario_key in seen_scenarios:
            errors.append(f"{prefix}: duplicate method/endpoint/scenario")
        seen_scenarios.add(scenario_key)
        if not isinstance(case["expected_result"], str) or not case["expected_result"].strip():
            errors.append(f"{prefix}: expected_result must be explicit")

    if errors:
        print("FAIL: validation found issues")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: validated {len(data)} test cases; schema and basic quality checks passed.")
    print("Note: human review is still required to confirm expected behavior is correct.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_generated_cases.py <json-file>")
        raise SystemExit(2)
    raise SystemExit(validate(sys.argv[1]))
