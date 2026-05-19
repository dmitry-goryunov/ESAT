# Changelog

## 2026-05-19 - Quiz repair and dashboard pass

Improved the quiz app and question bank after the initial workflow upgrade.

Changed:
- fixed all six missing TMUA answers with documented manual overrides
- added extractor fallbacks for previously missed NSAA and ENGAA question images
- rebuilt `data/questions.json` to 668 usable questions with answers and images
- added per-question exam notes: fastest route, common trap, recognition trigger and ESAT value
- added a Weak Dashboard tab using `data/attempts.jsonl`
- added spaced reattempt scheduling for missed, lucky, skipped and slow questions
- added Paper mode to preserve original question order for simulation-style practice
- added source-aware answer options so TMUA uses fewer answer buttons than NSAA/ENGAA
- added Streamlit Cloud config and pinned deployment dependencies
- added pure quiz-logic helpers plus unit tests
- updated validation to report missing exam notes

Rationale:
- this makes the quiz less random-practice and more diagnostic repair, while keeping full-paper timing available

---

## 2026-05-19 - Quiz workflow upgrade

Upgraded the Streamlit quiz workflow.

Changed:
- added timed test, drill and weak-topic repair modes
- added ESAT area, source, year and topic filters
- added 15-question, 27-question and 40-minute timing presets
- added confidence marking for confident, unsure and guessed answers
- added adjusted scoring so lucky correct answers do not count as mastered
- added skipped, guessed, lucky-correct and slow-question metrics
- added persistent per-question attempt history in `data/attempts.jsonl`
- added one-click export of missed, lucky, skipped and slow questions to `error_log.md`
- added keyboard shortcuts for answer selection, skip, next and back
- fixed quiz-start error handling so failed starts no longer immediately rerun
- fixed final-question skip timing so the last question is not double-counted
- added `scripts/validate_question_bank.py` to report missing answers, missing images, gaps and answer distribution
- corrected the quiz database message so it reports usable question count instead of claiming complete coverage

Rationale:
- the quiz now matches the project rules for speed, strategic skipping, adjusted scores and immediate diagnostic review

---

## 2026-05-19 - Added technique.md

Added `technique.md` with deployable quick-win techniques: answer substitution, dimensional elimination, limiting cases, ratio and proportionality, graph shape recognition, order-of-magnitude checks, pacing rules, trap patterns, and session habits.

---

## 2026-05-19 - Cleanup and consolidation

Cleaned the ESAT preparation project structure.

Changed:
- made `CLAUDE.md` the explicit source of truth
- reduced duplication across `prep.md`, `roadmap.md`, `strategy.md` and `schedule.md`
- narrowed `strategy.md` to exam technique only
- narrowed `prep.md` to reference notes and source assessment only
- added readiness gates to `roadmap.md`
- upgraded `error_log.md` with timing, chosen answer, correct answer, faster method and reattempt fields
- added `score_dashboard.md` for weekly module-level tracking
- revised `schedule.md` to balance Maths 1, Maths 2 and Physics more explicitly
- made triple simulations conditional rather than automatic every week

Rationale:
- the previous version had good strategy but repeated the same rules across several files
- score tracking was too light for diagnosing timing versus knowledge problems
- the plan needed clearer Maths 1 / Maths 2 / Physics balance

---

## 2026-05-17 (3)

Added official ESAT materials to `papers/esat/`:
- ESAT_Guide_Mathematics1_June2025.pdf
- ESAT_Guide_Physics_June2025.pdf
- ESAT_Guide_Mathematics2_June2025.pdf
- ESAT_Content_Specification_April2025.pdf

Source: UAT-UK (esat-tmua.ac.uk)

---

## 2026-05-17 (2)

Added `schedule.md` with a 12-week preparation schedule.

---

## 2026-05-17

Updated ESAT preparation project structure.

Changed:
- added `papers/pat/`
- removed separate mark scheme / answer subfolders
- kept each exam type in one folder
- clarified that papers, mark schemes, official solutions and examiner reports live together
- updated paper hierarchy to include PAT selected questions
