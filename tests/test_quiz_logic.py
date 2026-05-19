import unittest
from datetime import date

from scripts.quiz_logic import (
    answer_letters_for,
    build_reattempt_queue,
    infer_esat_area,
    is_mastered,
    next_due_date,
    summarize_attempt_rows,
)


class QuizLogicTests(unittest.TestCase):
    def test_infer_esat_area(self):
        self.assertEqual(infer_esat_area({"module": "physics", "topic": "mechanics"}), "Physics")
        self.assertEqual(infer_esat_area({"module": "maths", "topic": "graphs"}), "Maths 2")
        self.assertEqual(infer_esat_area({"module": "maths", "topic": "algebra"}), "Maths 1")

    def test_answer_letters_for(self):
        self.assertEqual(answer_letters_for({"id": "tmua_2023_q8"}), list("ABCDEF"))
        self.assertEqual(answer_letters_for({"id": "nsaa_2023_q8"}), list("ABCDEFGH"))

    def test_adjusted_score_excludes_lucky_correct(self):
        rows = [
            {"correct": True, "lucky_correct": False, "guessed": False, "skipped": False, "slow": False, "topic": "algebra", "source": "NSAA"},
            {"correct": True, "lucky_correct": True, "guessed": True, "skipped": False, "slow": False, "topic": "algebra", "source": "NSAA"},
            {"correct": False, "lucky_correct": False, "guessed": False, "skipped": True, "slow": False, "topic": "waves", "source": "NSAA"},
        ]
        summary = summarize_attempt_rows(rows, time_used=270)
        self.assertEqual(summary["correct"], 2)
        self.assertEqual(summary["adjusted_correct"], 1)
        self.assertEqual(summary["skipped"], 1)

    def test_mastered_requires_confident_correct_not_slow(self):
        self.assertTrue(is_mastered({"correct": True, "confidence": "Confident", "slow": False}))
        self.assertFalse(is_mastered({"correct": True, "confidence": "Guess", "slow": False}))
        self.assertFalse(is_mastered({"correct": True, "confidence": "Confident", "slow": True}))

    def test_reattempt_queue_spacing(self):
        self.assertEqual(next_due_date("2026-05-19", 0), "2026-05-20")
        attempts = [
            {"id": "q1", "date": "2026-05-19", "correct": False, "topic": "algebra"},
            {"id": "q2", "date": "2026-05-19", "correct": True, "confidence": "Confident", "slow": False, "topic": "waves"},
        ]
        due = build_reattempt_queue(attempts, today=date(2026, 5, 20))
        self.assertEqual([row["id"] for row in due], ["q1"])


if __name__ == "__main__":
    unittest.main()
