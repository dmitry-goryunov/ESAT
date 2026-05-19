import json
import random
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="ESAT Prep Dashboard", layout="wide")

st.title("ESAT Preparation Dashboard")
st.caption("Maths 1 · Maths 2 · Physics — Oxbridge / Imperial target")

tab4, tab1, tab2, tab3 = st.tabs(["🎯 Quiz", "📅 12-Week Schedule", "📚 Papers Timetable", "📊 Paper Comparison"])

# ─────────────────────────────────────────────
# TAB 1 — 12-WEEK SCHEDULE
# ─────────────────────────────────────────────
with tab1:

    phases = {
        "Phase 1 — Fluency Foundation": {
            "dates": "Weeks 1–3 · 19 May – 8 Jun",
            "goals": "Rebuild algebra and arithmetic fluency · diagnose weak topics · 15-Q timed sets · begin error logging",
            "weeks": {
                "Week 1 — 19–25 May": [
                    ("Mon", "Algebra / trig / log drill", "TMUA Specimen P1", "15 Q", "25 min"),
                    ("Tue", "Mechanics timed set", "Mechanics2 Q1–15", "15 Q", "20 min"),
                    ("Wed", "Waves timed set", "Waves1 Q1–15", "15 Q", "20 min"),
                    ("Thu", "Electronics timed set", "Electronics2 Q1–15", "15 Q", "20 min"),
                    ("Fri", "Mixed timed set", "Mechanics2 Q16–20 + Waves1 Q16–20 + Electronics2 Q16–20", "15 Q", "20 min"),
                    ("Sat", "Physics MCQ block", "NSAA 2016 S1", "~20 Q", "30 min"),
                    ("Sun", "Mistake review", "Error log + 10 TMUA Q untimed", "—", "open"),
                ],
                "Week 2 — 26 May–1 Jun": [
                    ("Mon", "Algebra / functions drill", "TMUA 2016 P1", "15 Q", "25 min"),
                    ("Tue", "Mechanics timed set", "Mechanics2 Q21–30 + Mechanics1 Q1–5", "15 Q", "20 min"),
                    ("Wed", "Waves timed set", "Waves1 Q21–30 + Waves2 Q1–5", "15 Q", "20 min"),
                    ("Thu", "Electronics timed set", "Electronics2 Q21–30 + Electronics1 Q1–5", "15 Q", "20 min"),
                    ("Fri", "Mixed timed set", "Mechanics / Waves / Electronics mixed", "15 Q", "20 min"),
                    ("Sat", "Maths MCQ block", "NSAA 2017 S1", "~20 Q", "30 min"),
                    ("Sun", "Mistake review + weak-topic ID", "Error log — note top 3 recurring errors", "—", "open"),
                ],
                "Week 3 — 2–8 Jun": [
                    ("Mon", "TMUA maths logic", "TMUA 2017 P1", "15 Q", "25 min"),
                    ("Tue", "Mechanics challenge", "Mechanics2 — weakest topic remix", "15 Q", "25 min"),
                    ("Wed", "Waves challenge", "Waves1 + Waves2 mixed", "15 Q", "20 min"),
                    ("Thu", "Electronics challenge", "Electronics2 + Electronics1 mixed", "15 Q", "20 min"),
                    ("Fri", "First 40-min block", "NSAA 2018 S1", "~20 Q", "40 min"),
                    ("Sat", "Maths 40-min block", "NSAA 2018 S1 (Maths section)", "~20 Q", "40 min"),
                    ("Sun", "Phase 1 review", "All error log entries — identify top weak topics", "—", "open"),
                ],
            },
        },
        "Phase 2 — Admissions Pacing": {
            "dates": "Weeks 4–6 · 9–29 Jun",
            "goals": "Move to NSAA and ENGAA at full speed · 40-min modules · skipping discipline · one PAT concept session/week",
            "weeks": {
                "Week 4 — 9–15 Jun": [
                    ("Mon", "ENGAA algebra block", "ENGAA 2016 S1", "20 Q", "30 min"),
                    ("Tue", "NSAA Physics block", "NSAA 2019 S1", "20 Q", "30 min"),
                    ("Wed", "TMUA drill", "TMUA 2018 P1", "20 Q", "30 min"),
                    ("Thu", "PAT concept — mechanics", "PAT 2017 Specimen (selected Q)", "10 Q", "untimed"),
                    ("Fri", "Mixed admissions drill", "ENGAA 2016 + NSAA 2019 mixed", "20 Q", "30 min"),
                    ("Sat", "40-min module sim", "NSAA 2019 S1 (full)", "~25 Q", "40 min"),
                    ("Sun", "Mistake review", "Error log", "—", "open"),
                ],
                "Week 5 — 16–22 Jun": [
                    ("Mon", "ENGAA Section A", "ENGAA 2017 S1", "20 Q", "30 min"),
                    ("Tue", "NSAA Section 1", "NSAA 2020 S1", "20 Q", "30 min"),
                    ("Wed", "TMUA drill", "TMUA 2019 P1", "20 Q", "30 min"),
                    ("Thu", "PAT concept — circuits", "PAT 2017 (selected Q)", "10 Q", "untimed"),
                    ("Fri", "Mixed admissions drill", "ENGAA 2017 + NSAA 2020 mixed", "20 Q", "30 min"),
                    ("Sat", "40-min module sim", "ENGAA 2017 S1 (full)", "20 Q", "40 min"),
                    ("Sun", "Mistake review", "Error log", "—", "open"),
                ],
                "Week 6 — 23–29 Jun": [
                    ("Mon", "ENGAA Section A", "ENGAA 2018 S1", "20 Q", "30 min"),
                    ("Tue", "NSAA Physics", "NSAA 2021 S1", "20 Q", "30 min"),
                    ("Wed", "ESAT Maths 1 Specimen", "Pearson VUE — ESAT Maths 1 Specimen (online)", "27 Q", "40 min"),
                    ("Thu", "PAT concept — waves", "PAT 2018 (selected Q)", "10 Q", "untimed"),
                    ("Fri", "Mixed admissions drill", "NSAA 2021 + ENGAA 2018 mixed", "20 Q", "30 min"),
                    ("Sat", "Double 40-min sim", "NSAA 2021 + ENGAA 2018 back-to-back", "2×20 Q", "80 min"),
                    ("Sun", "Phase 2 review", "Error log + update weak topic list", "—", "open"),
                ],
            },
        },
        "Phase 3 — Full Simulation": {
            "dates": "Weeks 7–9 · 30 Jun–20 Jul",
            "goals": "Triple-module simulations every Saturday · fatigue resistance · PAT for weak-topic repair only",
            "weeks": {
                "Week 7 — 30 Jun–6 Jul": [
                    ("Mon", "ENGAA full section", "ENGAA 2019 S1", "20 Q", "40 min"),
                    ("Tue", "NSAA full section", "NSAA 2022 S1", "~25 Q", "40 min"),
                    ("Wed", "ESAT Maths 2 Specimen", "Pearson VUE — ESAT Maths 2 Specimen (online)", "27 Q", "40 min"),
                    ("Thu", "PAT weak repair", "PAT 2019 — weakest topic from error log", "10 Q", "untimed"),
                    ("Fri", "Mixed timed block", "ENGAA 2019 + NSAA 2022 mix", "25 Q", "40 min"),
                    ("Sat", "TRIPLE SIM", "ENGAA 2019 + NSAA 2022 + ESAT Maths 2 Specimen", "3×27 Q", "3×40 min"),
                    ("Sun", "Post-sim review", "Error log update", "—", "open"),
                ],
                "Week 8 — 7–13 Jul": [
                    ("Mon", "ENGAA full section", "ENGAA 2020 S1", "20 Q", "40 min"),
                    ("Tue", "NSAA full section", "NSAA 2023 S1", "~25 Q", "40 min"),
                    ("Wed", "ESAT Physics Specimen", "Pearson VUE — ESAT Physics Specimen (online)", "27 Q", "40 min"),
                    ("Thu", "PAT weak repair", "PAT 2020 — weakest topic from error log", "10 Q", "untimed"),
                    ("Fri", "Fastest-pace drill", "Mixed — strict 1 min/Q target", "25 Q", "25 min"),
                    ("Sat", "TRIPLE SIM", "ENGAA 2020 + NSAA 2023 + ESAT Physics Specimen", "3×27 Q", "3×40 min"),
                    ("Sun", "Post-sim review", "Error log update", "—", "open"),
                ],
                "Week 9 — 14–20 Jul": [
                    ("Mon", "ENGAA full section", "ENGAA 2021 S1", "20 Q", "40 min"),
                    ("Tue", "NSAA repeat weakest", "Lowest-scoring NSAA from log", "~25 Q", "40 min"),
                    ("Wed", "ESAT Maths 1 Sample", "Pearson VUE — ESAT Maths 1 Sample (online)", "27 Q", "40 min"),
                    ("Thu", "Weak topic repair", "Error log top 3 topics", "—", "30 min"),
                    ("Fri", "Mixed precision drill", "ENGAA 2021 + NSAA mixed", "25 Q", "40 min"),
                    ("Sat", "TRIPLE SIM", "ENGAA 2021 + NSAA repeat + ESAT Maths 1 Sample", "3×27 Q", "3×40 min"),
                    ("Sun", "Phase 3 review", "Score table + error log summary", "—", "open"),
                ],
            },
        },
        "Phase 4 — Optimisation": {
            "dates": "Weeks 10–12 · 21 Jul–10 Aug",
            "goals": "Reduce volume · reattempt hardest prior mistakes · stabilise scores · no new PAT",
            "weeks": {
                "Week 10 — 21–27 Jul": [
                    ("Mon", "Weakest paper reattempt", "Lowest-scoring ENGAA from log", "20 Q", "40 min"),
                    ("Tue", "Error log drill — algebra slips", "All algebra slip entries", "15 Q", "25 min"),
                    ("Wed", "ESAT Maths 2 Sample", "Pearson VUE — ESAT Maths 2 Sample (online)", "27 Q", "40 min"),
                    ("Thu", "Concept repair", "Weakest topic from log", "—", "30 min"),
                    ("Fri", "Mixed precision drill", "ENGAA 2022 + NSAA hard Q only", "20 Q", "35 min"),
                    ("Sat", "TRIPLE SIM", "ENGAA 2022 + NSAA repeat + ESAT Maths 2 Sample", "3×27 Q", "3×40 min"),
                    ("Sun", "Score analysis", "Weekly summary table", "—", "open"),
                ],
                "Week 11 — 28 Jul–3 Aug": [
                    ("Mon", "Weakest paper reattempt", "Second-lowest-scoring ENGAA from log", "20 Q", "40 min"),
                    ("Tue", "Error log drill — traps/misreads", "All trap / misread entries", "15 Q", "25 min"),
                    ("Wed", "ESAT Physics Sample", "Pearson VUE — ESAT Physics Sample (online)", "27 Q", "40 min"),
                    ("Thu", "Concept repair", "Second weakest topic from log", "—", "30 min"),
                    ("Fri", "Full-speed drill", "ENGAA 2023 + NSAA — strict 1.5 min/Q", "25 Q", "37 min"),
                    ("Sat", "TRIPLE SIM", "ENGAA 2023 + NSAA repeat + ESAT Physics Sample", "3×27 Q", "3×40 min"),
                    ("Sun", "Score analysis", "Weekly summary + comparison table", "—", "open"),
                ],
                "Week 12 — 4–10 Aug": [
                    ("Mon", "Final reattempt", "Top 15 hardest questions from entire log", "15 Q", "untimed"),
                    ("Tue", "ESAT Maths 1 re-run", "Re-run weakest ESAT Maths 1 from log", "27 Q", "40 min"),
                    ("Wed", "ESAT Maths 2 re-run", "Re-run weakest ESAT Maths 2 from log", "27 Q", "40 min"),
                    ("Thu", "ESAT Physics re-run", "Re-run weakest ESAT Physics from log", "27 Q", "40 min"),
                    ("Fri", "Light confidence drill", "Best-performing topic areas", "15 Q", "20 min"),
                    ("Sat", "FINAL TRIPLE SIM", "ENGAA repeat + NSAA repeat + ESAT weakest module", "3×27 Q", "3×40 min"),
                    ("Sun", "Final review", "Score table + strategy notes only — no new material", "—", "open"),
                ],
            },
        },
    }

    phase_colors = {
        "Phase 1 — Fluency Foundation": "#1a3a5c",
        "Phase 2 — Admissions Pacing": "#1a4a3a",
        "Phase 3 — Full Simulation": "#4a2a1a",
        "Phase 4 — Optimisation": "#3a1a4a",
    }

    cols = st.columns(len(phases))
    for i, (phase, data) in enumerate(phases.items()):
        with cols[i]:
            st.markdown(
                f"<div style='background:{list(phase_colors.values())[i]};padding:10px;border-radius:8px;text-align:center'>"
                f"<b style='color:white;font-size:13px'>{phase}</b><br>"
                f"<span style='color:#ccc;font-size:11px'>{data['dates']}</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    for phase, data in phases.items():
        color = phase_colors[phase]
        st.markdown(
            f"<h3 style='color:white;background:{color};padding:10px 16px;border-radius:8px'>{phase} · {data['dates']}</h3>",
            unsafe_allow_html=True,
        )
        st.caption(f"**Goals:** {data['goals']}")

        for week, sessions in data["weeks"].items():
            st.markdown(f"**{week}**")
            df = pd.DataFrame(sessions, columns=["Day", "Session", "Source", "Volume", "Time"])
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Day": st.column_config.TextColumn(width="small"),
                    "Session": st.column_config.TextColumn(width="medium"),
                    "Source": st.column_config.TextColumn(width="large"),
                    "Volume": st.column_config.TextColumn(width="small"),
                    "Time": st.column_config.TextColumn(width="small"),
                },
            )

# ─────────────────────────────────────────────
# TAB 2 — PAPERS TIMETABLE
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Papers Per Week")
    st.caption("All papers mapped to specific weeks. Oldest papers first within each source.")

    timetable = [
        (1, "19–25 May", "Phase 1", "Mechanics2 · Waves1 · Electronics2", "—", "2016", "Specimen", "—", "—"),
        (2, "26 May–1 Jun", "Phase 1", "Mechanics1 · Waves2 · Electronics1", "—", "2017", "2016", "—", "—"),
        (3, "2–8 Jun", "Phase 1", "Mixed — weak topics", "—", "2018", "2017", "—", "—"),
        (4, "9–15 Jun", "Phase 2", "—", "2016", "2019", "2018", "2017 Specimen — mechanics", "—"),
        (5, "16–22 Jun", "Phase 2", "—", "2017", "2020", "2019", "2017 — circuits", "—"),
        (6, "23–29 Jun", "Phase 2", "—", "2018", "2021", "2020", "2018 — waves", "Maths 1 Specimen"),
        (7, "30 Jun–6 Jul", "Phase 3", "—", "2019", "2022", "2021", "2019 — weakest topic", "Maths 2 Specimen"),
        (8, "7–13 Jul", "Phase 3", "—", "2020", "2023", "2022", "2020 — weakest topic", "Physics Specimen"),
        (9, "14–20 Jul", "Phase 3", "—", "2021", "repeat weakest", "2023", "2021 — weakest topic", "Maths 1 Sample"),
        (10, "21–27 Jul", "Phase 4", "—", "2022", "repeat weakest", "—", "—", "Maths 2 Sample"),
        (11, "28 Jul–3 Aug", "Phase 4", "—", "2023", "repeat weakest", "—", "—", "Physics Sample"),
        (12, "4–10 Aug", "Phase 4", "—", "repeat weakest", "repeat weakest", "—", "—", "re-run weakest"),
    ]

    df_tt = pd.DataFrame(timetable, columns=[
        "Week", "Dates", "Phase",
        "Uploaded Docs", "ENGAA S1", "NSAA S1", "TMUA P1",
        "PAT (selected Q)", "ESAT Online"
    ])

    phase_map = {"Phase 1": "🔵", "Phase 2": "🟢", "Phase 3": "🟠", "Phase 4": "🟣"}
    df_tt["Phase"] = df_tt["Phase"].map(lambda p: f"{phase_map.get(p, '')} {p}")

    st.dataframe(
        df_tt,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Week": st.column_config.NumberColumn(width="small"),
            "Dates": st.column_config.TextColumn(width="medium"),
            "Phase": st.column_config.TextColumn(width="small"),
            "Uploaded Docs": st.column_config.TextColumn(width="medium"),
            "ENGAA S1": st.column_config.TextColumn(width="small"),
            "NSAA S1": st.column_config.TextColumn(width="small"),
            "TMUA P1": st.column_config.TextColumn(width="small"),
            "PAT (selected Q)": st.column_config.TextColumn(width="medium"),
            "ESAT Online": st.column_config.TextColumn(width="medium"),
        },
    )

    st.markdown("---")
    st.subheader("Timing Rules by Source")

    timing = [
        ("Uploaded docs", "15-Q sets", "Yes — 20–25 min", "Never sit full doc end to end"),
        ("TMUA Paper 1", "15–20 Q drill", "Yes — 25–30 min", "Full paper is 75 min — too slow; extract questions only"),
        ("NSAA S1 (Weeks 1–3)", "Partial section ~20 Q", "Yes — 30 min", "Saturday block only"),
        ("NSAA S1 (Weeks 4–6)", "Full section ~25 Q", "Yes — 40 min", "Single module sim"),
        ("NSAA S1 (Weeks 7–9)", "Full section", "Yes — 40 min", "Part of triple sim"),
        ("ENGAA S1 (Weeks 4–6)", "Full section ~20 Q", "Yes — 30–40 min", "Single module sim"),
        ("ENGAA S1 (Weeks 7–12)", "Full section", "Yes — 40 min", "Part of triple sim"),
        ("PAT", "Selected Q by topic", "No — untimed", "Concept depth only; never a full paper"),
        ("ESAT Specimen (online)", "Full module 27 Q", "Yes — 40 min", "Has explained answers — review carefully after"),
        ("ESAT Sample (online)", "Full module 27 Q", "Yes — 40 min", "Correct/incorrect only — full pressure"),
    ]

    df_timing = pd.DataFrame(timing, columns=["Source", "Format", "Timed?", "Notes"])
    st.dataframe(df_timing, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# TAB 3 — PAPER COMPARISON
# ─────────────────────────────────────────────
with tab3:
    st.subheader("How Each Source Compares to ESAT")

    st.markdown("#### Format and Pacing")
    format_data = [
        ("ESAT", "MCQ", "27/module", "40 min", "1.5 min", "No", "—"),
        ("NSAA S1", "MCQ", "~20–25", "30 min", "1.2–1.5 min", "No", "★★★★★"),
        ("ENGAA S1", "MCQ", "~20", "30 min", "1.5 min", "No", "★★★★★"),
        ("TMUA P1", "MCQ", "20", "75 min", "3.75 min", "No", "★★☆☆☆"),
        ("PAT", "Written (long-form)", "~25 mixed", "2 hours", "~5 min", "No (pre-2018)", "★☆☆☆☆"),
        ("Uploaded docs", "MCQ", "varies", "self-set", "self-set", "No", "★★★☆☆"),
    ]
    df_format = pd.DataFrame(format_data, columns=[
        "Source", "Type", "Questions", "Time", "Time/Q", "Calculator", "Pacing match to ESAT"
    ])
    st.dataframe(df_format, use_container_width=True, hide_index=True)

    st.markdown("#### Content Overlap with ESAT")
    content_data = [
        ("NSAA S1", "★★★★☆", "★★★☆☆", "★★★★★"),
        ("ENGAA S1", "★★★★☆", "★★★☆☆", "★★★★☆"),
        ("TMUA P1", "★★★★★", "★★★★☆", "☆☆☆☆☆"),
        ("PAT", "★★☆☆☆", "★★☆☆☆", "★★★★☆"),
        ("Uploaded docs", "★★★☆☆", "★★☆☆☆", "★★★★☆"),
    ]
    df_content = pd.DataFrame(content_data, columns=[
        "Source", "ESAT Maths 1", "ESAT Maths 2", "ESAT Physics"
    ])
    st.dataframe(df_content, use_container_width=True, hide_index=True)

    st.markdown("#### Style and Question Character")
    style_data = [
        ("NSAA S1", "Yes", "Yes", "Yes", "Rarely", "Yes", "Yes"),
        ("ENGAA S1", "Yes", "Yes", "Yes", "Rarely", "Yes", "Yes"),
        ("TMUA P1", "Yes", "Yes", "Yes", "Sometimes", "Yes", "Less so"),
        ("PAT", "No", "No", "No", "Often", "Occasionally", "No"),
        ("Uploaded docs", "Yes", "Sometimes", "Yes", "Rarely", "Yes", "Yes"),
    ]
    df_style = pd.DataFrame(style_data, columns=[
        "Source", "Short self-contained Q", "Estimation/elimination",
        "Pattern recognition", "Long derivation", "Conceptually deceptive", "Skipping strategy applies"
    ])
    st.dataframe(df_style, use_container_width=True, hide_index=True)

    st.markdown("#### Overall ESAT Training Value")
    value_data = [
        ("NSAA S1", "★★★★★", "Closest proxy — same pace, same format, physics directly relevant"),
        ("ENGAA S1", "★★★★★", "Closest proxy — identical time/Q ratio, engineering-flavoured maths + physics"),
        ("Uploaded docs", "★★★★☆", "Best starting point — accessible difficulty, builds fluency before NSAA/ENGAA"),
        ("TMUA P1", "★★★☆☆", "Strong maths content, wrong pace — use as drill not timed sim"),
        ("PAT", "★★☆☆☆", "Good physics depth, wrong format — concept repair only"),
    ]
    df_value = pd.DataFrame(value_data, columns=["Source", "Training Value", "Primary Use"])

    def colour_value(val):
        stars = val.count("★")
        if stars >= 5:
            return "background-color: #1a4a1a; color: white"
        elif stars == 4:
            return "background-color: #1a3a1a; color: white"
        elif stars == 3:
            return "background-color: #3a3a1a; color: white"
        else:
            return "background-color: #3a1a1a; color: white"

    st.dataframe(
        df_value.style.map(colour_value, subset=["Training Value"]),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.info(
        "**Bottom line:** NSAA and ENGAA are the best ESAT simulators — same MCQ format, "
        "same no-calculator condition, same ~1.5 min/Q pace. TMUA is useful for maths content "
        "but trains the wrong speed. PAT is furthest from ESAT and should only fill concept gaps."
    )

# ─────────────────────────────────────────────
# TAB 4 — QUIZ
# ─────────────────────────────────────────────

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "questions.json"
PROGRESS_FILE = ROOT / "data" / "progress.json"
ATTEMPTS_FILE = ROOT / "data" / "attempts.jsonl"
SCORES_FILE = ROOT / "scores.csv"
ERROR_LOG_FILE = ROOT / "error_log.md"

Q_TIME = 90  # seconds per question (1.5 min)
SLOW_TIME = 120  # seconds; slow correct answers still need review


def load_questions() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding="utf-8") as f:
        questions = [q for q in json.load(f) if q.get("answer")]
    for q in questions:
        q["esat_area"] = infer_esat_area(q)
        q["paper_key"] = "_".join(q["id"].split("_")[:2])
    return questions


def count_question_records() -> int:
    if not DATA_FILE.exists():
        return 0
    with DATA_FILE.open(encoding="utf-8") as f:
        return len(json.load(f))


def infer_esat_area(q: dict) -> str:
    if q.get("module") == "physics":
        return "Physics"
    maths2_topics = {"functions", "graphs", "sequences", "trig"}
    if q.get("topic") in maths2_topics:
        return "Maths 2"
    return "Maths 1"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with PROGRESS_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    return {"completed_correct": []}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.parent.mkdir(exist_ok=True)
    with PROGRESS_FILE.open("w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def load_attempts() -> list[dict]:
    if not ATTEMPTS_FILE.exists():
        return []
    attempts = []
    with ATTEMPTS_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                attempts.append(json.loads(line))
    return attempts


def append_attempts(rows: list[dict]) -> None:
    ATTEMPTS_FILE.parent.mkdir(exist_ok=True)
    with ATTEMPTS_FILE.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def log_score(summary: dict) -> None:
    import csv
    headers = [
        "date", "source", "mode", "area", "questions_attempted", "correct",
        "adjusted_correct", "time_minutes", "score_percent",
        "adjusted_score_percent", "seconds_per_question", "skipped",
        "guessed", "lucky_correct", "slow_review", "topics",
    ]
    row = {h: summary.get(h, "") for h in headers}
    exists = SCORES_FILE.exists()
    with SCORES_FILE.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def fmt_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def q_timer_color(elapsed: float) -> str:
    if elapsed < 75:
        return "#4caf50"
    if elapsed < 90:
        return "#ff9800"
    return "#f44336"


def qnum_label(qid: str) -> str:
    return "Q" + qid.rsplit("_q", 1)[-1]


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def get_filter_options(questions: list[dict]) -> tuple[list[str], list[str], list[str]]:
    sources = sorted({q["source"] for q in questions})
    years = sorted({q["id"].split("_")[1].capitalize() for q in questions})
    topics = sorted({q["topic"] for q in questions})
    return sources, years, topics


def apply_quiz_filters(
    questions: list[dict],
    area_filter: str,
    source_filter: str,
    year_filter: str,
    topic_filter: str,
    include_done: bool,
) -> list[dict]:
    progress = load_progress()
    done_ids = set(progress.get("completed_correct", []))
    pool = list(questions)
    if area_filter != "All":
        pool = [q for q in pool if q.get("esat_area") == area_filter]
    if source_filter != "All":
        pool = [q for q in pool if q["source"] == source_filter]
    if year_filter != "All":
        pool = [q for q in pool if q["id"].split("_")[1].capitalize() == year_filter]
    if topic_filter != "All":
        pool = [q for q in pool if q["topic"] == topic_filter]
    if not include_done:
        pool = [q for q in pool if q["id"] not in done_ids]
    return pool


def weak_topics_from_attempts() -> list[str]:
    attempts = load_attempts()
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"bad": 0, "total": 0})
    for row in attempts:
        topic = row.get("topic")
        if not topic:
            continue
        stats[topic]["total"] += 1
        if not row.get("correct") or row.get("confidence") in {"Guess", "Unsure"} or row.get("slow"):
            stats[topic]["bad"] += 1
    ranked = sorted(
        stats,
        key=lambda t: (stats[t]["bad"], stats[t]["bad"] / max(stats[t]["total"], 1)),
        reverse=True,
    )
    return [t for t in ranked if stats[t]["bad"] > 0]


def init_quiz(
    questions: list[dict],
    area_filter: str,
    source_filter: str,
    year_filter: str,
    topic_filter: str,
    include_done: bool,
    n_questions: int,
    quiz_mode: str,
    target_seconds: int,
) -> bool:
    pool = apply_quiz_filters(questions, area_filter, source_filter, year_filter, topic_filter, include_done)
    if quiz_mode == "Weak-topic repair" and topic_filter == "All":
        weak_topics = weak_topics_from_attempts()
        if weak_topics:
            weak_pool = [q for q in pool if q["topic"] in set(weak_topics[:3])]
            if len(weak_pool) >= min(n_questions, len(pool)):
                pool = weak_pool
    if len(pool) < n_questions:
        st.error(f"Not enough questions available ({len(pool)} found, need {n_questions}). "
                 "Loosen filters or enable already-correct questions.")
        return False

    # Group by paper (e.g. "nsaa_2022", "tmua_2018") and pick one paper.
    by_paper: dict[str, list[dict]] = defaultdict(list)
    for q in pool:
        by_paper[q["paper_key"]].append(q)
    eligible_papers = [k for k, qs in by_paper.items() if len(qs) >= n_questions]
    if eligible_papers and source_filter != "All":
        chosen_paper = random.choice(eligible_papers)
        selected = random.sample(by_paper[chosen_paper], n_questions)
    else:
        selected = random.sample(pool, n_questions)
    st.session_state.quiz_active = True
    st.session_state.quiz_questions = selected
    st.session_state.quiz_n_questions = n_questions
    st.session_state.quiz_mode = quiz_mode
    st.session_state.quiz_area_filter = area_filter
    st.session_state.quiz_source_filter = source_filter
    st.session_state.quiz_target_seconds = target_seconds
    st.session_state.quiz_index = 0
    st.session_state.quiz_answers = {}
    st.session_state.quiz_confidence = {}
    st.session_state.quiz_skipped = set()
    st.session_state.quiz_q_times = {}
    st.session_state.quiz_session_start = time.time()
    st.session_state.quiz_q_start = time.time()
    st.session_state.show_technique = False
    st.session_state.error_log_exported = False
    st.session_state.quiz_done = False
    return True


def record_q_time() -> None:
    """Accumulate time spent on current question into quiz_q_times."""
    if not st.session_state.get("quiz_active") or st.session_state.get("quiz_done"):
        return
    q_times = st.session_state.get("quiz_q_times", {})
    idx = st.session_state.quiz_index
    q = st.session_state.quiz_questions[idx]
    elapsed = time.time() - st.session_state.quiz_q_start
    q_times[q["id"]] = q_times.get(q["id"], 0.0) + elapsed
    st.session_state.quiz_q_times = q_times
    st.session_state.quiz_q_start = time.time()


def build_quiz_results() -> tuple[list[dict], dict]:
    questions = st.session_state.quiz_questions
    answers = st.session_state.quiz_answers
    confidence = st.session_state.get("quiz_confidence", {})
    skipped = set(st.session_state.get("quiz_skipped", set()))
    q_times = st.session_state.get("quiz_q_times", {})
    time_used = time.time() - st.session_state.quiz_session_start

    rows = []
    for i, q in enumerate(questions, 1):
        chosen = answers.get(q["id"], "")
        conf = confidence.get(q["id"], "Confident")
        is_correct = chosen == q["answer"]
        is_skipped = q["id"] in skipped or chosen == ""
        is_guess = conf in {"Guess", "Unsure"}
        q_secs = q_times.get(q["id"], 0.0)
        rows.append({
            "date": str(date.today()),
            "question_index": i,
            "id": q["id"],
            "source": q["source"],
            "area": q.get("esat_area", infer_esat_area(q)),
            "module": q.get("module", ""),
            "topic": q.get("topic", ""),
            "question": qnum_label(q["id"]),
            "chosen": chosen or "-",
            "correct_answer": q["answer"],
            "correct": is_correct,
            "confidence": conf,
            "skipped": is_skipped,
            "guessed": is_guess,
            "lucky_correct": is_correct and is_guess,
            "slow": q_secs >= SLOW_TIME,
            "time_seconds": round(q_secs, 1),
            "time_spent": fmt_time(q_secs),
            "mode": st.session_state.get("quiz_mode", "Timed test"),
        })

    n_q = len(rows)
    n_correct = sum(1 for r in rows if r["correct"])
    lucky = sum(1 for r in rows if r["lucky_correct"])
    adjusted_correct = n_correct - lucky
    summary = {
        "date": str(date.today()),
        "source": ", ".join(sorted({r["source"] for r in rows})),
        "mode": st.session_state.get("quiz_mode", "Timed test"),
        "area": st.session_state.get("quiz_area_filter", "All"),
        "questions_attempted": n_q,
        "correct": n_correct,
        "adjusted_correct": adjusted_correct,
        "time_minutes": round(time_used / 60, 1),
        "score_percent": round(n_correct / n_q * 100, 1) if n_q else 0,
        "adjusted_score_percent": round(adjusted_correct / n_q * 100, 1) if n_q else 0,
        "seconds_per_question": round(time_used / n_q, 1) if n_q else 0,
        "skipped": sum(1 for r in rows if r["skipped"]),
        "guessed": sum(1 for r in rows if r["guessed"]),
        "lucky_correct": lucky,
        "slow_review": sum(1 for r in rows if r["slow"]),
        "topics": ", ".join(sorted({r["topic"] for r in rows})),
        "time_used": time_used,
    }
    return rows, summary


def end_quiz() -> None:
    record_q_time()
    rows, summary = build_quiz_results()
    mastered_ids = [
        r["id"] for r in rows
        if r["correct"] and r["confidence"] == "Confident" and not r["slow"]
    ]

    progress = load_progress()
    existing = set(progress.get("completed_correct", []))
    existing.update(mastered_ids)
    progress["completed_correct"] = sorted(existing)
    save_progress(progress)
    append_attempts(rows)
    log_score(summary)

    st.session_state.quiz_done = True
    st.session_state.quiz_active = False
    st.session_state.quiz_results = rows
    st.session_state.quiz_summary = summary
    st.session_state.quiz_n_correct = summary["correct"]
    st.session_state.quiz_time_used = summary["time_used"]


def error_log_rows(rows: list[dict]) -> list[dict]:
    return [
        r for r in rows
        if (not r["correct"]) or r["lucky_correct"] or r["skipped"] or r["slow"]
    ]


def append_error_log(rows: list[dict]) -> int:
    rows_to_log = error_log_rows(rows)
    if not rows_to_log:
        return 0
    lines = []
    for r in rows_to_log:
        if r["skipped"]:
            error_type = "timing panic"
            root = "Skipped or left blank during timed work"
        elif r["lucky_correct"]:
            error_type = "method selection"
            root = "Correct but marked as guessed or unsure"
        elif r["slow"]:
            error_type = "overthinking"
            root = "Correct but slower than review threshold"
        else:
            error_type = "trap/misread"
            root = "Needs review"
        faster = "Use elimination, units, limiting cases or substitution before long derivation"
        action = "Redo this question and one related mini-drill"
        lines.append(
            "| " + " | ".join([
                markdown_escape(r["date"]),
                markdown_escape(r["source"]),
                markdown_escape(r["area"]),
                markdown_escape(r["question"]),
                markdown_escape(r["topic"]),
                markdown_escape(r["time_spent"]),
                markdown_escape(r["chosen"]),
                markdown_escape(r["correct_answer"]),
                error_type,
                root,
                faster,
                action,
                "pending",
                "pending",
            ]) + " |"
        )
    with ERROR_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")
    return len(rows_to_log)


def keyboard_shortcuts() -> None:
    components.html(
        """
        <script>
        const keys = ["A","B","C","D","E","F","G","H"];
        document.addEventListener("keydown", (event) => {
          if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") return;
          const key = event.key.toUpperCase();
          const buttons = [...window.parent.document.querySelectorAll("button")];
          if (keys.includes(key)) {
            const target = buttons.find((b) => b.innerText.trim() === key);
            if (target) target.click();
          }
          if (key === "S") {
            const target = buttons.find((b) => b.innerText.includes("Skip"));
            if (target) target.click();
          }
          if (event.key === "Enter") {
            const target = buttons.find((b) => b.innerText.includes("Next") || b.innerText.includes("Finish"));
            if (target) target.click();
          }
          if (event.key === "ArrowLeft") {
            const target = buttons.find((b) => b.innerText.includes("Back"));
            if (target) target.click();
          }
        });
        </script>
        """,
        height=0,
    )


with tab4:
    all_questions = load_questions()
    source_options, year_options, topic_options = get_filter_options(all_questions)

    with st.expander("Quiz settings", expanded=not st.session_state.get("quiz_active", False)):
        preset_cols = st.columns(3)
        with preset_cols[0]:
            if st.button("15Q drill", use_container_width=True):
                st.session_state.n_questions_input = 15
                st.session_state.target_minutes_input = 25
        with preset_cols[1]:
            if st.button("27Q ESAT module", use_container_width=True):
                st.session_state.n_questions_input = 27
                st.session_state.target_minutes_input = 40
        with preset_cols[2]:
            if st.button("40 min custom", use_container_width=True):
                st.session_state.target_minutes_input = 40

        col_mode, col_area, col_source = st.columns(3)
        with col_mode:
            quiz_mode = st.selectbox("Mode", ["Timed test", "Drill", "Weak-topic repair"], key="quiz_mode_input")
        with col_area:
            area_filter = st.selectbox("Area", ["All", "Maths 1", "Maths 2", "Physics"], key="area_filter")
        with col_source:
            source_filter = st.selectbox("Source", ["All"] + source_options, key="source_filter")

        col_year, col_topic, col_count, col_time = st.columns(4)
        with col_year:
            year_filter = st.selectbox("Year", ["All"] + year_options, key="year_filter")
        with col_topic:
            topic_filter = st.selectbox("Topic", ["All"] + topic_options, key="topic_filter")
        with col_count:
            n_questions = st.number_input("Questions", min_value=1, max_value=50, value=15, step=1, key="n_questions_input")
        with col_time:
            target_minutes = st.number_input("Target minutes", min_value=1, max_value=120, value=25, step=1, key="target_minutes_input")

        include_done = st.checkbox("Include already-mastered questions", value=False, key="include_done")
        preview_pool = apply_quiz_filters(
            all_questions, area_filter, source_filter, year_filter, topic_filter, include_done
        )
        progress_data = load_progress()
        done_count = len(progress_data.get("completed_correct", []))
        weak_topics = weak_topics_from_attempts()
        if quiz_mode == "Weak-topic repair" and topic_filter == "All" and weak_topics:
            st.caption(f"Weak-topic repair will prioritise: {', '.join(weak_topics[:3])}")
        st.caption(
            f"{len(preview_pool)} matching questions · {done_count} mastered · "
            f"{len(all_questions)} usable questions in bank"
        )

        col_a, col_b = st.columns([3, 1])
        with col_a:
            if st.button("Start quiz", type="primary", use_container_width=True):
                started = init_quiz(
                    all_questions,
                    area_filter,
                    source_filter,
                    year_filter,
                    topic_filter,
                    include_done,
                    int(n_questions),
                    quiz_mode,
                    int(target_minutes * 60),
                )
                if started:
                    st.rerun()
        with col_b:
            if st.button("Reset progress", use_container_width=True):
                st.session_state["confirm_reset"] = True

        if st.session_state.get("confirm_reset"):
            st.warning("This clears mastered-question progress, not attempt history.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Yes, reset", type="primary", use_container_width=True):
                    save_progress({"completed_correct": []})
                    st.session_state.pop("confirm_reset", None)
                    st.rerun()
            with c2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.pop("confirm_reset", None)
                    st.rerun()

    if st.session_state.get("quiz_done"):
        rows = st.session_state.get("quiz_results", [])
        summary = st.session_state.get("quiz_summary", {})
        n_q = summary.get("questions_attempted", 0)
        pct = round(summary.get("score_percent", 0))
        adjusted = round(summary.get("adjusted_score_percent", 0))
        color = "#4caf50" if pct >= 70 else "#ff9800" if pct >= 50 else "#f44336"

        st.markdown(
            f"<h2 style='color:{color}'>Quiz complete - {summary.get('correct', 0)}/{n_q} correct ({pct}%)</h2>"
            f"<p>Adjusted score: {adjusted}% · Time used: {fmt_time(summary.get('time_used', 0))} · "
            f"{summary.get('seconds_per_question', 0)} sec/question</p>",
            unsafe_allow_html=True,
        )

        metric_cols = st.columns(5)
        metric_cols[0].metric("Skipped", summary.get("skipped", 0))
        metric_cols[1].metric("Guessed/unsure", summary.get("guessed", 0))
        metric_cols[2].metric("Lucky correct", summary.get("lucky_correct", 0))
        metric_cols[3].metric("Slow review", summary.get("slow_review", 0))
        metric_cols[4].metric("Mode", summary.get("mode", "Timed test"))

        review_count = len(error_log_rows(rows))
        if st.session_state.get("error_log_exported"):
            st.success("Review rows already appended to error_log.md for this quiz.")
        elif review_count:
            if st.button(f"Append {review_count} review rows to error_log.md", type="primary"):
                written = append_error_log(rows)
                st.session_state.error_log_exported = True
                st.success(f"Added {written} rows to error_log.md")
        else:
            st.success("No missed, lucky, skipped or slow questions to log.")

        st.markdown("**Click any row to review the question, answer, and technique.**")
        q_by_id = {q["id"]: q for q in st.session_state.get("quiz_questions", [])}
        for r in rows:
            q = q_by_id[r["id"]]
            result_icon = "OK" if r["correct"] else "MISS"
            flags = []
            if r["skipped"]:
                flags.append("skipped")
            if r["lucky_correct"]:
                flags.append("lucky")
            if r["slow"]:
                flags.append("slow")
            flag_text = f" · {', '.join(flags)}" if flags else ""
            label = (
                f"{result_icon} Q{r['question_index']} · {r['source']} · {r['topic'].capitalize()} "
                f"· Your answer: {r['chosen']} · Correct: {r['correct_answer']} · {r['time_spent']}{flag_text}"
            )
            with st.expander(label, expanded=False):
                ecol_img, ecol_info = st.columns([3, 1])
                with ecol_img:
                    img_path = ROOT / q["image"]
                    if img_path.exists():
                        st.image(str(img_path), width=st.session_state.get("img_zoom", 600))
                    else:
                        st.warning(f"Image not found: {q['image']}")
                with ecol_info:
                    st.markdown(f"**Area:** {r['area']}")
                    st.markdown(f"**Confidence:** {r['confidence']}")
                    st.markdown(f"**Topic:** {r['topic']}")
                    st.markdown("---")
                    st.markdown(q.get("technique", "No technique note for this question."))

        if st.button("Start new quiz", type="primary"):
            for key in [
                "quiz_active", "quiz_done", "quiz_questions", "quiz_index",
                "quiz_answers", "quiz_confidence", "quiz_skipped", "quiz_q_times",
                "quiz_session_start", "quiz_q_start", "show_technique",
                "quiz_results", "quiz_summary", "error_log_exported",
            ]:
                st.session_state.pop(key, None)
            st.rerun()

    elif st.session_state.get("quiz_active"):
        keyboard_shortcuts()
        st_autorefresh(interval=1000, key="quiz_refresh")

        now = time.time()
        total_elapsed = now - st.session_state.quiz_session_start
        n_q = st.session_state.get("quiz_n_questions", 15)
        target_seconds = st.session_state.get("quiz_target_seconds", n_q * Q_TIME)
        idx = st.session_state.quiz_index
        q = st.session_state.quiz_questions[idx]
        q_accum = st.session_state.get("quiz_q_times", {}).get(q["id"], 0.0)
        q_elapsed = q_accum + (now - st.session_state.quiz_q_start)

        hcol1, hcol2, hcol3, hcol4 = st.columns([2, 2, 2, 2])
        hcol1.metric("Total", fmt_time(total_elapsed))
        hcol2.metric("Target", fmt_time(target_seconds), delta=fmt_time(target_seconds - total_elapsed))
        hcol3.metric("Progress", f"{idx + 1}/{n_q}")
        hcol4.markdown(
            f"<span style='font-size:16px;color:{q_timer_color(q_elapsed)}'>Question<br><b>{fmt_time(q_elapsed)}</b></span>",
            unsafe_allow_html=True,
        )

        st.progress(min(total_elapsed / max(target_seconds, 1), 1.0))
        st.caption(
            f"**{q['source']}** · {q.get('esat_area', infer_esat_area(q))} · "
            f"{q['module'].capitalize()} · {q['topic']} · keys: A-H, S skip, Enter next"
        )

        show_tech = st.session_state.get("show_technique", False)
        quiz_mode = st.session_state.get("quiz_mode", "Timed test")
        col_img, col_right = st.columns([3, 1])

        with col_img:
            img_zoom = st.slider("Zoom", 300, 1200, st.session_state.get("img_zoom", 600), step=50, key=f"zoom_{idx}")
            st.session_state["img_zoom"] = img_zoom
            img_path = ROOT / q["image"]
            if img_path.exists():
                st.image(str(img_path), width=img_zoom)
            else:
                st.warning(f"Image not found: {q['image']}")

        with col_right:
            if quiz_mode == "Timed test":
                st.caption("Technique hidden until review in Timed test mode.")
            else:
                toggle_label = "Hide technique" if show_tech else "Show technique"
                if st.button(toggle_label, key=f"tech_toggle_{idx}", use_container_width=True):
                    st.session_state.show_technique = not show_tech
                    st.rerun()
                if show_tech:
                    st.markdown(f"**Topic:** {q['topic']}")
                    st.markdown(q.get("technique", "No technique note for this question."))

            st.markdown("---")
            st.markdown("**Answer**")
            answer_letters = list("ABCDEFGH")
            chosen = st.session_state.quiz_answers.get(q["id"])
            for letter in answer_letters:
                btn_type = "primary" if chosen == letter else "secondary"
                if st.button(letter, key=f"ans_{idx}_{letter}", use_container_width=True, type=btn_type):
                    st.session_state.quiz_answers[q["id"]] = letter
                    st.session_state.quiz_skipped.discard(q["id"])

            st.radio(
                "Confidence",
                ["Confident", "Unsure", "Guess"],
                horizontal=True,
                key=f"conf_radio_{idx}",
                index=["Confident", "Unsure", "Guess"].index(
                    st.session_state.get("quiz_confidence", {}).get(q["id"], "Confident")
                ),
            )
            st.session_state.quiz_confidence[q["id"]] = st.session_state[f"conf_radio_{idx}"]

            st.markdown("---")
            if idx > 0:
                if st.button("Back", use_container_width=True):
                    record_q_time()
                    st.session_state.quiz_index -= 1
                    st.session_state.show_technique = False
                    st.rerun()
            if st.button("Skip", use_container_width=True):
                st.session_state.quiz_answers[q["id"]] = ""
                st.session_state.quiz_skipped.add(q["id"])
                if idx + 1 < n_q:
                    record_q_time()
                    st.session_state.quiz_index += 1
                    st.session_state.show_technique = False
                else:
                    end_quiz()
                st.rerun()
            next_label = "Finish" if idx + 1 == n_q else "Next"
            if st.button(next_label, type="primary", use_container_width=True):
                if q["id"] not in st.session_state.quiz_answers:
                    st.session_state.quiz_answers[q["id"]] = ""
                    st.session_state.quiz_skipped.add(q["id"])
                if idx + 1 < n_q:
                    record_q_time()
                    st.session_state.quiz_index += 1
                    st.session_state.show_technique = False
                else:
                    end_quiz()
                st.rerun()

    else:
        st.markdown("### How it works")
        cols = st.columns(4)
        steps = [
            ("1", "Pick mode", "Timed test, drill, or weak-topic repair"),
            ("2", "Filter", "Area, source, year and topic"),
            ("3", "Answer fast", "A-H keys, skip discipline, confidence marking"),
            ("4", "Review", "Adjusted score, attempt history and error-log export"),
        ]
        for col, (num, title, desc) in zip(cols, steps):
            with col:
                st.markdown(
                    f"<div style='background:#1a2a3a;padding:16px;border-radius:8px;text-align:center'>"
                    f"<b style='font-size:24px;color:#4caf50'>{num}</b><br>"
                    f"<b style='color:white'>{title}</b><br>"
                    f"<span style='color:#aaa;font-size:13px'>{desc}</span></div>",
                    unsafe_allow_html=True,
                )
        answered = len(all_questions)
        total_records = count_question_records()
        missing = total_records - answered
        st.info(
            f"Database: **{answered} usable questions** with answers. "
            f"{missing} extracted questions currently lack parsed answers. "
            "Run `python scripts/validate_question_bank.py` for coverage checks."
        )
