#!/usr/bin/env python3
"""Dialogue Archive v0.1 reference validator (DA-001 through DA-007)."""

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError:
    print(
        "[ERROR] Install dependencies: "
        "python -m pip install 'jsonschema[format]'",
        file=sys.stderr,
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "dialogue-record.schema.json"
DEFAULT_RECORD = ROOT / "examples" / "sample-dialogue.json"


def read_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def schema_error_code(error):
    """Map JSON Schema errors to v0.1 diagnostic categories."""
    path = list(error.absolute_path)
    field = str(path[0]) if path else ""

    if not field and error.validator == "required":
        for name in (
            "dialogue_id",
            "archive_version",
            "metadata",
            "messages",
            "question_links",
            "visibility",
        ):
            if f"'{name}'" in error.message:
                field = name
                break

    return {
        "dialogue_id": "INVALID_DIALOGUE_ID",
        "archive_version": "INVALID_ARCHIVE_VERSION",
        "metadata": "INVALID_METADATA",
        "messages": "INVALID_MESSAGE",
        "question_links": "INVALID_QUESTION_LINK",
        "visibility": "INVALID_VISIBILITY",
    }.get(field, "SCHEMA_VALIDATION_ERROR")


def validate_record(record, schema_validator, seen_dialogues):
    """Return a list of (error_code, detail) pairs."""

    schema_errors = sorted(
        schema_validator.iter_errors(record),
        key=lambda error: (
            tuple(map(str, error.absolute_path)),
            error.message,
        ),
    )

    if schema_errors:
        # Validate structure before inspecting nested data.
        error = schema_errors[0]
        return [(schema_error_code(error), error.message)]

    errors = []

    # DA-002: Dialogue identifiers must be unique.
    dialogue_id = record["dialogue_id"]

    if dialogue_id in seen_dialogues:
        errors.append((
            "DUPLICATE_DIALOGUE_ID",
            f"{dialogue_id!r} already appeared",
        ))
    else:
        seen_dialogues.add(dialogue_id)

    # DA-003: Message identifiers must be unique.
    message_ids = set()

    for message in record["messages"]:
        message_id = message["message_id"]

        if message_id in message_ids:
            errors.append((
                "DUPLICATE_MESSAGE_ID",
                f"duplicate message_id: {message_id!r}",
            ))

        message_ids.add(message_id)

    # DA-005: Question links must reference existing messages.
    for link in record["question_links"]:
        if link["message_id"] not in message_ids:
            errors.append((
                "UNKNOWN_MESSAGE_REFERENCE",
                f"question {link['question_id']!r} references "
                f"unknown message {link['message_id']!r}",
            ))

    # External question IDs are opaque.
    # No QuestionTube lookup is performed.

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate Dialogue Archive v0.1 records"
    )

    parser.add_argument(
        "records",
        nargs="*",
        type=Path,
        help=(
            "JSON record files "
            "(default: examples/sample-dialogue.json)"
        ),
    )

    args = parser.parse_args()
    paths = args.records or [DEFAULT_RECORD]

    # Load and verify the JSON Schema.
    try:
        schema = read_json(SCHEMA_PATH)

        Draft202012Validator.check_schema(schema)

        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )

    except (OSError, ValueError, SchemaError) as exc:
        print(
            f"[ERROR] Cannot load a valid schema: {exc}",
            file=sys.stderr,
        )
        return 2

    seen_dialogues = set()
    passed = 0
    failed = 0

    for path in paths:
        try:
            record = read_json(path)

        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
        ) as exc:
            print(f"[FAIL] {path}: INVALID_JSON: {exc}")
            failed += 1
            continue

        errors = validate_record(
            record,
            validator,
            seen_dialogues,
        )

        if errors:
            failed += 1

            for code, detail in errors:
                print(
                    f"[FAIL] {path}: {code}: {detail}"
                )

        else:
            passed += 1
            print(
                f"[PASS] {path}: {record['dialogue_id']}"
            )

    print(
        f"\nDialogue Archive v0.1: "
        f"{passed} PASS, {failed} FAIL"
    )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
