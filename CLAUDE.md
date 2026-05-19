# ESAT Preparation Project - Working Instructions

## Objective

Prepare for:
- ESAT Mathematics 1
- ESAT Mathematics 2
- ESAT Physics

Target: competitive Oxbridge / Imperial level performance.

The preparation focus is:
- timing
- pattern recognition
- algebra fluency
- rapid topic switching
- strategic skipping
- stamina under pressure

Do not turn this into olympiad, STEP or long-form proof preparation.

## Source of truth

`CLAUDE.md` is the source of truth for project rules.

Other files have narrower roles:

| File | Role |
|---|---|
| `schedule.md` | Day-by-day plan |
| `roadmap.md` | Phase milestones and gates |
| `strategy.md` | Exam technique only |
| `prep.md` | Source notes and reference material |
| `error_log.md` | Question-level mistakes |
| `score_dashboard.md` | Weekly performance metrics |
| `CHANGELOG.md` | Record of material changes |

Avoid duplicating the same rule across several files. If a rule belongs everywhere, put it here and refer to it elsewhere.

## Core training philosophy

ESAT is a speed and adaptability exam. The objective is not to produce perfect written solutions. The objective is to select the correct answer quickly and reliably.

Preferred training resembles sprint interval training:
- short timed sets
- aggressive pacing
- immediate review
- topic switching
- repeated correction of weak patterns

## Timing rules

| Situation | Action |
|---|---|
| Solvable immediately | Solve directly |
| Route visible but algebra long | Estimate or eliminate first |
| No clear route after 45 to 60 seconds | Guess strategically and move on |
| Two answers left | Use units, limiting cases or substitution |
| Question looks unusually long | Skip and return only if time remains |

Never allow one question to damage the whole module.

## Fast methods to prioritise

Use:
- ratio reasoning
- units and dimensions
- limiting cases
- symmetry
- proportionality
- graph shape recognition
- order-of-magnitude checks
- answer substitution where faster than derivation

Avoid:
- long derivations unless clearly short
- unnecessary substitution
- checking every option after the correct answer is already clear
- writing textbook-style solutions during timed work

## Paper hierarchy

Priority order:
1. ENGAA
2. NSAA
3. ESAT official specimens and samples
4. TMUA selected questions
5. Uploaded MCQ documents
6. PAT selected questions
7. Isaac Physics

Use ESAT official online material sparingly. Do not burn through it too early.

## PAT rule

PAT is supporting material, not the main ESAT benchmark.

Use PAT for:
- deeper Physics understanding
- mechanics
- electricity and circuits
- waves and optics
- graph interpretation
- unfamiliar modelling questions

Do not sit full PAT papers as routine ESAT timing practice. Extract selected questions into:
- `mocks/` for constructed timed sets
- `reviews/` for weak-topic repair

Keep original PAT papers and mark schemes in `papers/pat/`.

## Session standards

Preferred routine sessions:
- 15 questions
- 20 to 25 minutes
- no calculator
- immediate marking
- immediate logging of mistakes

Full modules:
- 27 questions where using ESAT material
- 40 minutes
- no calculator
- strict skipping discipline

Full simulations:
- 3 modules of 40 minutes
- realistic fatigue conditions
- minimal pauses
- used only after pacing is stable

## Balance across modules

Each normal week should include exposure to all three modules:

| Area | Minimum weekly exposure |
|---|---|
| Maths 1 fluency | 2 short sets or one full module |
| Maths 2 problem solving | 2 short sets or one full module |
| Physics | 2 short sets or one full module |
| Mixed pacing | 1 timed mixed block |
| Review | 1 dedicated error-log session |

Do not let Physics crowd out Maths, or TMUA crowd out ESAT-style speed.

## Readiness gates

Use these gates before increasing pressure:

| Gate | Requirement |
|---|---|
| Move from 15-question sets to 40-minute modules | 70 percent or better in two recent short sets within time |
| Move from single modules to double modules | average time per question below 1.7 minutes with no collapse in accuracy |
| Move from double modules to triple simulations | two back-to-back modules completed without rising careless errors |
| Reduce volume | careless errors rising for two sessions in a row |
| Add PAT repair | repeated conceptual error in one Physics topic |

## Review standards

Every timed session must produce:
- raw score
- adjusted score if guesses were lucky
- time used
- average time per question
- skipped questions
- guessed questions
- weak topics
- mistake categories
- next repair action

Every incorrect or lucky question must be logged in `error_log.md`.

Mistake categories:
- knowledge gap
- algebra slip
- careless arithmetic
- timing panic
- trap/misread
- overthinking
- stamina/fatigue
- method selection

## Quiz app standards

The Streamlit quiz should support three modes:
- Timed test: no technique shown until review
- Drill: technique may be shown during practice
- Weak-topic repair: prioritise topics from attempt history and error log

Every quiz attempt should track:
- chosen answer
- confidence: confident, unsure or guess
- skipped status
- time per question
- raw score
- adjusted score excluding lucky correct guesses
- slow questions needing review

Only confident, correct and not-slow answers should be marked as mastered.

Missed, skipped, lucky-correct and slow questions should be exported or copied into `error_log.md`.

`data/attempts.jsonl` stores per-question quiz history.
`data/progress.json` stores mastered-question progress only.
`scores.csv` stores quiz/session score summaries.

## Output standards

Use concise markdown, tables and explicit metrics.

Avoid:
- motivational filler
- repeated rules already present in this file
- unstructured notes
- changing the plan without evidence from scores or errors
- overwriting error logs without preserving prior entries

## When analysing questions or papers

Prioritise:
- fastest valid route
- shortcut method
- why the wrong answer was tempting
- whether the question is good ESAT practice
- how to recognise the pattern next time

Compare full derivation with exam-efficient method where useful.

## When editing project files

Make small, auditable changes.
Update `CHANGELOG.md` after material changes.
Do not duplicate content already covered in another file.
