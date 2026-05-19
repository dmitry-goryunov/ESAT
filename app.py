import json
import random
import time
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="ESAT Prep Dashboard", layout="wide")

st.title("ESAT Preparation Dashboard")
st.caption("Maths 1 · Maths 2 · Physics — Oxbridge / Imperial target")

tab1, tab2, tab3, tab4 = st.tabs(["📅 12-Week Schedule", "📚 Papers Timetable", "📊 Paper Comparison", "🎯 Quiz"])

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
SCORES_FILE = ROOT / "scores.csv"

Q_TIME = 90  # seconds per question (1.5 min)


def load_questions() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding="utf-8") as f:
        return [q for q in json.load(f) if q.get("answer")]


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with PROGRESS_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    return {"completed_correct": []}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.parent.mkdir(exist_ok=True)
    with PROGRESS_FILE.open("w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def log_score(n_correct: int, time_used: float) -> None:
    import csv
    headers = ["date", "source", "questions_attempted", "correct",
               "time_minutes", "score_percent", "seconds_per_question"]
    n_q = st.session_state.get("quiz_n_questions", 15)
    row = {
        "date": str(date.today()),
        "source": "Quiz — mixed",
        "questions_attempted": n_q,
        "correct": n_correct,
        "time_minutes": round(time_used / 60, 1),
        "score_percent": round(n_correct / n_q * 100, 1),
        "seconds_per_question": round(time_used / n_q, 1),
    }
    exists = SCORES_FILE.exists()
    with SCORES_FILE.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def fmt_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def q_timer_color(remaining: float) -> str:
    if remaining > 45:
        return "#4caf50"
    if remaining > 15:
        return "#ff9800"
    return "#f44336"


def init_quiz(questions: list[dict], module_filter: str, include_done: bool, n_questions: int) -> None:
    progress = load_progress()
    done_ids = set(progress.get("completed_correct", []))
    pool = [q for q in questions if module_filter == "Both" or q["module"] == module_filter.lower()]
    if not include_done:
        pool = [q for q in pool if q["id"] not in done_ids]
    if len(pool) < n_questions:
        st.error(f"Not enough questions available ({len(pool)} found, need {n_questions}). "
                 "Enable 'Include already-correct questions' or choose a different module.")
        return
    selected = random.sample(pool, n_questions)
    total_time = int((n_questions * 1.5 + 1) * 60)
    st.session_state.quiz_active = True
    st.session_state.quiz_questions = selected
    st.session_state.quiz_n_questions = n_questions
    st.session_state.quiz_total_time = total_time
    st.session_state.quiz_index = 0
    st.session_state.quiz_answers = {}
    st.session_state.quiz_session_start = time.time()
    st.session_state.quiz_q_start = time.time()
    st.session_state.show_technique = False
    st.session_state.quiz_done = False
    st.session_state.quiz_submitted = False


def end_quiz() -> None:
    questions = st.session_state.quiz_questions
    answers = st.session_state.quiz_answers
    time_used = time.time() - st.session_state.quiz_session_start

    correct_ids = []
    n_correct = 0
    for q in questions:
        chosen = answers.get(q["id"], "")
        if chosen == q["answer"]:
            n_correct += 1
            correct_ids.append(q["id"])

    progress = load_progress()
    existing = set(progress.get("completed_correct", []))
    existing.update(correct_ids)
    progress["completed_correct"] = list(existing)
    save_progress(progress)
    log_score(n_correct, time_used)

    st.session_state.quiz_done = True
    st.session_state.quiz_n_correct = n_correct
    st.session_state.quiz_time_used = time_used


with tab4:
    all_questions = load_questions()

    # ── Sidebar-style controls in an expander ─────────────────────────────
    with st.expander("Quiz settings", expanded=not st.session_state.get("quiz_active", False)):
        module_filter = st.radio("Module", ["Both", "Maths", "Physics"], horizontal=True, key="module_filter")
        n_questions = st.number_input("Number of questions", min_value=1, max_value=50,
                                      value=15, step=1, key="n_questions_input")
        total_mins = round(n_questions * 1.5 + 1, 1)
        st.caption(f"Total time: **{total_mins} min** · {Q_TIME}s per question")
        include_done = st.checkbox("Include already-correct questions", value=False, key="include_done")

        progress_data = load_progress()
        done_count = len(progress_data.get("completed_correct", []))
        st.caption(f"{done_count} questions marked correct so far · {len(all_questions)} total available")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Start quiz", type="primary", use_container_width=True):
                init_quiz(all_questions, module_filter, include_done, int(n_questions))
                st.rerun()
        with col_b:
            if st.button("Reset progress", use_container_width=True):
                save_progress({"completed_correct": []})
                st.success("Progress reset.")
                st.rerun()

    # ── Quiz done screen ───────────────────────────────────────────────────
    if st.session_state.get("quiz_done"):
        n_correct = st.session_state.quiz_n_correct
        time_used = st.session_state.quiz_time_used
        n_q = st.session_state.get("quiz_n_questions", 15)
        pct = round(n_correct / n_q * 100)
        color = "#4caf50" if pct >= 70 else "#ff9800" if pct >= 50 else "#f44336"

        st.markdown(
            f"<h2 style='color:{color}'>Quiz complete — {n_correct}/{n_q} correct ({pct}%)</h2>"
            f"<p>Time used: {fmt_time(time_used)}</p>",
            unsafe_allow_html=True,
        )

        rows = []
        for i, q in enumerate(st.session_state.quiz_questions, 1):
            chosen = st.session_state.quiz_answers.get(q["id"], "—")
            correct = q["answer"]
            result = "✓" if chosen == correct else "✗"
            rows.append({
                "Q": i, "Source": q["source"], "Topic": q["topic"],
                "Your answer": chosen, "Correct": correct, "Result": result,
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

        if st.button("Start new quiz", type="primary"):
            for key in ["quiz_active", "quiz_done", "quiz_questions", "quiz_index",
                        "quiz_answers", "quiz_session_start", "quiz_q_start",
                        "show_technique", "quiz_submitted"]:
                st.session_state.pop(key, None)
            st.rerun()

    # ── Active quiz ────────────────────────────────────────────────────────
    elif st.session_state.get("quiz_active"):
        # 1-second auto-refresh while quiz is running
        st_autorefresh(interval=1000, key="quiz_refresh")

        now = time.time()
        total_elapsed = now - st.session_state.quiz_session_start
        n_q = st.session_state.get("quiz_n_questions", 15)
        total_time = st.session_state.get("quiz_total_time", int((n_q * 1.5 + 1) * 60))
        total_remaining = total_time - total_elapsed

        if total_remaining <= 0:
            end_quiz()
            st.rerun()

        idx = st.session_state.quiz_index
        q = st.session_state.quiz_questions[idx]

        q_elapsed = now - st.session_state.quiz_q_start
        q_remaining = Q_TIME - q_elapsed

        if q_remaining <= 0 and not st.session_state.get("quiz_submitted"):
            # Auto-advance: record no answer if not already set
            if q["id"] not in st.session_state.quiz_answers:
                st.session_state.quiz_answers[q["id"]] = ""
            if idx + 1 < n_q:
                st.session_state.quiz_index += 1
                st.session_state.quiz_q_start = time.time()
                st.session_state.show_technique = False
            else:
                end_quiz()
            st.rerun()

        # Header row: total timer + progress
        hcol1, hcol2, hcol3 = st.columns([3, 2, 1])
        with hcol1:
            t_color = q_timer_color(total_remaining)
            st.markdown(
                f"<span style='font-size:18px;color:{t_color}'>⏱ Total: <b>{fmt_time(total_remaining)}</b></span>",
                unsafe_allow_html=True,
            )
        with hcol2:
            st.markdown(
                f"<span style='font-size:16px;color:#aaa'>Q {idx + 1} / {n_q}</span>",
                unsafe_allow_html=True,
            )
        with hcol3:
            q_color = q_timer_color(q_remaining)
            st.markdown(
                f"<span style='font-size:16px;color:{q_color}'><b>{fmt_time(q_remaining)}</b></span>",
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Source tag
        st.caption(f"**{q['source']}** · {q['module'].capitalize()} · {q['topic']}")

        # Main layout: image left | answers + technique right
        show_tech = st.session_state.get("show_technique", False)
        col_img, col_right = st.columns([3, 1])

        with col_img:
            img_path = ROOT / q["image"]
            if img_path.exists():
                st.image(str(img_path), width=600)
            else:
                st.warning(f"Image not found: {q['image']}")

        with col_right:
            # Technique at top
            toggle_label = "Hide technique ▲" if show_tech else "Show technique ▼"
            if st.button(toggle_label, key=f"tech_toggle_{idx}", use_container_width=True):
                st.session_state.show_technique = not show_tech
                st.rerun()
            if show_tech:
                st.markdown(f"**Topic:** {q['topic']}")
                st.markdown(q.get("technique", "No technique note for this question."))

            st.markdown("---")

            # Answer buttons stacked vertically
            st.markdown("**Answer**")
            answer_letters = list("ABCDEFGH")
            chosen = st.session_state.quiz_answers.get(q["id"])
            for letter in answer_letters:
                btn_type = "primary" if chosen == letter else "secondary"
                if st.button(letter, key=f"ans_{idx}_{letter}",
                             use_container_width=True, type=btn_type):
                    st.session_state.quiz_answers[q["id"]] = letter

            st.markdown("---")

            # Navigation
            if idx > 0:
                if st.button("← Back", use_container_width=True):
                    st.session_state.quiz_index -= 1
                    st.session_state.quiz_q_start = time.time()
                    st.session_state.show_technique = False
                    st.rerun()
            if st.button("⏭ Skip", use_container_width=True):
                if q["id"] not in st.session_state.quiz_answers:
                    st.session_state.quiz_answers[q["id"]] = ""
                if idx + 1 < n_q:
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_q_start = time.time()
                    st.session_state.show_technique = False
                else:
                    end_quiz()
                st.rerun()
            next_label = "Finish" if idx + 1 == n_q else "Next →"
            if st.button(next_label, type="primary", use_container_width=True):
                if q["id"] not in st.session_state.quiz_answers:
                    st.session_state.quiz_answers[q["id"]] = ""
                if idx + 1 < n_q:
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_q_start = time.time()
                    st.session_state.show_technique = False
                else:
                    end_quiz()
                st.rerun()

    # ── Start screen ───────────────────────────────────────────────────────
    else:
        st.markdown("### How it works")
        cols = st.columns(4)
        steps = [
            ("1", "Choose module", "Maths, Physics, or Both"),
            ("2", "15 questions", "Randomly drawn from NSAA, ENGAA, TMUA, PAT"),
            ("3", "1.5 min / question", "25-minute total · ESAT pace"),
            ("4", "Score + log", "Correct questions removed from active pool"),
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
        st.markdown("")
        st.info(f"Database: **{len(all_questions)} questions** with answers · NSAA 2016–2023, ENGAA 2016–2023, TMUA, PAT")
