# Cleanup Notes

## What was cleaned

The original project had the right ESAT philosophy, but the same rules appeared in several places. This made the repository harder to maintain.

The cleanup applies a clearer file architecture:

| Area | Before | After |
|---|---|---|
| Source of truth | spread across several files | `CLAUDE.md` owns project rules |
| Strategy | mixed with PAT and folder guidance | `strategy.md` contains exam technique only |
| Preparation notes | repeated schedule and strategy | `prep.md` contains reference notes and source assessment only |
| Roadmap | phase goals only | phase goals plus readiness gates |
| Schedule | heavy but rigid | balanced Maths 1 / Maths 2 / Physics schedule with conditional triple sims |
| Error log | basic mistake table | full diagnostic table with timing, chosen answer, correct answer, faster method and reattempt |
| Score tracking | simple weekly table inside schedule | separate `score_dashboard.md` for module-level tracking |

## Main design decisions

1. Keep `CLAUDE.md` as the single source of truth.
2. Keep `schedule.md` operational and avoid repeating strategy explanations there.
3. Keep `strategy.md` short enough to be read before timed practice.
4. Make official ESAT material start from Week 6 only.
5. Make triple simulations conditional until the student is ready.
6. Track Maths 1, Maths 2 and Physics separately to avoid hidden imbalance.
7. Log not only wrong answers, but also lucky guesses and badly timed questions.

## Files added

| File | Purpose |
|---|---|
| `score_dashboard.md` | weekly and session-level score tracking |
| `CLEANUP_NOTES.md` | explanation of the cleanup |

## Files materially changed

| File | Change |
|---|---|
| `CLAUDE.md` | consolidated rules and removed repeated material |
| `schedule.md` | revised and balanced across modules |
| `error_log.md` | upgraded into diagnostic log |
| `roadmap.md` | added readiness gates |
| `strategy.md` | narrowed to exam technique only |
| `prep.md` | narrowed to reference notes |
| `README.md` | simplified file map and workflow |
| `CHANGELOG.md` | added 2026-05-19 cleanup entry |
