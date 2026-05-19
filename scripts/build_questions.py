"""
Build data/questions.json from extracted images + answer keys + topic/technique maps.

Run from the project root:
    python scripts/build_questions.py

Requires: pdfplumber (already available)
"""

import json
import re
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "data" / "images"
OUT_FILE = ROOT / "data" / "questions.json"

# ---------------------------------------------------------------------------
# Module assignment
# NSAA 2016-2019: Q1-18 = maths, Q19+ = physics
# NSAA 2020-2023: Q1-20 = maths, Q21+ = physics
# ENGAA 2016-2019: Q1-28 Part A (alternating maths/physics), Q1-14 even=physics odd=maths
# ENGAA 2020-2023: Q1-20 Part A
# TMUA: all maths
# PAT: all physics
# ---------------------------------------------------------------------------

def get_module(qid: str) -> str:
    parts = qid.split("_")
    source = parts[0]
    if source == "tmua":
        return "maths"
    if source == "pat":
        return "physics"
    year = int(parts[1]) if parts[1].isdigit() else 0
    qnum = int(parts[-1].lstrip("q"))
    if source == "nsaa":
        if year <= 2019:
            return "maths" if qnum <= 18 else "physics"
        else:
            return "maths" if qnum <= 20 else "physics"
    if source == "engaa":
        # Part A: Q1-28 (2016-2019) or Q1-20 (2020+), alternating maths/physics
        # Odd Qs tend to be maths, even tend to be physics in Part A
        # Simplified: use strat file guidance that Part A is mixed
        # We assign by odd/even for Part A questions
        if year <= 2019:
            part_a_limit = 28
        else:
            part_a_limit = 20
        if qnum <= part_a_limit:
            return "maths" if qnum % 2 == 1 else "physics"
        return "maths"  # Part B default (advanced maths/physics)
    return "maths"


# ---------------------------------------------------------------------------
# Topic assignment — derived from strat files topic maps
# ---------------------------------------------------------------------------

NSAA_MATHS_TOPICS = {
    # algebra: Q7-Q10 range typically
    7: "algebra", 8: "algebra", 9: "ratio", 10: "algebra",
    12: "geometry", 13: "geometry", 14: "probability", 15: "algebra",
    16: "algebra", 17: "ratio", 18: "algebra",
    # 2020+ format
    3: "algebra", 4: "probability", 5: "algebra", 6: "geometry",
    11: "algebra", 20: "algebra",
}

NSAA_PHYSICS_TOPICS = {
    19: "mechanics", 20: "mechanics", 21: "nuclear",
    22: "mechanics", 23: "waves", 24: "waves", 25: "nuclear",
    26: "energy", 27: "energy", 28: "circuits",
    29: "circuits", 30: "mechanics", 31: "thermal",
    32: "circuits", 33: "waves", 34: "mechanics",
    35: "nuclear", 36: "mechanics", 37: "waves",
    38: "circuits", 39: "thermal", 40: "mechanics",
}

TOPIC_TECHNIQUES = {
    "algebra": "Substitute answer options when rearrangement is ugly. Try simple values (x=0, 1, -1) to eliminate symbolic options. Factor before expanding.",
    "ratio": "Use multipliers, not additive language. Reverse percentages by dividing by the multiplier. For combined ratios, make the shared quantity match.",
    "geometry": "Redraw diagrams cleanly. Mark right angles, equal lengths, parallel lines and tangents first. Use area formulae before coordinate methods.",
    "probability": "Use complement for 'at least one'. Use a two-way table for category questions. For without-replacement, reduce numerator and denominator after each draw.",
    "sequences": "Write first terms and look for telescoping. Use general term and set exponent to target. Sum = n/2(first + last) for arithmetic.",
    "functions": "Track minimum point and intercepts through any transformation. Use discriminant for tangency or no intersection. Graph first when counting solutions.",
    "trig": "Factor trig expressions, use identities, count solutions carefully across the interval. Use exact values (0°, 30°, 45°, 60°, 90°) to test options.",
    "graphs": "Identify gradient, area, intercept or asymptote before calculation. For velocity-time: area = displacement, gradient = acceleration.",
    "mechanics": "Draw a free-body diagram. Use resultant force, not just applied force. For collisions: momentum first, energy loss second. Use v²=u²+2as when time is absent.",
    "waves": "Start with v = fλ. Frequency stays constant across a medium boundary. One oscillation = 4A particle travel. Echo/ultrasound path is there and back (halve).",
    "circuits": "Find equivalent resistance first. Series: same current. Parallel: same voltage. Use P=IV, I²R or V²/R depending on which quantities are known.",
    "nuclear": "Make an A/Z ledger. Alpha: -4 mass, -2 proton. Beta minus: mass unchanged, proton +1. Background count must be subtracted before halving for half-life.",
    "energy": "Write an energy audit: input = useful + wasted. Efficiency = useful output / input. Power = energy / time. Gravitational PE = mgh.",
    "thermal": "For conduction: rate ∝ area × ΔT / length. Poorer conductor has steeper temperature drop. Latent heat required if phase change occurs.",
    "dimensional": "Check units of each answer choice before algebra. Dimensionally impossible options are always wrong. Power = J/s, pressure = N/m², charge = A·s.",
    "proportionality": "Identify the power law first. If F ∝ r²: doubling r means 4× F. No formula needed — read the exponent and apply scaling.",
    "mixed": "Ask in order: Can I substitute? Can I eliminate by units? Can I use a limiting case? Only then derive.",
}

def get_topic_and_technique(qid: str, module: str) -> tuple[str, str]:
    parts = qid.split("_")
    source = parts[0]
    qnum = int(parts[-1].lstrip("q"))

    if source == "tmua":
        topic = "algebra"
        if qnum in [6, 7, 14, 17, 18]:
            topic = "graphs"
        elif qnum in [12, 13]:
            topic = "geometry"
        elif qnum in [9, 20]:
            topic = "probability"
        elif qnum in [8, 19]:
            topic = "sequences"
        elif qnum in [2, 5]:
            topic = "functions"
        return topic, TOPIC_TECHNIQUES.get(topic, TOPIC_TECHNIQUES["mixed"])

    if source == "pat":
        topic = "mechanics"
        if qnum in [2]:
            topic = "probability"
        elif qnum in [3]:
            topic = "waves"
        return topic, TOPIC_TECHNIQUES.get(topic, TOPIC_TECHNIQUES["mixed"])

    if source == "nsaa":
        if module == "maths":
            topic = NSAA_MATHS_TOPICS.get(qnum, "algebra")
        else:
            topic = NSAA_PHYSICS_TOPICS.get(qnum, "physics")
            if topic == "physics":
                topic = "mechanics"
        return topic, TOPIC_TECHNIQUES.get(topic, TOPIC_TECHNIQUES["mixed"])

    if source == "engaa":
        topic = "algebra" if module == "maths" else "mechanics"
        return topic, TOPIC_TECHNIQUES.get(topic, TOPIC_TECHNIQUES["mixed"])

    return "mixed", TOPIC_TECHNIQUES["mixed"]


# ---------------------------------------------------------------------------
# Answer key parsing
# ---------------------------------------------------------------------------

def parse_answer_key(pdf_path: Path) -> dict[int, str]:
    """Parse a question-answer PDF and return {q_num: answer_letter}.

    Handles three formats seen across years:
      1. Two-column numeric:   "1 G  46 A"  (NSAA/ENGAA 2016-2018)
      2. Single-column numeric: "1 F\n2 H"   (NSAA 2019-2020)
      3. Q-prefixed:           "Q1 E MATH"  (NSAA/ENGAA 2021+)
    """
    answers = {}
    try:
        with pdfplumber.open(str(pdf_path)) as p:
            text = "\n".join(pg.extract_text() or "" for pg in p.pages)
        # Format 3: Q-prefixed — must check first to avoid partial matches
        if re.search(r"Q\d+\s+[A-H]", text):
            for match in re.finditer(r"Q(\d+)\s+([A-H])", text):
                answers[int(match.group(1))] = match.group(2)
        else:
            # Formats 1 & 2: plain "NUM LETTER" pairs (unanchored catches both columns)
            for match in re.finditer(r"\b(\d{1,2})\s+([A-H])\b", text):
                qnum = int(match.group(1))
                letter = match.group(2)
                if qnum not in answers:  # first match wins (left column first)
                    answers[qnum] = letter
    except Exception as e:
        print(f"  WARNING: could not parse {pdf_path.name}: {e}")
    return answers


def load_all_answer_keys() -> dict[str, dict[int, str]]:
    """Load answer keys for all sources. Returns {source_slug: {q_num: letter}}."""
    keys = {}

    # NSAA
    for year in range(2016, 2024):
        path = ROOT / f"papers/nsaa/NSAA_{year}_S1_AnswerKey.pdf"
        k = parse_answer_key(path)
        if k:
            keys[f"nsaa_{year}"] = k

    # ENGAA
    for year in range(2016, 2024):
        path = ROOT / f"papers/engaa/ENGAA_{year}_S1_AnswerKey.pdf"
        k = parse_answer_key(path)
        if k:
            keys[f"engaa_{year}"] = k

    # TMUA — answers embedded in worked-answer PDFs
    for year in range(2016, 2024):
        path = ROOT / f"papers/tmua/TMUA-{year}-paper-1-worked-answers.pdf"
        k = parse_answer_key(path)
        if k:
            keys[f"tmua_{year}"] = k
    # Specimen
    path = ROOT / "papers/tmua/TMUA-early-specimen-paper-1-worked-answers.pdf"
    k = parse_answer_key(path)
    if k:
        keys["tmua_specimen"] = k

    # PAT — no standard MCQ answer key; PAT questions are written-answer
    # We use placeholder "—" and note it in the question record
    for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023]:
        keys[f"pat_{year}"] = {}  # filled manually or left blank
    keys["pat_specimen"] = {}

    return keys


def get_source_key(qid: str) -> str:
    """Map qid like 'nsaa_2019_q7' to answer key slug like 'nsaa_2019'."""
    parts = qid.split("_")
    source = parts[0]
    if source == "pat":
        if parts[1] == "specimen":
            return "pat_specimen"
        return f"pat_{parts[1]}"
    if source == "tmua":
        if parts[1] == "specimen":
            return "tmua_specimen"
        return f"tmua_{parts[1]}"
    if source in ("nsaa", "engaa"):
        return f"{source}_{parts[1]}"
    return qid


def get_qnum(qid: str) -> int:
    return int(qid.split("_")[-1].lstrip("q"))


def get_source_label(qid: str) -> str:
    parts = qid.split("_")
    source = parts[0].upper()
    year = parts[1].capitalize() if parts[1] == "specimen" else parts[1]
    return f"{source} {year}"


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build():
    print("Loading answer keys...")
    all_keys = load_all_answer_keys()
    for slug, k in all_keys.items():
        print(f"  {slug}: {len(k)} answers")

    print("\nBuilding questions.json...")
    questions = []
    missing_answers = []

    image_files = sorted(IMAGES_DIR.glob("*.png"))

    for img_path in image_files:
        qid = img_path.stem
        source_key = get_source_key(qid)
        qnum = get_qnum(qid)
        module = get_module(qid)
        topic, technique = get_topic_and_technique(qid, module)
        source_label = get_source_label(qid)

        answer_map = all_keys.get(source_key, {})
        answer = answer_map.get(qnum, "")

        if not answer:
            missing_answers.append(qid)

        questions.append({
            "id": qid,
            "source": source_label,
            "module": module,
            "topic": topic,
            "image": f"data/images/{qid}.png",
            "answer": answer,
            "technique": technique,
        })

    OUT_FILE.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nWrote {len(questions)} questions to {OUT_FILE}")
    if missing_answers:
        print(f"\nMissing answers for {len(missing_answers)} questions (PAT and any parse failures):")
        for qid in missing_answers:
            print(f"  {qid}")
    print("\nDone. Review data/questions.json and fill in missing answers manually.")


if __name__ == "__main__":
    build()
