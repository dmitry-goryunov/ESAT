"""
Extract question page images from past paper PDFs.

Run from the project root:
    python scripts/extract_question_images.py

Output: data/images/<id>.png  (one PNG per question entry in MANIFEST)
Then run build_questions.py to generate questions.json.

Page formulas (verified from existing extractions):
  NSAA all years:       page_idx = qnum + 1
  ENGAA all years:      page_idx = qnum + 1  (Part A only — Part B offset unverified)
  TMUA all years:       page_idx = qnum - 1  (no cover page)

Sources included:
  NSAA 2016-2023  — all questions (Q1-36 for 2016-2019, Q1-40 for 2020-2023)
  ENGAA 2016-2023 — Part A only (Q1-28 for 2016-2019, Q1-20 for 2020-2023)
  TMUA 2016-2023 + specimen — all 20 questions per paper

PAT excluded: wrong format for ESAT-style timed MCQ practice.
"""

from pathlib import Path
import pypdfium2 as pdfium

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "data" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

SCALE = 2.5  # ~180 DPI


def generate_manifest() -> list[tuple[str, str, int]]:
    entries = []

    # ── NSAA 2016-2023: all questions, page_idx = qnum + 1 ──────────────────
    for year in range(2016, 2024):
        max_q = 36 if year <= 2019 else 40
        pdf = f"papers/nsaa/NSAA_{year}_S1_QuestionPaper.pdf"
        for q in range(1, max_q + 1):
            entries.append((f"nsaa_{year}_q{q}", pdf, q + 1))

    # ── ENGAA 2016-2023: Part A only, page_idx = qnum + 1 ───────────────────
    # 2016-2019: Part A = Q1-28 (54 questions total, Part B offset unverified)
    # 2020-2023: Part A = Q1-20 (40 questions total, Part B offset unverified)
    for year in range(2016, 2024):
        part_a_limit = 28 if year <= 2019 else 20
        pdf = f"papers/engaa/ENGAA_{year}_S1_QuestionPaper.pdf"
        for q in range(1, part_a_limit + 1):
            entries.append((f"engaa_{year}_q{q}", pdf, q + 1))

    # ── TMUA 2016-2023: all 20 questions, page_idx = qnum - 1 ───────────────
    for year in range(2016, 2024):
        pdf = f"papers/tmua/TMUA-{year}-paper-1.pdf"
        for q in range(1, 21):
            entries.append((f"tmua_{year}_q{q}", pdf, q - 1))

    # ── TMUA specimen ────────────────────────────────────────────────────────
    for q in range(1, 21):
        entries.append((
            f"tmua_specimen_q{q}",
            "papers/tmua/TMUA-early-specimen-paper-1.pdf",
            q - 1,
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


def remove_pat_images():
    removed = 0
    for f in IMAGES_DIR.glob("pat_*.png"):
        f.unlink()
        removed += 1
    if removed:
        print(f"Removed {removed} PAT images.")


def main():
    remove_pat_images()

    manifest = generate_manifest()
    print(f"Manifest: {len(manifest)} question entries\n")

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
