# technique.md

# ESAT Technique Manual: consolidated from NSAA, ENGAA, TMUA and PAT

Purpose: one master shortcut manual for ESAT preparation.  
Sources used as technique drills:
- NSAA Maths and Physics, 2016 to 2023.
- ENGAA Section 1 relevant Maths/Physics, 2016 to 2023.
- TMUA Paper 1 relevant Maths, 2016 to 2023.
- PAT relevant Maths/Physics, 2017 to 2024 specimen.

Core rule:

> Fast correct elimination beats elegant derivation.

---

## 1. Universal timing rules

### 20-second route test

Before solving:

1. Can I identify the type?
2. Can I eliminate by units, sign, graph shape, special value or scale?
3. Is the full route under 60 seconds?
4. Is this question long for one mark?

If no route appears, eliminate, mark, guess if necessary and move on.

### 45-second warning

If after 45 seconds there is no real progress, stop deriving. Switch technique or move on.

### Two-options-left rule

Once only two options remain, do not restart the full solution. Use:
- units
- limiting case
- sign
- graph shape
- special value
- proportionality

---

## 2. First 10-second trigger table

| What you see | First technique |
|---|---|
| Numerical options | Estimate or substitute |
| Algebraic options | Substitute x = 0, 1, -1, 2 |
| Formula options | Dimensional check |
| Ratio/percentage | Multipliers or convenient total |
| Probability | Table, complement or outcome count |
| Sequence | Test n = 1, 2, 3 |
| Trig | Special angles or interval count |
| Graph | Area, gradient, intercept or asymptote |
| Circuit | Reduce circuit, find current |
| Nuclear | A/Z ledger |
| Wave | v = fλ; decide wave versus particle motion |
| Mechanics | Free-body diagram |
| Energy/power | Input/useful/wasted audit |
| Optics | Ray diagram and limiting case |
| Geometry | Redraw and mark invariants |

---

## 3. Maths techniques

### 3.1 Substitution and special values

Use when:
- options are algebraic
- expression equivalence is asked
- expansion looks long
- rearrangement options are messy

Values:
- x = 0
- x = 1
- x = -1
- x = 2
- n = 1 and n = 2
- θ = 0°, 30°, 45°, 60°, 90° where legal

Do not expand first unless substitution fails.

---

### 3.2 Quadratics and functions

| Problem | Fast method |
|---|---|
| no intersection | discriminant < 0 |
| tangent | discriminant = 0 |
| two intersections | discriminant > 0 |
| minimum/maximum | complete the square |
| root difference | use discriminant/root separation |
| graph transformation | track vertex or one key point |
| range/domain | check restrictions before simplifying |
| solution count | sketch both sides |

TMUA and ENGAA lesson: the discriminant is often faster than solving.

---

### 3.3 Graphs and transformations

Before algebra, ask:
- What is the shape?
- What are the intercepts?
- What are the asymptotes?
- What happens under translation/reflection/stretch?
- What point is easiest to track?

Transformation rule:
Track one point at a time, in the stated order.

---

### 3.4 Ratios, percentages and proportionality

Use multipliers.

| Language | Multiplier |
|---|---:|
| increase by 20% | ×1.20 |
| decrease by 20% | ×0.80 |
| 700% more | ×8 |
| 25% reduction | ×0.75 |
| reverse 25% reduction | divide by 0.75 |

Scaling:
- length scale = k
- area scale = k²
- volume scale = k³
- surface area of sphere/cylinder ∝ length²
- volume of sphere/cylinder/cone ∝ length³

---

### 3.5 Probability

Use:
- complement for “at least one”
- table for categories
- tree only for sequential dependence
- outcome counting for dice
- ordered outcomes for repeated trials unless stated otherwise

Common trap:
Do not mix ordered and unordered counting.

---

### 3.6 Geometry and trigonometry

Geometry:
- redraw cleanly
- mark equal lengths, right angles, tangents and parallels
- use similarity before coordinate algebra
- use area formulae before long algebra
- for bearings, draw North at each point

Trigonometry:
- test special angles
- factor identities
- count the full interval
- use substitution such as u = sin x for optimisation
- check quadrant signs

---

### 3.7 Binomial, sequences and series

Binomial:
- target only the requested term
- write the general term
- match power of x

Sequences:
- write first few terms
- test n = 1
- watch off-by-one errors

Series:
- look for telescoping
- check convergence before using sum to infinity

---

## 4. Physics techniques

### 4.1 Units and dimensional analysis

Use units first for unfamiliar formulae.

| Quantity | Unit shortcut |
|---|---|
| energy | J = N m |
| power | W = J s^-1 |
| pressure | Pa = N m^-2 |
| charge | C = A s |
| momentum | kg m s^-1 |
| force | N = kg m s^-2 |
| density | kg m^-3 |
| resistance | Ω = V A^-1 |

PAT lesson: dimensional analysis can build the whole formula when content memory is weak.

---

### 4.2 Graph meaning

| Graph | Meaning |
|---|---|
| distance-time | gradient = speed |
| velocity-time | gradient = acceleration, area = displacement |
| speed-time | area = distance |
| momentum-time | gradient = resultant force |
| force-distance | area = work done |
| current-voltage | read axes before using gradient |
| temperature-time | gradient linked to power and heat capacity |
| product-time | initial gradient = initial rate |

First question: area, gradient, intercept or trend?

---

### 4.3 Energy, work, power and efficiency

Energy audit:

`input energy = useful energy + wasted energy`

Useful formulae:
- work = force × distance in force direction
- gravitational energy = mgh
- kinetic energy = 1/2 mv²
- spring energy = 1/2 kx²
- power = energy/time
- efficiency = useful/input
- heating = mcΔT
- latent heat = mL

ENGAA/PAT lesson:
Conservation or energy audit is often faster than force-by-force calculation.

---

### 4.4 Mechanics and forces

Process:
1. Draw free-body diagram.
2. Choose axis.
3. Use resultant force.
4. Apply `F = ma`.
5. Use energy/momentum if faster.

Common rules:
- constant speed means resultant force is zero
- Newton's third-law pairs act on different bodies
- friction opposes relative motion or tendency to move
- for moments, choose pivot to remove unknowns
- for pulleys, count supporting rope segments

---

### 4.5 Momentum and impulse

Use for:
- collisions
- explosions
- stopping force
- contact force
- rockets/ejected mass

Rules:
- choose positive direction
- momentum before = momentum after if no external impulse
- impulse = change in momentum
- average force = change in momentum / time
- kinetic energy is not conserved in sticky collisions

---

### 4.6 Circuits and electricity

Circuit order:
1. Reduce series/parallel structure.
2. Identify fixed voltage or fixed current.
3. Find total current.
4. Find local voltage/power.

Formula choice:
- P = IV
- P = I²R
- P = V²/R
- Q = It
- E = VQ
- transformer: V ratio = turns ratio
- ideal transformer: input power = output power

Common trap:
At fixed supply voltage, lowering total resistance increases total current and total power.

---

### 4.7 Waves, sound and optics

Waves:
- v = fλ
- frequency usually stays fixed across a boundary
- one particle oscillation distance = 4 × amplitude
- wave speed is not particle speed
- echo/ultrasound path is there and back
- phase difference depends on path difference / wavelength

Optics:
- draw normal
- use Snell's law
- total internal reflection requires going from higher n to lower n
- check limiting cases: θ = 0, critical angle, grazing incidence

PAT lesson:
Ray diagrams usually simplify optics before formulae.

---

### 4.8 Nuclear and half-life

A/Z ledger:

| Process | Mass number A | Proton number Z |
|---|---:|---:|
| alpha | -4 | -2 |
| beta minus | 0 | +1 |
| neutron emission | -1 | 0 |
| gamma | 0 | 0 |

Half-life:
- subtract background before halving
- for daughter growth, use final plateau to infer original parent amount
- compare ratios after integer numbers of half-lives

---

### 4.9 Thermal physics and gases

Thermal:
- conduction rate ∝ area × temperature difference / length
- in layered conduction, poorer conductor has steeper temperature gradient
- shiny surfaces are poor absorbers and poor emitters
- vacuum stops conduction and convection, not radiation

Gases:
- at constant temperature, pV = constant
- pressure and density scale together if temperature is fixed
- depth pressure is not always linear with volume; use pressure ratios

---

## 5. Source-specific additions

### From NSAA

Added:
- table-first approach
- statement-by-statement truth testing
- graph meaning before formulae
- A/Z nuclear ledger
- circuit current first
- half-life background correction

### From ENGAA

Added:
- mixed-topic reset after every question
- Advanced Part B relevance filter
- stronger use of proportionality and units
- moments/pivots and pulley tension rules
- mechanics extension: work, friction, collisions, spacecraft momentum

### From TMUA

Added:
- substitution before expansion
- discriminant for intersections
- solution counting by graph
- coefficient targeting
- transformation by key point
- trig interval discipline
- special-value elimination

### From PAT

Added:
- dimensional analysis as a core technique
- marks-time discipline for longer questions
- conservation-first approach
- ray diagrams for optics
- pulley segment counting
- physical modelling and limiting-case checks

---

## 6. Error-log tags

Use in `error_log.md`:

- no 20-second route test
- substitution missed
- special value missed
- units missed
- dimensional analysis missed
- graph meaning missed
- discriminant missed
- table missed
- complement missed
- scaling missed
- circuit reduction missed
- circuit constraint missed
- A/Z ledger missed
- half-life background missed
- FBD missed
- moment pivot missed
- pulley segment count missed
- energy audit missed
- conservation law missed
- wave-particle confusion
- ray diagram missed
- trig interval missed
- coefficient targeting missed
- domain/range missed
- over-solving
- advanced question over-attempted

---

## 7. Final exam reflex

Before deriving, ask:

1. Can I eliminate by units?
2. Can I substitute a simple value?
3. Can I use proportionality or scaling?
4. Can I use graph area/gradient?
5. Can I use a table?
6. Can I use a limiting case?
7. Can I use an option as a shortcut?

Only derive when these fail or when the derivation is clearly short.
