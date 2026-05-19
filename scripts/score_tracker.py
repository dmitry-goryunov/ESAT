from pathlib import Path
import csv

DATA_FILE = Path("scores.csv")

HEADERS = [
    "date",
    "source",
    "questions_attempted",
    "correct",
    "time_minutes",
    "score_percent",
    "seconds_per_question",
]

def add_score(date, source, questions_attempted, correct, time_minutes):
    score_percent = round(correct / questions_attempted * 100, 1)
    seconds_per_question = round(time_minutes * 60 / questions_attempted, 1)

    exists = DATA_FILE.exists()

    with DATA_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)

        if not exists:
            writer.writeheader()

        writer.writerow({
            "date": date,
            "source": source,
            "questions_attempted": questions_attempted,
            "correct": correct,
            "time_minutes": time_minutes,
            "score_percent": score_percent,
            "seconds_per_question": seconds_per_question,
        })

if __name__ == "__main__":
    print("Example:")
    print("add_score('2026-05-17', 'Mechanics2 Q1-15', 15, 11, 20)")
