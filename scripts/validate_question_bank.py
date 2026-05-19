"""
Validate data/questions.json and image coverage.

Run from the project root:
    python scripts/validate_question_bank.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "questions.json"


def question_number(qid: str) -> int:
    return int(qid.rsplit("_q", 1)[1])


def source_key(qid: str) -> str:
    return qid.rsplit("_q", 1)[0]


def main() -> int:
    if not DATA_FILE.exists():
        print(f"Missing {DATA_FILE}")
        return 1

    questions = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ids = [q["id"] for q in questions]
    duplicate_ids = [qid for qid, count in Counter(ids).items() if count > 1]
    missing_answers = [q for q in questions if not q.get("answer")]
    missing_images = [q for q in questions if not (ROOT / q["image"]).exists()]
    missing_exam_notes = [q for q in questions if not q.get("exam_note")]

    by_source: dict[str, list[int]] = defaultdict(list)
    for q in questions:
        by_source[source_key(q["id"])].append(question_number(q["id"]))

    gaps = {}
    for key, nums in sorted(by_source.items()):
        if not nums:
            continue
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        if missing:
            gaps[key] = missing

    answer_counts = Counter(q.get("answer", "") or "<missing>" for q in questions)
    topic_counts = Counter(q.get("topic", "<missing>") for q in questions)
    module_counts = Counter(q.get("module", "<missing>") for q in questions)

    print("Question bank validation")
    print("========================")
    print(f"Records: {len(questions)}")
    print(f"Usable with answers: {len(questions) - len(missing_answers)}")
    print(f"Missing answers: {len(missing_answers)}")
    print(f"Missing images: {len(missing_images)}")
    print(f"Missing exam notes: {len(missing_exam_notes)}")
    print(f"Duplicate ids: {len(duplicate_ids)}")
    print()

    print("Modules:")
    for module, count in module_counts.most_common():
        print(f"  {module}: {count}")
    print()

    print("Top topics:")
    for topic, count in topic_counts.most_common():
        print(f"  {topic}: {count}")
    print()

    print("Answer distribution:")
    for answer, count in sorted(answer_counts.items()):
        print(f"  {answer}: {count}")
    print()

    if missing_answers:
        print("Missing answer ids:")
        for q in missing_answers:
            print(f"  {q['id']} ({q['source']}, {q['topic']})")
        print()

    if gaps:
        print("Question-number gaps by source:")
        for key, missing in gaps.items():
            print(f"  {key}: {missing}")
        print()

    if missing_images:
        print("Missing image ids:")
        for q in missing_images:
            print(f"  {q['id']} -> {q['image']}")
        print()

    if duplicate_ids:
        print("Duplicate ids:")
        for qid in duplicate_ids:
            print(f"  {qid}")
        print()

    return 1 if duplicate_ids or missing_images else 0


if __name__ == "__main__":
    raise SystemExit(main())
