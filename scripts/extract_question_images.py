"""
Extract question page images from past paper PDFs.

Run from the project root:
    python scripts/extract_question_images.py

Output: data/images/<id>.png  (one PNG per question entry in MANIFEST)
Then run build_questions.py to generate questions.json.

Page finding (NSAA / ENGAA):
  Each PDF is scanned page-by-page. The current section (PART A, PART B, ...)
  is tracked via page headers and carried forward to pages that have no header.
  Questions are only collected from allowed parts.

  NSAA: include PART A (Mathematics) and PART B (Physics) — exclude Chemistry, Biology, etc.
  ENGAA: include PART A (Mathematics and Physics) only — exclude PART B (Advanced).

TMUA page layout (verified by inspection):
  2016 + specimen: 2 questions per page, Q1/Q2 at index 2 → page_idx = (qnum-1)//2 + 2
  2017-2023:       1 question per page,  Q1 at index 2    → page_idx = qnum + 1

Sources included:
  NSAA 2016-2023  — Maths (Part A) + Physics (Part B) only
  ENGAA 2016-2023 — Section 1 Part A only (accessible Maths + Physics)
  TMUA 2016-2023 + specimen — all 20 questions per paper
"""

import re
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "data" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

SCALE = 2.5  # ~180 DPI

_PART_NAMES = ("PART A", "PART B", "PART C", "PART D", "PART E")
# Matches a 1-2 digit question number at the start of a line, followed by a capital letter.
_Q_NUM = re.compile(r"(?:^|\n)(\d{1,2}) [A-Z]")


def scan_question_pages(
    pdf_path: Path,
    include_parts: tuple[str, ...] | None,
    max_q: int,
) -> dict[int, int]:
    """
    Scan a PDF and return {question_number: page_idx}.

    Tracks the current named part (PART A, PART B, ...) as a running header
    across pages that don't explicitly name their part. Questions are only
    collected when the current part is in include_parts (or include_parts is
    None, which accepts all pages).
    """
    q_to_page: dict[int, int] = {}
    current_part: str | None = None

    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for idx, page in enumerate(pdf.pages):
                text = page.extract_text() or ""

                # Update tracked part when this page has an explicit part header.
                for pname in _PART_NAMES:
                    if pname in text:
                        current_part = pname
                        break

                # Skip pages outside the allowed parts.
                if include_parts is not None and current_part not in include_parts:
                    continue

                # Collect question numbers from this page.
                for m in _Q_NUM.finditer(text):
                    qnum = int(m.group(1))
                    if 1 <= qnum <= max_q and qnum not in q_to_page:
                        q_to_page[qnum] = idx
    except Exception as e:
        print(f"  WARNING: could not scan {pdf_path.name}: {e}")

    return q_to_page


def generate_manifest() -> list[tuple[str, str, int]]:
    entries = []

    # ── NSAA 2016-2023: Part A (Maths) + Part B (Physics) only ─────────────
    # Chemistry (Part C), Biology (Part D), and Advanced (Part E) are excluded.
    for year in range(2016, 2024):
        max_q = 36 if year <= 2019 else 40
        rel_pdf = f"papers/nsaa/NSAA_{year}_S1_QuestionPaper.pdf"
        pdf_path = ROOT / rel_pdf
        if not pdf_path.exists():
            print(f"  SKIP (PDF not found): {pdf_path.name}")
            continue
        q_pages = scan_question_pages(
            pdf_path, include_parts=("PART A", "PART B"), max_q=max_q
        )
        print(f"  NSAA {year}: {len(q_pages)}/{max_q} pages found")
        for q in range(1, max_q + 1):
            if q in q_pages:
                entries.append((f"nsaa_{year}_q{q}", rel_pdf, q_pages[q]))
            else:
                print(f"    WARNING: nsaa_{year}_q{q} not found in scan")

    # ── ENGAA 2016-2023: Section 1 Part A only ──────────────────────────────
    # Part A is the accessible Maths+Physics section (no running header on
    # question pages; part is carried forward from the section header page).
    # Part B is "Advanced Mathematics and Advanced Physics" — excluded.
    for year in range(2016, 2024):
        # Generous cap; scan will only find questions actually in Part A.
        max_q = 35
        rel_pdf = f"papers/engaa/ENGAA_{year}_S1_QuestionPaper.pdf"
        pdf_path = ROOT / rel_pdf
        if not pdf_path.exists():
            print(f"  SKIP (PDF not found): {pdf_path.name}")
            continue
        q_pages = scan_question_pages(
            pdf_path, include_parts=("PART A",), max_q=max_q
        )
        print(f"  ENGAA {year}: {len(q_pages)}/{max_q} pages found")
        for q in sorted(q_pages):
            entries.append((f"engaa_{year}_q{q}", rel_pdf, q_pages[q]))

    # ── TMUA 2016: 2 questions per page, Q1+Q2 share index 2 ────────────────
    rel_pdf_2016 = "papers/tmua/TMUA-2016-paper-1.pdf"
    for q in range(1, 21):
        entries.append((f"tmua_2016_q{q}", rel_pdf_2016, (q - 1) // 2 + 2))

    # ── TMUA 2017-2023: 1 question per page, Q1 at index 2 ──────────────────
    for year in range(2017, 2024):
        rel_pdf = f"papers/tmua/TMUA-{year}-paper-1.pdf"
        for q in range(1, 21):
            entries.append((f"tmua_{year}_q{q}", rel_pdf, q + 1))

    # ── TMUA specimen: 2 questions per page, Q1+Q2 share index 2 ────────────
    for q in range(1, 21):
        entries.append((
            f"tmua_specimen_q{q}",
            "papers/tmua/TMUA-early-specimen-paper-1.pdf",
            (q - 1) // 2 + 2,
        ))

    return entries


def extract_page(pdf_path: Path, page_idx: int, out_path: Path) -> bool:
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


def remove_stale_images():
    """Delete existing NSAA, ENGAA, and PAT images so they are re-extracted correctly."""
    removed = 0
    for pattern in ("nsaa_*.png", "engaa_*.png", "pat_*.png", "tmua_*.png"):
        for f in IMAGES_DIR.glob(pattern):
            f.unlink()
            removed += 1
    if removed:
        print(f"Removed {removed} stale NSAA/ENGAA/PAT/TMUA images (will re-extract).\n")


def main():
    remove_stale_images()

    print("Scanning PDFs for question page positions...\n")
    manifest = generate_manifest()
    print(f"\nManifest: {len(manifest)} question entries\n")

    ok = 0
    skipped = 0
    for qid, rel_pdf, page_idx in manifest:
        out_path = IMAGES_DIR / f"{qid}.png"
        if out_path.exists():
            ok += 1
            continue
        pdf_path = ROOT / rel_pdf
        print(f"Extracting {qid} (page {page_idx + 1}) ...", end=" ")
        if extract_page(pdf_path, page_idx, out_path):
            print("OK")
            ok += 1
        else:
            skipped += 1

    print(f"\nDone. {ok} extracted/existing, {skipped} skipped.")
    print(f"Images in: {IMAGES_DIR}")
    print("\nNext: python scripts/build_questions.py")


if __name__ == "__main__":
    main()
