"""
Extract question page images from past paper PDFs.

Run from the project root:
    python scripts/extract_question_images.py

Output: data/images/<id>.png  (one PNG per question entry in MANIFEST)
Then manually verify images and run build_questions.py to generate questions.json.
"""

import json
from pathlib import Path
import pypdfium2 as pdfium

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "data" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Scale factor for rendering (2 = ~144 DPI, 3 = ~216 DPI)
SCALE = 2.5

# ---------------------------------------------------------------------------
# MANIFEST
# Each entry: (id, pdf_path_relative_to_root, page_number_0_indexed)
# Page numbers are 0-indexed (PDF page 1 = index 0).
#
# Strategy file sources for priority questions:
#   strat_NSAA.md  section 6  — year-by-year priority Q lists
#   strat_ENGAA.md section 4  — Part A all + selected Part B
#   strat_TMUA.md  section 4  — priority Q per year
#   strat_PAT.md   section 4  — Q1-Q12 per year
#
# How to find the right page number:
#   Open the PDF, navigate to the question, note the physical page number,
#   subtract 1 for 0-indexed. The cover page is usually page 0.
#
# Format: ("id", "papers/source/file.pdf", page_0indexed)
# ---------------------------------------------------------------------------

MANIFEST = [
    # ── NSAA 2016 ──────────────────────────────────────────────────────────
    # Maths Part A (Q1-18), Physics Part B (Q19-36)
    # Priority Maths: Q7, Q8, Q12, Q14, Q15, Q18
    # Priority Physics: Q21, Q24, Q25, Q26, Q27, Q28, Q32, Q35, Q36
    ("nsaa_2016_q7",  "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 8),
    ("nsaa_2016_q8",  "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 9),
    ("nsaa_2016_q12", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 13),
    ("nsaa_2016_q14", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 15),
    ("nsaa_2016_q15", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 16),
    ("nsaa_2016_q18", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 19),
    ("nsaa_2016_q21", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 22),
    ("nsaa_2016_q24", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 25),
    ("nsaa_2016_q25", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 26),
    ("nsaa_2016_q26", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 27),
    ("nsaa_2016_q27", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 28),
    ("nsaa_2016_q28", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 29),
    ("nsaa_2016_q32", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 33),
    ("nsaa_2016_q35", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 36),
    ("nsaa_2016_q36", "papers/nsaa/NSAA_2016_S1_QuestionPaper.pdf", 37),

    # ── NSAA 2017 ──────────────────────────────────────────────────────────
    ("nsaa_2017_q5",  "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 6),
    ("nsaa_2017_q10", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 11),
    ("nsaa_2017_q12", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 13),
    ("nsaa_2017_q13", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 14),
    ("nsaa_2017_q14", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 15),
    ("nsaa_2017_q15", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 16),
    ("nsaa_2017_q17", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 18),
    ("nsaa_2017_q18", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 19),
    ("nsaa_2017_q19", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 20),
    ("nsaa_2017_q21", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 22),
    ("nsaa_2017_q25", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 26),
    ("nsaa_2017_q28", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 29),
    ("nsaa_2017_q29", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 30),
    ("nsaa_2017_q31", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 32),
    ("nsaa_2017_q33", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 34),
    ("nsaa_2017_q34", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 35),
    ("nsaa_2017_q36", "papers/nsaa/NSAA_2017_S1_QuestionPaper.pdf", 37),

    # ── NSAA 2018 ──────────────────────────────────────────────────────────
    ("nsaa_2018_q4",  "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 5),
    ("nsaa_2018_q6",  "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 7),
    ("nsaa_2018_q7",  "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 8),
    ("nsaa_2018_q8",  "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 9),
    ("nsaa_2018_q14", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 15),
    ("nsaa_2018_q15", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 16),
    ("nsaa_2018_q16", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 17),
    ("nsaa_2018_q18", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 19),
    ("nsaa_2018_q20", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 21),
    ("nsaa_2018_q22", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 23),
    ("nsaa_2018_q24", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 25),
    ("nsaa_2018_q27", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 28),
    ("nsaa_2018_q28", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 29),
    ("nsaa_2018_q31", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 32),
    ("nsaa_2018_q32", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 33),
    ("nsaa_2018_q34", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 35),
    ("nsaa_2018_q35", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 36),
    ("nsaa_2018_q36", "papers/nsaa/NSAA_2018_S1_QuestionPaper.pdf", 37),

    # ── NSAA 2019 ──────────────────────────────────────────────────────────
    ("nsaa_2019_q7",  "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 8),
    ("nsaa_2019_q9",  "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 10),
    ("nsaa_2019_q10", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 11),
    ("nsaa_2019_q14", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 15),
    ("nsaa_2019_q15", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 16),
    ("nsaa_2019_q16", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 17),
    ("nsaa_2019_q17", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 18),
    ("nsaa_2019_q18", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 19),
    ("nsaa_2019_q19", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 20),
    ("nsaa_2019_q21", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 22),
    ("nsaa_2019_q25", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 26),
    ("nsaa_2019_q27", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 28),
    ("nsaa_2019_q29", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 30),
    ("nsaa_2019_q30", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 31),
    ("nsaa_2019_q31", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 32),
    ("nsaa_2019_q32", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 33),
    ("nsaa_2019_q33", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 34),
    ("nsaa_2019_q36", "papers/nsaa/NSAA_2019_S1_QuestionPaper.pdf", 37),

    # ── NSAA 2020 ──────────────────────────────────────────────────────────
    ("nsaa_2020_q3",  "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 4),
    ("nsaa_2020_q4",  "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 5),
    ("nsaa_2020_q7",  "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 8),
    ("nsaa_2020_q11", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 12),
    ("nsaa_2020_q12", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 13),
    ("nsaa_2020_q15", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 16),
    ("nsaa_2020_q17", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 18),
    ("nsaa_2020_q18", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 19),
    ("nsaa_2020_q20", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 21),
    ("nsaa_2020_q21", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 22),
    ("nsaa_2020_q23", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 24),
    ("nsaa_2020_q24", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 25),
    ("nsaa_2020_q27", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 28),
    ("nsaa_2020_q28", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 29),
    ("nsaa_2020_q29", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 30),
    ("nsaa_2020_q30", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 31),
    ("nsaa_2020_q32", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 33),
    ("nsaa_2020_q36", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 37),
    ("nsaa_2020_q37", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 38),
    ("nsaa_2020_q40", "papers/nsaa/NSAA_2020_S1_QuestionPaper.pdf", 41),

    # ── NSAA 2021 ──────────────────────────────────────────────────────────
    ("nsaa_2021_q4",  "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 5),
    ("nsaa_2021_q8",  "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 9),
    ("nsaa_2021_q10", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 11),
    ("nsaa_2021_q11", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 12),
    ("nsaa_2021_q12", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 13),
    ("nsaa_2021_q14", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 15),
    ("nsaa_2021_q15", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 16),
    ("nsaa_2021_q17", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 18),
    ("nsaa_2021_q20", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 21),
    ("nsaa_2021_q21", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 22),
    ("nsaa_2021_q23", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 24),
    ("nsaa_2021_q24", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 25),
    ("nsaa_2021_q28", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 29),
    ("nsaa_2021_q29", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 30),
    ("nsaa_2021_q30", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 31),
    ("nsaa_2021_q31", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 32),
    ("nsaa_2021_q34", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 35),
    ("nsaa_2021_q35", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 36),
    ("nsaa_2021_q36", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 37),
    ("nsaa_2021_q40", "papers/nsaa/NSAA_2021_S1_QuestionPaper.pdf", 41),

    # ── NSAA 2022 ──────────────────────────────────────────────────────────
    ("nsaa_2022_q8",  "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 9),
    ("nsaa_2022_q10", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 11),
    ("nsaa_2022_q12", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 13),
    ("nsaa_2022_q14", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 15),
    ("nsaa_2022_q16", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 17),
    ("nsaa_2022_q18", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 19),
    ("nsaa_2022_q20", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 21),
    ("nsaa_2022_q21", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 22),
    ("nsaa_2022_q23", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 24),
    ("nsaa_2022_q24", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 25),
    ("nsaa_2022_q25", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 26),
    ("nsaa_2022_q26", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 27),
    ("nsaa_2022_q27", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 28),
    ("nsaa_2022_q30", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 31),
    ("nsaa_2022_q31", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 32),
    ("nsaa_2022_q34", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 35),
    ("nsaa_2022_q35", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 36),
    ("nsaa_2022_q37", "papers/nsaa/NSAA_2022_S1_QuestionPaper.pdf", 38),

    # ── NSAA 2023 ──────────────────────────────────────────────────────────
    ("nsaa_2023_q5",  "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 6),
    ("nsaa_2023_q8",  "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 9),
    ("nsaa_2023_q11", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 12),
    ("nsaa_2023_q13", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 14),
    ("nsaa_2023_q14", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 15),
    ("nsaa_2023_q16", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 17),
    ("nsaa_2023_q19", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 20),
    ("nsaa_2023_q20", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 21),
    ("nsaa_2023_q21", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 22),
    ("nsaa_2023_q22", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 23),
    ("nsaa_2023_q24", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 25),
    ("nsaa_2023_q26", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 27),
    ("nsaa_2023_q30", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 31),
    ("nsaa_2023_q31", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 32),
    ("nsaa_2023_q32", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 33),
    ("nsaa_2023_q33", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 34),
    ("nsaa_2023_q35", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 36),
    ("nsaa_2023_q36", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 37),
    ("nsaa_2023_q39", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 40),
    ("nsaa_2023_q40", "papers/nsaa/NSAA_2023_S1_QuestionPaper.pdf", 41),

    # ── ENGAA 2016 ─────────────────────────────────────────────────────────
    ("engaa_2016_q2",  "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 3),
    ("engaa_2016_q4",  "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 5),
    ("engaa_2016_q6",  "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 7),
    ("engaa_2016_q8",  "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 9),
    ("engaa_2016_q10", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 11),
    ("engaa_2016_q12", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 13),
    ("engaa_2016_q14", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 15),
    ("engaa_2016_q16", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 17),
    ("engaa_2016_q20", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 21),
    ("engaa_2016_q22", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 23),
    ("engaa_2016_q23", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 24),
    ("engaa_2016_q28", "papers/engaa/ENGAA_2016_S1_QuestionPaper.pdf", 29),

    # ── ENGAA 2017–2023: Part A questions (all high value) ─────────────────
    # Abbreviated for brevity — add full lists following same pattern above
    ("engaa_2017_q1",  "papers/engaa/ENGAA_2017_S1_QuestionPaper.pdf", 2),
    ("engaa_2017_q2",  "papers/engaa/ENGAA_2017_S1_QuestionPaper.pdf", 3),
    ("engaa_2017_q3",  "papers/engaa/ENGAA_2017_S1_QuestionPaper.pdf", 4),
    ("engaa_2017_q4",  "papers/engaa/ENGAA_2017_S1_QuestionPaper.pdf", 5),
    ("engaa_2017_q5",  "papers/engaa/ENGAA_2017_S1_QuestionPaper.pdf", 6),
    ("engaa_2018_q1",  "papers/engaa/ENGAA_2018_S1_QuestionPaper.pdf", 2),
    ("engaa_2018_q2",  "papers/engaa/ENGAA_2018_S1_QuestionPaper.pdf", 3),
    ("engaa_2018_q3",  "papers/engaa/ENGAA_2018_S1_QuestionPaper.pdf", 4),
    ("engaa_2019_q1",  "papers/engaa/ENGAA_2019_S1_QuestionPaper.pdf", 2),
    ("engaa_2019_q2",  "papers/engaa/ENGAA_2019_S1_QuestionPaper.pdf", 3),
    ("engaa_2020_q1",  "papers/engaa/ENGAA_2020_S1_QuestionPaper.pdf", 2),
    ("engaa_2020_q2",  "papers/engaa/ENGAA_2020_S1_QuestionPaper.pdf", 3),
    ("engaa_2021_q1",  "papers/engaa/ENGAA_2021_S1_QuestionPaper.pdf", 2),
    ("engaa_2021_q2",  "papers/engaa/ENGAA_2021_S1_QuestionPaper.pdf", 3),
    ("engaa_2022_q1",  "papers/engaa/ENGAA_2022_S1_QuestionPaper.pdf", 2),
    ("engaa_2022_q2",  "papers/engaa/ENGAA_2022_S1_QuestionPaper.pdf", 3),
    ("engaa_2023_q1",  "papers/engaa/ENGAA_2023_S1_QuestionPaper.pdf", 2),
    ("engaa_2023_q2",  "papers/engaa/ENGAA_2023_S1_QuestionPaper.pdf", 3),

    # ── TMUA 2016–2023: priority questions ─────────────────────────────────
    ("tmua_2016_q4",  "papers/tmua/TMUA-2016-paper-1.pdf", 3),
    ("tmua_2016_q6",  "papers/tmua/TMUA-2016-paper-1.pdf", 5),
    ("tmua_2016_q7",  "papers/tmua/TMUA-2016-paper-1.pdf", 6),
    ("tmua_2016_q8",  "papers/tmua/TMUA-2016-paper-1.pdf", 7),
    ("tmua_2016_q10", "papers/tmua/TMUA-2016-paper-1.pdf", 9),
    ("tmua_2016_q13", "papers/tmua/TMUA-2016-paper-1.pdf", 12),
    ("tmua_2016_q14", "papers/tmua/TMUA-2016-paper-1.pdf", 13),
    ("tmua_2016_q17", "papers/tmua/TMUA-2016-paper-1.pdf", 16),
    ("tmua_2016_q18", "papers/tmua/TMUA-2016-paper-1.pdf", 17),
    ("tmua_2016_q20", "papers/tmua/TMUA-2016-paper-1.pdf", 19),
    ("tmua_2017_q4",  "papers/tmua/TMUA-2017-paper-1.pdf", 3),
    ("tmua_2017_q6",  "papers/tmua/TMUA-2017-paper-1.pdf", 5),
    ("tmua_2017_q8",  "papers/tmua/TMUA-2017-paper-1.pdf", 7),
    ("tmua_2017_q10", "papers/tmua/TMUA-2017-paper-1.pdf", 9),
    ("tmua_2018_q3",  "papers/tmua/TMUA-2018-paper-1.pdf", 2),
    ("tmua_2018_q5",  "papers/tmua/TMUA-2018-paper-1.pdf", 4),
    ("tmua_2018_q7",  "papers/tmua/TMUA-2018-paper-1.pdf", 6),
    ("tmua_2019_q4",  "papers/tmua/TMUA-2019-paper-1.pdf", 3),
    ("tmua_2019_q6",  "papers/tmua/TMUA-2019-paper-1.pdf", 5),
    ("tmua_2019_q8",  "papers/tmua/TMUA-2019-paper-1.pdf", 7),
    ("tmua_2020_q3",  "papers/tmua/TMUA-2020-paper-1.pdf", 2),
    ("tmua_2020_q5",  "papers/tmua/TMUA-2020-paper-1.pdf", 4),
    ("tmua_2021_q4",  "papers/tmua/TMUA-2021-paper-1.pdf", 3),
    ("tmua_2021_q6",  "papers/tmua/TMUA-2021-paper-1.pdf", 5),
    ("tmua_2021_q8",  "papers/tmua/TMUA-2021-paper-1.pdf", 7),
    ("tmua_2022_q3",  "papers/tmua/TMUA-2022-paper-1.pdf", 2),
    ("tmua_2022_q5",  "papers/tmua/TMUA-2022-paper-1.pdf", 4),
    ("tmua_2023_q2",  "papers/tmua/TMUA-2023-paper-1.pdf", 1),
    ("tmua_2023_q5",  "papers/tmua/TMUA-2023-paper-1.pdf", 4),
    ("tmua_2023_q7",  "papers/tmua/TMUA-2023-paper-1.pdf", 6),
    ("tmua_2023_q8",  "papers/tmua/TMUA-2023-paper-1.pdf", 7),
    ("tmua_2023_q9",  "papers/tmua/TMUA-2023-paper-1.pdf", 8),
    ("tmua_2023_q12", "papers/tmua/TMUA-2023-paper-1.pdf", 11),
    ("tmua_2023_q14", "papers/tmua/TMUA-2023-paper-1.pdf", 13),
    ("tmua_specimen_q4", "papers/tmua/TMUA-early-specimen-paper-1.pdf", 3),
    ("tmua_specimen_q6", "papers/tmua/TMUA-early-specimen-paper-1.pdf", 5),
    ("tmua_specimen_q8", "papers/tmua/TMUA-early-specimen-paper-1.pdf", 7),

    # ── PAT 2017–2023: Q1-Q12 quick drill set per year ─────────────────────
    ("pat_2017_q1",  "papers/pat/PAT-2017.pdf", 1),
    ("pat_2017_q2",  "papers/pat/PAT-2017.pdf", 1),
    ("pat_2017_q3",  "papers/pat/PAT-2017.pdf", 2),
    ("pat_2018_q1",  "papers/pat/PAT-2018.pdf", 1),
    ("pat_2018_q2",  "papers/pat/PAT-2018.pdf", 1),
    ("pat_2019_q1",  "papers/pat/PAT-2019.pdf", 1),
    ("pat_2019_q2",  "papers/pat/PAT-2019.pdf", 1),
    ("pat_2020_q1",  "papers/pat/PAT-2020.pdf", 1),
    ("pat_2020_q2",  "papers/pat/PAT-2020.pdf", 1),
    ("pat_2021_q1",  "papers/pat/PAT-2021.pdf", 1),
    ("pat_2021_q2",  "papers/pat/PAT-2021.pdf", 1),
    ("pat_2022_q1",  "papers/pat/PAT-2022.pdf", 1),
    ("pat_2022_q2",  "papers/pat/PAT-2022.pdf", 1),
    ("pat_2023_q1",  "papers/pat/PAT-2023.pdf", 1),
    ("pat_2023_q2",  "papers/pat/PAT-2023.pdf", 1),
    ("pat_specimen_q1", "papers/pat/PAT-2017-Specimen.pdf", 1),
    ("pat_specimen_q2", "papers/pat/PAT-2017-Specimen.pdf", 1),
]


def extract_page(pdf_path: Path, page_idx: int, out_path: Path) -> bool:
    """Render one PDF page as a PNG. Returns True on success."""
    if not pdf_path.exists():
        print(f"  SKIP (PDF not found): {pdf_path}")
        return False
    try:
        doc = pdfium.PdfDocument(str(pdf_path))
        if page_idx >= len(doc):
            print(f"  SKIP (page {page_idx} out of range, PDF has {len(doc)} pages): {pdf_path.name}")
            return False
        page = doc[page_idx]
        bitmap = page.render(scale=SCALE)
        img = bitmap.to_pil()
        img.save(str(out_path))
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    ok = 0
    skipped = 0
    for qid, rel_pdf, page_idx in MANIFEST:
        out_path = IMAGES_DIR / f"{qid}.png"
        if out_path.exists():
            print(f"  EXISTS: {qid}.png")
            ok += 1
            continue
        pdf_path = ROOT / rel_pdf
        print(f"Extracting {qid} (page {page_idx + 1}) ...", end=" ")
        if extract_page(pdf_path, page_idx, out_path):
            print("OK")
            ok += 1
        else:
            skipped += 1

    print(f"\nDone. {ok} extracted, {skipped} skipped.")
    print(f"Images saved to: {IMAGES_DIR}")
    print("\nNext step: run scripts/build_questions.py to generate data/questions.json")


if __name__ == "__main__":
    main()
