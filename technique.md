# ESAT Technique Quick Wins

Fast, deployable techniques that work from session one without new content knowledge.

## Method selection hierarchy

Always ask in this order before starting a question:

1. Can I substitute an answer choice and check?
2. Can I eliminate using units or dimensions?
3. Can I use a limiting case (0, 1, ∞)?
4. Can I use symmetry or proportionality?
5. Only then: derive from scratch.

---

## Quick win techniques

### Answer substitution

Plug answer choices back into the question instead of solving algebraically.

| When to use | How |
|---|---|
| Equation with a numerical answer | Try the middle answer first; if too big go down, if too small go up |
| Quadratic or polynomial | Substitute each option, stop when it works |
| Physics with units and numbers | Check one option dimensionally before solving |

Saves 30 to 90 seconds per question on algebra-heavy Maths 1 and Maths 2 questions.

---

### Dimensional elimination

Check units of each answer choice before doing any algebra.

| When to use | Example |
|---|---|
| Any Physics quantity question | If the answer should be in watts, eliminate options in joules or newtons immediately |
| Formula derivation | A dimensionally inconsistent option is always wrong |
| Speed, force, energy, power, charge | Units are sufficient to eliminate 2 to 3 options in under 10 seconds |

Costs nothing. Do it as a reflex on every Physics question.

---

### Limiting cases

Set a variable to 0, 1, or ∞ and check which answer survives.

| Limit | Use |
|---|---|
| Set angle to 0° or 90° | Eliminates wrong trig expressions immediately |
| Set mass or length to 0 | Wrong energy or momentum formulae collapse |
| Set n to 1 in a sequence | Validates or eliminates general-term expressions |
| Let resistance → 0 or → ∞ | Checks circuit formulae without full derivation |

Works on both Maths and Physics. Takes 10 to 20 seconds.

---

### Ratio and proportionality

If a quantity doubles, identify what happens to the target without deriving.

| Pattern | Application |
|---|---|
| Power laws: F ∝ r² | If r doubles, F quadruples — no formula needed |
| Ohm's law, kinetic energy | Read proportionality directly from the relationship |
| Scaling questions | Identify the exponent, apply scaling, ignore constants |

Faster than substituting numbers for any scaling question.

---

### Graph shape recognition

Match the described relationship to a known curve shape without plotting.

| Relationship | Shape |
|---|---|
| Linear y = mx + c | Straight line, non-zero intercept |
| y ∝ x² | Parabola through origin |
| y ∝ 1/x | Hyperbola, never touches axes |
| y = e^x or decay | Exponential, check intercept and asymptote |
| y = sin x or cos x | Period, amplitude, phase shift |

On graph questions, identify the correct shape first, then use intercept or asymptote to narrow to one option.

---

### Order-of-magnitude checks

Estimate the answer before computing. Eliminates options that are 10× too big or small.

| When to use | Method |
|---|---|
| Any numerical Physics question | Round everything to 1 significant figure and compute |
| Maths questions with large numbers | Check whether the answer is in the hundreds, thousands, or millions |
| After computing | Verify your answer is the right order before selecting |

Takes 5 to 10 seconds. Catches arithmetic errors and wrong-formula errors.

---

## Pacing quick wins

| Situation | Action | Why |
|---|---|---|
| No clear route after 45 seconds | Eliminate what you can, guess, move on | One stuck question costs three easy ones at the end |
| Two options remain | Apply limiting case or units — do not re-derive | Re-derivation at this stage rarely changes the answer |
| Question is longer than 5 lines | Skip immediately on first pass, return only if time allows | Long questions take disproportionate time relative to their mark |
| You have computed an answer not in the options | Check arithmetic once, then pick nearest option and move | Do not re-derive from scratch under time pressure |

---

## Trap patterns

Recognising traps is faster than solving carefully.

| Trap | What it looks like | Counter |
|---|---|---|
| Sign error bait | Answer choices differ only by a sign | Check direction conventions before substituting |
| Off-by-one in sequences | Two adjacent options that differ by one term | Verify n=1 case explicitly |
| Rounding bait | Options clustered within 5 percent of each other | Carry one extra significant figure through the calculation |
| Dimension match but wrong formula | Two options with the same units | Use a limiting case to separate them |
| Plausible distractor | The most natural wrong answer appears as an option | Slow down for 5 seconds on questions where one option feels too obvious |

---

## Session habits that compound quickly

| Habit | Frequency | Effect |
|---|---|---|
| Log every wrong or lucky question in `error_log.md` | Every session | Turns mistakes into searchable patterns within two weeks |
| Record time used, not just score | Every session | Exposes whether the problem is speed or knowledge |
| Sunday error review before new questions | Every week | Stops the same mistake repeating across sessions |
| Identify the faster method for every logged question | Every session | Builds a personal shortcut library over 12 weeks |
