from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta


SPACING_DAYS = (1, 3, 7, 14)


def infer_esat_area(question: dict) -> str:
    if question.get("module") == "physics":
        return "Physics"
    maths2_topics = {"functions", "graphs", "sequences", "trig"}
    if question.get("topic") in maths2_topics:
        return "Maths 2"
    return "Maths 1"


def answer_letters_for(question: dict) -> list[str]:
    qid = question.get("id", "")
    if qid.startswith("tmua_"):
        return list("ABCDEF")
    return list("ABCDEFGH")


def is_review_attempt(row: dict) -> bool:
    return (
        not row.get("correct", False)
        or row.get("lucky_correct", False)
        or row.get("skipped", False)
        or row.get("slow", False)
    )


def is_mastered(row: dict) -> bool:
    return bool(row.get("correct")) and row.get("confidence") == "Confident" and not row.get("slow", False)


def summarize_attempt_rows(rows: list[dict], time_used: float, mode: str = "Timed test", area: str = "All") -> dict:
    n_q = len(rows)
    n_correct = sum(1 for r in rows if r.get("correct"))
    lucky = sum(1 for r in rows if r.get("lucky_correct"))
    adjusted_correct = n_correct - lucky
    return {
        "date": str(date.today()),
        "source": ", ".join(sorted({r.get("source", "") for r in rows if r.get("source")})),
        "mode": mode,
        "area": area,
        "questions_attempted": n_q,
        "correct": n_correct,
        "adjusted_correct": adjusted_correct,
        "time_minutes": round(time_used / 60, 1),
        "score_percent": round(n_correct / n_q * 100, 1) if n_q else 0,
        "adjusted_score_percent": round(adjusted_correct / n_q * 100, 1) if n_q else 0,
        "seconds_per_question": round(time_used / n_q, 1) if n_q else 0,
        "skipped": sum(1 for r in rows if r.get("skipped")),
        "guessed": sum(1 for r in rows if r.get("guessed")),
        "lucky_correct": lucky,
        "slow_review": sum(1 for r in rows if r.get("slow")),
        "topics": ", ".join(sorted({r.get("topic", "") for r in rows if r.get("topic")})),
        "time_used": time_used,
    }


def next_due_date(attempt_date: str, prior_review_count: int = 0) -> str:
    try:
        base = datetime.fromisoformat(attempt_date).date()
    except ValueError:
        base = date.today()
    offset = SPACING_DAYS[min(prior_review_count, len(SPACING_DAYS) - 1)]
    return str(base + timedelta(days=offset))


def build_reattempt_queue(attempts: list[dict], today: date | None = None) -> list[dict]:
    today = today or date.today()
    review_counts: dict[str, int] = defaultdict(int)
    latest_review: dict[str, dict] = {}

    for row in attempts:
        qid = row.get("id")
        if not qid:
            continue
        if is_mastered(row):
            latest_review.pop(qid, None)
            review_counts.pop(qid, None)
            continue
        if is_review_attempt(row):
            count = review_counts[qid]
            due = next_due_date(row.get("date", str(today)), count)
            review_counts[qid] += 1
            latest_review[qid] = {**row, "due_date": due, "review_count": review_counts[qid]}

    due_rows = []
    for row in latest_review.values():
        try:
            due = datetime.fromisoformat(row["due_date"]).date()
        except ValueError:
            due = today
        if due <= today:
            due_rows.append(row)
    return sorted(due_rows, key=lambda r: (r.get("due_date", ""), r.get("topic", ""), r.get("id", "")))


def topic_dashboard_rows(attempts: list[dict]) -> list[dict]:
    stats: dict[str, dict] = defaultdict(lambda: {
        "attempts": 0,
        "correct": 0,
        "adjusted_correct": 0,
        "guessed": 0,
        "skipped": 0,
        "slow": 0,
        "total_time": 0.0,
    })
    for row in attempts:
        topic = row.get("topic") or "unknown"
        s = stats[topic]
        s["attempts"] += 1
        s["correct"] += int(bool(row.get("correct")))
        s["adjusted_correct"] += int(bool(row.get("correct")) and not bool(row.get("lucky_correct")))
        s["guessed"] += int(bool(row.get("guessed")))
        s["skipped"] += int(bool(row.get("skipped")))
        s["slow"] += int(bool(row.get("slow")))
        s["total_time"] += float(row.get("time_seconds", 0) or 0)

    rows = []
    for topic, s in stats.items():
        attempts_n = s["attempts"]
        rows.append({
            "topic": topic,
            "attempts": attempts_n,
            "accuracy_percent": round(s["correct"] / attempts_n * 100, 1),
            "adjusted_accuracy_percent": round(s["adjusted_correct"] / attempts_n * 100, 1),
            "avg_seconds": round(s["total_time"] / attempts_n, 1),
            "guessed": s["guessed"],
            "skipped": s["skipped"],
            "slow": s["slow"],
            "repair_score": (attempts_n - s["adjusted_correct"]) + s["guessed"] + s["skipped"] + s["slow"],
        })
    return sorted(rows, key=lambda r: (r["repair_score"], r["avg_seconds"]), reverse=True)
