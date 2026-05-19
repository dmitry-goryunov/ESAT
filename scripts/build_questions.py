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

MANUAL_ANSWER_OVERRIDES = {
    "tmua_2016_q20": "D",
    "tmua_2017_q20": "E",
    "tmua_2018_q13": "C",
    "tmua_2018_q19": "D",
    "tmua_2021_q17": "A",
    "tmua_2023_q8": "B",
}

# ---------------------------------------------------------------------------
# Module assignment
# NSAA 2016-2019: Q1-18 = maths, Q19+ = physics
# NSAA 2020-2023: Q1-20 = maths, Q21+ = physics
# ENGAA 2016-2019: Q1-28 Part A (alternating maths/physics), odd=maths even=physics
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
        part_a_limit = 28 if year <= 2019 else 20
        if qnum <= part_a_limit:
            return "maths" if qnum % 2 == 1 else "physics"
        return "maths"
    return "maths"


# ---------------------------------------------------------------------------
# Topic assignment
# ---------------------------------------------------------------------------

NSAA_MATHS_TOPICS = {
    # Q1-6 tend to be straightforward algebra/arithmetic
    1: "algebra", 2: "algebra", 3: "algebra", 4: "probability",
    5: "algebra", 6: "geometry",
    # Q7-10: algebra / ratio core
    7: "algebra", 8: "algebra", 9: "ratio", 10: "algebra",
    # Q11-13: geometry
    11: "algebra", 12: "geometry", 13: "geometry",
    # Q14-15: probability
    14: "probability", 15: "algebra",
    # Q16-20: algebra / functions / ratio
    16: "algebra", 17: "ratio", 18: "algebra",
    19: "functions", 20: "algebra",
}

NSAA_PHYSICS_TOPICS = {
    # 2016-2019 format: Q19-36
    19: "mechanics", 20: "mechanics", 21: "nuclear",
    22: "mechanics", 23: "waves", 24: "waves", 25: "nuclear",
    26: "energy", 27: "energy", 28: "circuits",
    29: "circuits", 30: "mechanics", 31: "thermal",
    32: "circuits", 33: "waves", 34: "mechanics",
    35: "nuclear", 36: "mechanics",
    # 2020-2023 format: Q21-40
    37: "waves", 38: "circuits", 39: "thermal", 40: "mechanics",
}

ENGAA_MATHS_TOPICS = {
    # Part A odd questions are Maths (alternating pattern)
    1: "algebra", 3: "algebra", 5: "algebra", 7: "ratio",
    9: "geometry", 11: "algebra", 13: "functions", 15: "algebra",
    17: "geometry", 19: "probability", 21: "algebra", 23: "geometry",
    25: "algebra", 27: "algebra",
}

ENGAA_PHYSICS_TOPICS = {
    # Part A even questions are Physics
    2: "mechanics", 4: "mechanics", 6: "waves", 8: "circuits",
    10: "mechanics", 12: "energy", 14: "nuclear", 16: "waves",
    18: "circuits", 20: "mechanics", 22: "waves", 24: "thermal",
    26: "energy", 28: "mechanics",
}


# ---------------------------------------------------------------------------
# Topic techniques — sourced from strat file topic-map sections
# ---------------------------------------------------------------------------

TOPIC_TECHNIQUES = {
    "algebra": (
        "- Substitute answer options for awkward rearrangements.\n"
        "- Test simple values (x = 0, 1, −1) to eliminate symbolic options.\n"
        "- Factor before expanding.\n"
        "- For inequalities: solve normally, then check one test value.\n"
        "- For roots of quadratics: use sum/product or discriminant before the full formula."
    ),
    "ratio": (
        "- Use multipliers, not additive language.\n"
        "- Reverse percentages by dividing by the multiplier.\n"
        "- For combined ratios: make the shared quantity match.\n"
        "- For similar shapes: length scale k, area scale k², volume scale k³.\n"
        "- Average speed = total distance / total time, not average of speeds."
    ),
    "geometry": (
        "- Redraw diagrams cleanly.\n"
        "- Mark right angles, equal lengths, parallel lines and tangent points first.\n"
        "- Use area formulae before coordinate methods.\n"
        "- In bearings: draw North lines at each point and convert to triangle angles.\n"
        "- For similar triangles: write matching sides in the same order.\n"
        "- Radius to tangent is always perpendicular."
    ),
    "probability": (
        "- Use complement for 'at least one'.\n"
        "- Use a two-way table for category or gender/activity questions.\n"
        "- For without-replacement: reduce numerator and denominator after each draw.\n"
        "- Count ordered outcomes when dice or repeated draws are involved.\n"
        "- For two-stage problems: condition on the first draw."
    ),
    "sequences": (
        "- Write the first few terms and look for telescoping or a pattern.\n"
        "- Use the general term and set exponent equal to the target.\n"
        "- Sum = n/2 × (first + last) for arithmetic sequences.\n"
        "- For recurrence relations: generate terms, do not guess."
    ),
    "functions": (
        "- Track minimum point and intercepts through any transformation.\n"
        "- Use discriminant for tangency or no intersection (b² − 4ac = 0 for tangent).\n"
        "- Graph first when counting solutions — sketch both sides and count crossings.\n"
        "- For transformations: apply operations in order, track one key point."
    ),
    "trig": (
        "- Factor trig expressions and use identities before full solving.\n"
        "- Count solutions carefully across the given interval.\n"
        "- Use exact values (0°, 30°, 45°, 60°, 90°) to test or eliminate options.\n"
        "- Convert to a single trig function when possible."
    ),
    "graphs": (
        "- Identify whether the question needs gradient, area, intercept or asymptote.\n"
        "- Velocity-time: area = displacement; gradient = acceleration.\n"
        "- Distance-time: gradient = speed.\n"
        "- Momentum-time: gradient = resultant force.\n"
        "- Force-distance: area = work done."
    ),
    "mechanics": (
        "- Draw a free-body diagram.\n"
        "- Use resultant force, not just applied force.\n"
        "- For collisions: momentum first, then energy loss.\n"
        "- Impulse: force × time = change in momentum.\n"
        "- Use v² = u² + 2as when time is absent."
    ),
    "waves": (
        "- Always start with v = fλ.\n"
        "- Frequency stays constant across a medium boundary.\n"
        "- One oscillation: particle travels 4 × amplitude.\n"
        "- Echoes and ultrasound: path is there and back — halve the total.\n"
        "- Doppler/redshift: moving away → lower frequency, longer wavelength."
    ),
    "circuits": (
        "- Find equivalent resistance first.\n"
        "- Series: same current. Parallel: same potential difference.\n"
        "- Use P = IV, I²R or V²/R depending on which quantities are known.\n"
        "- For thermistor/variable-resistor questions: find fixed resistor from first condition, then reuse.\n"
        "- Trap: voltage is not fixed across one resistor in a changing series circuit."
    ),
    "nuclear": (
        "- Make an A/Z ledger.\n"
        "- Alpha: mass number −4, proton number −2.\n"
        "- Beta minus: mass number unchanged, proton number +1.\n"
        "- In fission: balance total mass number and proton number.\n"
        "- For half-life with background: subtract background count before halving."
    ),
    "energy": (
        "- Write an energy audit: input = useful + wasted.\n"
        "- Efficiency = useful output / input.\n"
        "- Power = energy / time.\n"
        "- Gravitational PE = mgh; use vertical height, not distance along slope.\n"
        "- For heating: energy = mcΔT, plus latent heat if there is a phase change."
    ),
    "thermal": (
        "- Conduction rate ∝ area × ΔT / length; poorer conductor → steeper temperature drop.\n"
        "- Radiation: dull black surfaces emit and absorb more than shiny surfaces.\n"
        "- Vacuum stops conduction and convection, not radiation.\n"
        "- For ice-water: check whether available heat melts all ice before calculating final temperature."
    ),
    "dimensional": (
        "- Check final units before any detailed calculation.\n"
        "- Power = J s⁻¹, pressure = N m⁻², charge = A·s.\n"
        "- Dimensionally impossible answer choices are always wrong.\n"
        "- Watch unit conversions: cm→m, g→kg, min→s, cm³→m³."
    ),
    "proportionality": (
        "- Identify the power law first (e.g. F ∝ r²).\n"
        "- Doubling r means F quadruples — no formula needed.\n"
        "- Length scale k → area k², volume k³.\n"
        "- Use proportionality before substituting numbers."
    ),
    "mixed": (
        "- Ask in order: Can I substitute? Can I eliminate by units? Can I use a limiting case? Only then derive.\n"
        "- Skip after 45 seconds with no clear route."
    ),
}


# ---------------------------------------------------------------------------
# Year-specific techniques — sourced directly from strat file year-by-year sections
# ---------------------------------------------------------------------------

SOURCE_YEAR_TECHNIQUES = {
    # ── NSAA ─────────────────────────────────────────────────────────────────
    "nsaa_2016": (
        "- A/Z ledger for all nuclear questions.\n"
        "- Scale before calculation for conduction and radiation questions.\n"
        "- Circuit: find current first, then resistor-specific power.\n"
        "- Velocity-time graph: area = distance; distinguish total distance from displacement.\n"
        "- Echo: find path length first, then divide by speed.\n"
        "- Maths: table for probability and mixtures; multipliers for depreciation; draw North at each point for bearings."
    ),
    "nsaa_2017": (
        "- Velocity-time graphs: isolate only the decelerating sections.\n"
        "- EM spectrum: use v = fλ.\n"
        "- Nuclear: balance A and Z before reading options.\n"
        "- Atom/nucleus density ratio: density ∝ 1/radius³ if mass is fixed.\n"
        "- Use known resistor power to infer branch current/voltage.\n"
        "- Maths: exterior angle = 360/n for regular polygons; for clocks use relative angular speed; volume scale = length scale cubed."
    ),
    "nsaa_2018": (
        "- Series circuit removal: infer supply voltage from original current × resistance.\n"
        "- Speed-time graph: average speed = total area / total time.\n"
        "- Half-life: identify background count before halving.\n"
        "- Terminal speed: set weight = drag (net force = 0).\n"
        "- V-I graph with series resistor: supply voltage is the constraint line.\n"
        "- Maths: two-group totals → table first; similar volumes → cube the scale factor; combined mean → use total sum, not average of averages."
    ),
    "nsaa_2019": (
        "- Wave amplitude: one oscillation means particle travels 4 × amplitude.\n"
        "- Diode + resistor: read diode voltage from V-I graph at the given current.\n"
        "- Gas compression at constant temperature: use pressure × volume = constant.\n"
        "- Motor effect balance: compare readings before and after to find the force difference.\n"
        "- Collisions: compute initial momentum and kinetic energy separately.\n"
        "- Maths: difference of squares for surds; sphere volume scaling = (new/old radius)³; exponent equations → convert to one base; transformations → move one vertex at a time."
    ),
    "nsaa_2020": (
        "- Thermal loss: input power × time minus mcΔT gives heat lost.\n"
        "- Ideal gas at constant temperature: pressure and density scale together.\n"
        "- Thermistors: infer the fixed resistor from the first condition, then reuse it.\n"
        "- Distance-time graph: use the final constant gradient to read speed.\n"
        "- Rocket: constant thrust + decreasing mass → increasing acceleration.\n"
        "- Maths: complement for dice probability; inverse cube → set t = k/x³; tan x = 100x → graph shape and asymptotes, not algebra."
    ),
    "nsaa_2021": (
        "- Power = VQ/t is often faster than finding current first.\n"
        "- Series lamps at fixed supply voltage: total power ∝ 1/R_total.\n"
        "- Momentum-time graph gradient = resultant force.\n"
        "- Wave encounter: use relative speed.\n"
        "- Heating graph: power P = mc × gradient of temperature-time graph.\n"
        "- Maths: tangent perpendicular to radius; equal-spending ratio → set initial amounts then subtract s; for q−p from quadratic roots → use discriminant separation."
    ),
    "nsaa_2022": (
        "- Magnetic force: find current from charge/time first.\n"
        "- Impulse: average force = change in momentum / contact time.\n"
        "- Ultrasound: difference in return times gives distance difference — halve the path.\n"
        "- V-I graph circuits: read values at the actual operating current/voltage intersection.\n"
        "- Spring energy: E ∝ x²; if E gives height, height ∝ E/m.\n"
        "- Maths: median/mean with repeated values → write ordered list; average speed → total distance / total time; polygon interior angle = 180 − 360/n."
    ),
    "nsaa_2023": (
        "- Stopping distance: work-energy (F × d = ΔKE) beats SUVAT.\n"
        "- Layered conduction: steeper temperature drop occurs in the poorer conductor.\n"
        "- Ice-water equilibrium: check whether available heat is enough to melt all ice before calculating final temperature.\n"
        "- Phase delay in glass: compare number of wavelengths fitting through the same thickness.\n"
        "- Floating block: extra submersion → extra upthrust from extra displaced volume.\n"
        "- Maths: coordinate area → shoelace or split into triangles; similar solids with area factor 2 → length factor √2, volume factor 2√2; trig optimisation → set u = sin x."
    ),
    # ── ENGAA ────────────────────────────────────────────────────────────────
    "engaa_2016": (
        "- A/Z ledger for all nuclear questions.\n"
        "- Proportionality for star radiation and inverse-square/root relations.\n"
        "- Wave particles: distance per cycle = 4 × amplitude.\n"
        "- Circuit: find current first, then resistor-specific power.\n"
        "- Velocity-time graph: separate total distance from displacement.\n"
        "- Pulleys and tensions: isolate one object at a time."
    ),
    "engaa_2017": (
        "- Algebraic options: test simple values before expanding.\n"
        "- Proportionality: identify powers first, then scale.\n"
        "- Mechanics: draw all forces and use resultant force.\n"
        "- Graph questions: decide area or gradient before reaching for a formula.\n"
        "- Statement questions: evaluate each statement independently."
    ),
    "engaa_2018": (
        "- Energy audit for all machine and efficiency questions.\n"
        "- Circuit reduction before any calculation.\n"
        "- Graph questions: use gradients.\n"
        "- Polynomial/factor questions: answer substitution is often faster than full factoring."
    ),
    "engaa_2019": (
        "- Physics: units first.\n"
        "- Powers-of-ten bookkeeping for numerical Physics answers.\n"
        "- Quadratics: complete the square or use discriminant.\n"
        "- Probability or multi-category data: table method.\n"
        "- Any mechanics with contact, tension or friction: free-body diagram first."
    ),
    "engaa_2020": (
        "- Apply a 20-second route test before starting any question.\n"
        "- Physics: formula recognition and unit checks before arithmetic.\n"
        "- Maths: substitution and special values.\n"
        "- Graph questions: mark area/gradient/intercept immediately."
    ),
    "engaa_2021": (
        "- Ratios and percentages: use multipliers.\n"
        "- Circuits: fixed-voltage constraint matters when resistance changes.\n"
        "- Transformers: power conservation is usually faster than current ratios.\n"
        "- Kinematics: use v² = u² + 2as when time is absent.\n"
        "- Similar shapes: do not confuse surface area scaling (k²) with volume scaling (k³)."
    ),
    "engaa_2022": (
        "- Ultrasound/echo: halve the travel path.\n"
        "- Work against resistance: distinguish useful work from energy lost.\n"
        "- Spring energy: proportional to extension squared.\n"
        "- Mean/median: write the ordered list explicitly.\n"
        "- Similar triangles: write matching sides in matching order."
    ),
    "engaa_2023": (
        "- Stopping distance: work-energy (F × d = ΔKE) beats SUVAT.\n"
        "- Spring graph: E = ½Fx and E ∝ x².\n"
        "- Layered conduction: steeper temperature drop in the poorer conductor.\n"
        "- Gas compression: use pressure ratios, not linear depth intuition.\n"
        "- Stationary waves: closed-open pipe fundamental = quarter-wave; open-open = half-wave.\n"
        "- Resistance reshaping: same volume → area changes when length changes."
    ),
    # ── TMUA ─────────────────────────────────────────────────────────────────
    "tmua_2016": (
        "- Generate first few terms for sequence questions.\n"
        "- Use graph intersections to count solutions — do not solve high-degree equations.\n"
        "- Use stationary points or graph shape rather than algebra.\n"
        "- Use substitution (x = 0, 1, −1) for algebraic identities.\n"
        "- Geometry: draw a clean diagram and introduce one variable."
    ),
    "tmua_2017": (
        "- Factor before expanding.\n"
        "- Use discriminant for 'no intersection' or 'two roots' (b² − 4ac < 0 / > 0).\n"
        "- Use special values for algebraic equivalence.\n"
        "- Use graph shape for function transformations.\n"
        "- Use sign/range checks before algebra."
    ),
    "tmua_2018": (
        "- Use first few terms for recurrence/series.\n"
        "- Binomial/combinatorics: target the requested coefficient only.\n"
        "- Functions: locate turning point or key intercept first.\n"
        "- Coordinate geometry: use symmetry if present.\n"
        "- Integration/area: sketch before calculating."
    ),
    "tmua_2019": (
        "- Use answer options to reduce algebra.\n"
        "- Complete the square for quadratic transformations.\n"
        "- Trig: convert to one trig function when possible.\n"
        "- Logs: check domains first.\n"
        "- Inequalities: use a factor/sign table."
    ),
    "tmua_2020": (
        "- Do not expand unless necessary.\n"
        "- Use symmetry and invariants.\n"
        "- Functions: track transformations through key points.\n"
        "- Equations: use substitution and check range.\n"
        "- Probability: define the sample space carefully."
    ),
    "tmua_2021": (
        "- Graph first for solution counting.\n"
        "- Transformations: track minimum/maximum points.\n"
        "- Use discriminant for tangency/intersection.\n"
        "- Use special values for identities.\n"
        "- Use sign charts for inequalities."
    ),
    "tmua_2022": (
        "- Reduce to a simpler variable when expressions are complicated.\n"
        "- Use endpoint and range checks.\n"
        "- Trig: count solutions carefully across the interval.\n"
        "- Circles/coordinate geometry: use centre and radius first.\n"
        "- Binomial/series: avoid full expansion — target required term."
    ),
    "tmua_2023": (
        "- Integrals with parameters: treat as linear equations in the integral.\n"
        "- 'Graphs do not meet': use discriminant.\n"
        "- Trig solution counts: factor and count the transformed angle range.\n"
        "- f(x) transformed minimums: track the minimum point, not the whole graph.\n"
        "- Maximise expressions in sin x: set u = sin x and optimise over −1 ≤ u ≤ 1.\n"
        "- Probability from finite integer choices: enumerate valid cases."
    ),
    "tmua_specimen": (
        "- Substitute before expanding (x = 0, 1, −1, 2; or θ = 0°, 30°, 45°, 60°, 90°).\n"
        "- Number of solutions: sketch both sides and count intersections.\n"
        "- Sequences: write first terms and identify the pattern.\n"
        "- Quadratic conditions: discriminant (< 0, = 0, > 0).\n"
        "- Binomial: target the requested term only."
    ),
    # ── PAT ──────────────────────────────────────────────────────────────────
    "pat_2017": (
        "- Units and scaling for quick MCQs.\n"
        "- Free-body diagrams for mechanics.\n"
        "- Symmetry and equivalent resistance for circuits.\n"
        "- Wave speed is separate from particle oscillation speed."
    ),
    "pat_2018": (
        "- Conservation of energy before force equations where possible.\n"
        "- Circular motion: compare required centripetal force with available force.\n"
        "- Graphs: label intercepts, gradients and limits.\n"
        "- Estimation: keep one significant figure until the final step."
    ),
    "pat_2019": (
        "- Break long questions into small physical statements.\n"
        "- Dimensional checks early.\n"
        "- Circuits: equivalent resistance or current conservation.\n"
        "- Optics/waves: draw rays or wavefronts before reaching for formulae."
    ),
    "pat_2020": (
        "- Energy methods for motion under gravity.\n"
        "- Proportionality for scaling questions.\n"
        "- Limiting cases to check formulae.\n"
        "- Clean sign convention for momentum/collisions."
    ),
    "pat_2021": (
        "- Forces: draw all forces and choose axes carefully.\n"
        "- Electrical power: choose P = IV, I²R, or V²/R based on which quantities are known.\n"
        "- Graph sketches: determine asymptotes and stationary points before drawing.\n"
        "- Multi-part questions: harvest early marks first."
    ),
    "pat_2022": (
        "- Conservation first.\n"
        "- Dimensional analysis for unfamiliar formulae.\n"
        "- Optics: draw the normal and ray path.\n"
        "- Waves: identify phase, path difference and wavelength.\n"
        "- Long algebra: define variables cleanly and avoid expanding too early."
    ),
    "pat_2023": (
        "- Equal kinetic energy: m₁v₁² = m₂v₂²; solve by square-root scaling.\n"
        "- Frequency estimate: speed / length scale.\n"
        "- Pulley displacement: count supporting rope segments.\n"
        "- Circuit symmetry can beat full calculation.\n"
        "- Dimensional analysis with base units.\n"
        "- Drag equilibrium: horizontal/vertical force ratio = tan θ.\n"
        "- Wave period = λ/v; particle travel per period = 4A."
    ),
    "pat_specimen": (
        "- Extract the governing conservation law for each question.\n"
        "- Shorter items first; use longer written questions for technique review only.\n"
        "- Draw physical diagrams: free-body, ray, circuit, wave path."
    ),
}


def get_source_year_key(qid: str) -> str:
    parts = qid.split("_")
    source = parts[0]
    year_or_spec = parts[1]
    return f"{source}_{year_or_spec}"


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

    elif source == "nsaa":
        if module == "maths":
            topic = NSAA_MATHS_TOPICS.get(qnum, "algebra")
        else:
            topic = NSAA_PHYSICS_TOPICS.get(qnum, "mechanics")

    elif source == "engaa":
        if module == "maths":
            topic = ENGAA_MATHS_TOPICS.get(qnum, "algebra")
        else:
            topic = ENGAA_PHYSICS_TOPICS.get(qnum, "mechanics")

    else:
        topic = "mixed"

    year_key = get_source_year_key(qid)
    year_tech = SOURCE_YEAR_TECHNIQUES.get(year_key, "")
    topic_tech = TOPIC_TECHNIQUES.get(topic, TOPIC_TECHNIQUES["mixed"])

    source_label = source.upper()
    year_part = parts[1].capitalize() if parts[1] == "specimen" else parts[1]

    if year_tech:
        technique = (
            f"**{source_label} {year_part} — paper techniques:**\n{year_tech}\n\n"
            f"**Topic ({topic}) — always apply:**\n{topic_tech}"
        )
    else:
        technique = f"**Topic ({topic}) — always apply:**\n{topic_tech}"

    return topic, technique


# ---------------------------------------------------------------------------
# Answer key parsing
# ---------------------------------------------------------------------------

def parse_answer_key(pdf_path: Path) -> dict[int, str]:
    """Parse NSAA/ENGAA answer-key PDF. Returns {q_num: answer_letter}.

    Handles three formats:
      1. Two-column numeric:   "1 G  46 A"  (NSAA/ENGAA 2016-2018)
      2. Single-column numeric: "1 F\n2 H"   (NSAA 2019-2020)
      3. Q-prefixed:           "Q1 E MATH"  (NSAA/ENGAA 2021+)
    """
    answers = {}
    try:
        with pdfplumber.open(str(pdf_path)) as p:
            text = "\n".join(pg.extract_text() or "" for pg in p.pages)
        if re.search(r"Q\d+\s+[A-H]", text):
            for match in re.finditer(r"Q(\d+)\s+([A-H])", text):
                answers[int(match.group(1))] = match.group(2)
        else:
            for match in re.finditer(r"\b(\d{1,2})\s+([A-H])\b", text):
                qnum = int(match.group(1))
                letter = match.group(2)
                if qnum not in answers:
                    answers[qnum] = letter
    except Exception as e:
        print(f"  WARNING: could not parse {pdf_path.name}: {e}")
    return answers


# Patterns for TMUA prose-format worked answers
_TMUA_QH = re.compile(r"Question\s*(\d+)", re.IGNORECASE)
_TMUA_ANS = re.compile(
    r"(?:"
    r"the\s*correct\s*answer\s*is\s*(?:(?:therefore|option)\s*)?"
    r"|the\s*correct\s*option\s*is\s*"
    r"|which\s*is\s*option\s*"
    r"|the\s*answer\s*is\s*(?:option\s*)?"
    r"|answer\s+is\s+(?:option\s+)?"
    r"|answer\s+as\s+option\s+"
    r"|this\s+is\s+option\s+"
    r"|giving\s+option\s+"
    r"|offered\s+option\s+is\s+"
    r")([A-H])",
    re.IGNORECASE,
)
_TMUA_FALLBACK = re.compile(r"\boption\s+([A-H])\b", re.IGNORECASE)


def _tmua_is_toc(text: str) -> bool:
    return len(_TMUA_QH.findall(text)) > 3


def _tmua_extract_answer(text: str) -> str:
    ms = _TMUA_ANS.findall(text)
    if ms:
        return ms[-1].upper()
    ms2 = _TMUA_FALLBACK.findall(text[-300:])
    if ms2:
        return ms2[-1].upper()
    return ""


def parse_tmua_answer_key(pdf_path: Path) -> dict[int, str]:
    """Parse a TMUA worked-answer PDF where answers appear in prose.

    Each page starts with 'Question N'; some questions span multiple pages.
    The correct answer appears in phrases like 'the answer is F', 'this is option C'.
    """
    answers: dict[int, str] = {}
    try:
        with pdfplumber.open(str(pdf_path)) as p:
            current_q: int | None = None
            acc = ""
            for page in p.pages:
                txt = page.extract_text() or ""
                q_match = _TMUA_QH.search(txt[:300]) if not _tmua_is_toc(txt) else None
                if q_match:
                    if current_q and current_q not in answers:
                        a = _tmua_extract_answer(acc)
                        if a:
                            answers[current_q] = a
                    current_q = int(q_match.group(1))
                    acc = txt
                else:
                    acc += "\n" + txt
            if current_q and current_q not in answers:
                a = _tmua_extract_answer(acc)
                if a:
                    answers[current_q] = a
    except Exception as e:
        print(f"  WARNING: could not parse {pdf_path.name}: {e}")
    return answers


def load_all_answer_keys() -> dict[str, dict[int, str]]:
    keys = {}

    for year in range(2016, 2024):
        path = ROOT / f"papers/nsaa/NSAA_{year}_S1_AnswerKey.pdf"
        k = parse_answer_key(path)
        if k:
            keys[f"nsaa_{year}"] = k

    for year in range(2016, 2024):
        path = ROOT / f"papers/engaa/ENGAA_{year}_S1_AnswerKey.pdf"
        k = parse_answer_key(path)
        if k:
            keys[f"engaa_{year}"] = k

    for year in range(2016, 2024):
        path = ROOT / f"papers/tmua/TMUA-{year}-paper-1-worked-answers.pdf"
        k = parse_tmua_answer_key(path)
        if k:
            keys[f"tmua_{year}"] = k

    path = ROOT / "papers/tmua/TMUA-early-specimen-paper-1-worked-answers.pdf"
    k = parse_tmua_answer_key(path)
    if k:
        keys["tmua_specimen"] = k

    return keys


def get_source_key(qid: str) -> str:
    parts = qid.split("_")
    source = parts[0]
    if source == "pat":
        return "pat_specimen" if parts[1] == "specimen" else f"pat_{parts[1]}"
    if source == "tmua":
        return "tmua_specimen" if parts[1] == "specimen" else f"tmua_{parts[1]}"
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


def get_exam_note(qid: str, topic: str, module: str) -> dict[str, str]:
    fastest = {
        "algebra": "Try option substitution or special values before expanding.",
        "ratio": "Convert to multipliers and compare scale factors directly.",
        "geometry": "Redraw the key triangle/shape and mark equal or perpendicular structure first.",
        "probability": "Build the sample space or use the complement before multiplying branches.",
        "functions": "Track intercepts, turning points and transformations rather than expanding.",
        "graphs": "Decide whether the graph is asking for area, gradient, intercept or crossings.",
        "sequences": "Generate early terms and look for a recurrence or telescoping pattern.",
        "mechanics": "Choose force, momentum or energy first; avoid mixing them mid-route.",
        "waves": "Start with v = fλ or path difference; halve echo paths.",
        "circuits": "Reduce the circuit or identify fixed voltage/current constraints first.",
        "nuclear": "Balance mass number and proton number in a ledger.",
        "energy": "Write input = useful + wasted, then choose the shortest energy equation.",
        "thermal": "Check transfer direction and whether all material changes state.",
    }.get(topic, "Try units, limiting cases, substitution or elimination before full derivation.")
    trap = {
        "algebra": "Expanding too early and losing the structure of the options.",
        "ratio": "Averaging ratios or speeds instead of totals.",
        "geometry": "Using the diagram as if it were to scale.",
        "probability": "Counting unordered outcomes when order matters.",
        "functions": "Transforming the whole expression when one key point is enough.",
        "graphs": "Confusing gradient with area.",
        "mechanics": "Using applied force where resultant force is needed.",
        "waves": "Forgetting that echo/ultrasound paths are there and back.",
        "circuits": "Assuming one resistor keeps the same voltage in a changing series circuit.",
        "nuclear": "Changing mass number during beta-minus decay.",
        "energy": "Using distance along a slope instead of vertical height.",
        "thermal": "Ignoring background/latent heat/equilibrium checks.",
    }.get(topic, "Committing to long algebra before checking options.")
    recognition = f"If a {topic} question looks long, first ask which option-killer applies: units, scale, graph shape or substitution."
    source = qid.split("_", 1)[0].upper()
    esat_value = "High" if source in {"NSAA", "ENGAA"} else "Medium" if source == "TMUA" else "Repair"
    if module == "physics" and source == "PAT":
        esat_value = "Concept repair"
    return {
        "fastest_route": fastest,
        "common_trap": trap,
        "recognition_trigger": recognition,
        "esat_value": esat_value,
    }


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

    image_files = sorted(f for f in IMAGES_DIR.glob("*.png") if not f.stem.startswith("pat_"))

    for img_path in image_files:
        qid = img_path.stem
        source_key = get_source_key(qid)
        qnum = get_qnum(qid)
        module = get_module(qid)
        topic, technique = get_topic_and_technique(qid, module)
        source_label = get_source_label(qid)

        answer_map = all_keys.get(source_key, {})
        answer = MANUAL_ANSWER_OVERRIDES.get(qid, answer_map.get(qnum, ""))

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
            "exam_note": get_exam_note(qid, topic, module),
        })

    OUT_FILE.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nWrote {len(questions)} questions to {OUT_FILE}")
    if missing_answers:
        print(f"\nMissing answers for {len(missing_answers)} questions (PAT and any parse failures):")
        for qid in missing_answers:
            print(f"  {qid}")
    print("\nDone.")


if __name__ == "__main__":
    build()
