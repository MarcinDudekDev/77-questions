# Adversarial review: `QUESTIONS.md`

Prioritised findings only. I re-ran `greedy.py`, `friendly.py`, and `indep.py`, and wrote additional Python checks for collision math, Block B/M/N entropy, prefix ordering, and assorted dependencies.

---

## Critical (headline or central logic wrong)

### 1. “76 questions → uniqueness” confuses **expected** collisions with **guaranteed** uniqueness

Section 5 claims **0.2 people still colliding** at 68.11 bits. That is **E[non-unique people]** under a random-assignment model, not “every human has a distinct pattern.”

Recomputed:

| Bits | E[non-unique people] | P(zero collisions) |
|-----:|---------------------:|-------------------:|
| 65.0 | 1.74 | 0.42 |
| 65.8 | ~1.0 | ~0.50 |
| 68.11 | 0.20 | **0.904** |

So even at the claimed budget, **~10% of assignment draws still have at least one collision**. The document never states P(all unique). Under its own model, the title claim is overstated.

### 2. The ~65-bit target mixes two different birthday metrics

Section 1 derives **64.8 bits** from **expected colliding pairs** = N²/(2M) = 1.

The table in section 1 uses **people not unique** = N(1 − e^{−(N−1)/M}).

Those are not the same target:

- **E[pairs] = 1** → b = log₂(N²/2) = **64.795** ✓ (I reproduced 64.795)
- **E[non-unique] = 1** → b ≈ **65.795**

The table values themselves check out (e.g. 33 bits → 4.848×10⁹ non-unique; 54.41 → 2,674; 68.11 → 0.20). The error is presenting 64.8 as “the answer” while the stopping table is built on the stricter people metric.

### 3. Block M is **over-budgeted by ~1.3 bits**; Q63 is a dead question

Section 4b credits Block M with **4.60 bits** from five mother-year parities after Block B.

Measured on the documented Block B + maternal-age model (child year − age, UN-ish age weights):

- **H(Block B) = 11.754** (doc 11.76 — matches)
- **Incremental gain from Block M’s five questions after full Block B = 3.258 bits**, not 4.60

Per-question gains after Block B:

| Q | Predicate | Gain |
|---|-----------|-----:|
| 60 | year even | 1.000 |
| 61 | last digit 0–4 | 0.971 |
| 62 | digit sum odd | 0.996 |
| **63** | **tens digit odd** | **0.000** |
| 64 | born 1970+ | 0.290 |

**Q63 is deterministic given Q60–Q62** in this setup — a dependency not in the register.

The text’s ceiling argument uses **H(maternal age) = 4.77 bits given exact child birth year** (I got 4.795). That is correct *conditional on exact year*. But the **listed questions only extract 3.26 bits after Block B**. The block is booked at 4.60.

Block N is likely inflated similarly (same five predicates, assortative mating makes father-year bits overlap mother-year bits; MI on “born 1970+” alone ≈ **0.73 bits** under a simple assortative model).

**Net: ~2–3 bits of inflation in M+N**, before counting other blocks.

At **~65.5 bits** instead of 68.11: **E[colliders] ≈ 1.2**, not 0.2. The “0.2 people” headline is fragile.

---

## High (material overcount or false structural claim)

### 4. Effective-bits accounting is not defensible as joint entropy

The budget table sums block totals with hand percentage discounts (−5%, −7%, −10%, “small discount”). That is not joint entropy and not measured except for A, B, C, D, H.

Problems:

- **No cross-block covariance** (M↔N, C↔E/F, B↔M via year−age, K↔M via birth order).
- **Measured blocks are summed with estimated ones** as if independent.
- Section 8 admits **±2 bits** on the core 54.41 alone. At 54.41 bits, collisions swing by ~4× per bit (54.41 → 2,674; 52.41 → 10,695; 56.41 → 668 — all recomputed).

The document is honest that E–L are estimated; it is **not** honest to treat **68.11** as a measured quantity. It is a discounted sum of mixed measured/estimated parts.

### 5. “Prefix-optimality” is false for the list as written

Section 3: *“every prefix of the list is itself the best identifier of that length.”*

Counterexample: move Blocks H+I before E+F+G (same source-grouping spirit, higher bits/question). Using the document’s own per-block bit allocations:

| Stop at Q# | Current order | H,I before E,F,G | Δ |
|----------:|--------------:|-----------------:|--:|
| 37 | 35.76 | 36.31 | +0.55 |
| 38 | 36.74 | 37.26 | +0.52 |
| 45 | 43.54 | 43.81 | +0.27 |

Within Block B, greedy may hold; **globally it does not**. The real ordering principle is “group by source, then mostly descending bits” — not prefix optimality.

### 6. Name blocks C/D are “MEASURED” but not reproducible from the repo

README says every MEASURED number came from the scripts. **`greedy.py` / `indep.py` / `friendly.py` do not touch names.**

I reproduced the claimed MI figures using `/usr/share/dict/words` (235,974 English dictionary words):

- MI(1st, 2nd letter A–M) = **0.0045** (exact match)
- 6-question joint entropy = **5.978 bits** (doc 5.95)

So the numbers are internally consistent — **for dictionary words, not human names**. Section 8 discloses the proxy; the budget table tagging C/D as **MEASURED** overstates confidence. Real names (frequency, culture, length, Anna/Anne pairs) will differ, and the twin section already shows near-duplicate given names can collapse entire blocks.

### 7. Undetected / under-registered dependencies (beyond the 13 listed)

| Relationship | Evidence |
|--------------|----------|
| **Q63 ⊥ Q60–62** | +0.000 bits after Block B (above) |
| **Q75 ⊥ Q74** | “If so, delivered first?” — non-multiples must answer no; Q75 is a deterministic function of Q74 for ~98% of people. H(Q75) ≈ 0.081 bits total, not “0.08 bits for the 2% it applies to” cleanly separated |
| **Q54, Q55, Q56 for only children** | Only child → Q54=no, Q55=no, Q56=no always. Register mentions 54↔55 overlap, not the **three-way** only-child lock |
| **Short-name “answer no” rule (Q16–17, Q70–73)** | Forces correlated zeros across letter-position questions; not in register |
| **Block G “don’t know → no”** | ~20% get four correlated nos; discount −10% is a guess |
| **M↔N year blocks** | MI ≈ 0.73 bits on Q64/Q69 alone under assortative mating; N’s “small discount” vs M is insufficient |
| **K↔M (maternal age)** | Q54 (“older sibling”) shifts maternal-age-at-your-birth distribution. Effect modest in my model (~0.08 bits), but **not listed** while M/N are singled out as “least scrutinised” |

H↔I and M↔H (year vs day/month): **no material redundancy found** (mother year vs day/month overlap ≈ 0; MI(Q6 child year even, Q60 mother year even) ≈ 5×10⁻⁵).

---

## Medium (estimates likely off or universality leaks bits)

### 8. Block K: “3 questions, ~2.00 bits” ignores Q56

Q54+Q55 joint entropy ≈ **1.95 bits** in a simple 4-state sibling model — already accounts for only-child constraint on those two. **Q56** (“even number of maternal children”) is largely predictable from Q54+Q55 (+ only-child case). Booking a full third bit is generous.

### 9. Block J (~3.00 bits) is the weakest claim in the core list

Four ~50% splits are asserted with no script and heavy universality problems:

- No house/building number (rural, nomadic, unhoused)
- Postal-code parity varies by country format
- Street-name A–M depends on romanization

Fallback “answer no to all four” creates a **correlated non-answer stratum** — same failure mode as Block G, but without a discount.

### 10. Q1 split is not what the question asks

Q1: “Do you identify as male?” with **50.4%** yes — that is **sex ratio at birth**, not gender identity. Identity splits are not 50/50 globally and are culturally loaded. Minor in bits, but a universality/correlation footgun (cf. Fable’s sex↔vowel-final-name coupling — not in this register).

### 11. Block B is “greedy” but Q2 is hand-placed and absent from `greedy.py`

`greedy.py`’s first pick is **“year mod 4 is 0 or 1”**, not “born 1995 or later.” `friendly.py` prefers **“born 2001 or later.”** The documented Block B (with 1995+) yields **11.755 bits** — fine numerically, but the “not taste, greedy maximisation” claim is overstated for Q2 and ordering.

### 12. Fallback rules silently create duplicate questions for non-answerers

Register #13 covers H/I/J borrowing Block B. Also:

- **H/I unknown → six nos** (four-bit loss, fully correlated)
- **G unknown → four nos**
- **J none applies → four nos**
- **Q58, Q76 unknown → no** (same bit as “born afternoon” / “light birth weight”)

These are handled as “accept the loss,” but they **re-concentrate** non-answerers in the same pattern region — the collision math assumes well-spread pseudo-random answers and **overstates effective bits** for the worst-served populations.

---

## Lower (real issues, smaller bite)

### 13. Section 9 twin arithmetic is fine; the impossibility argument is sound

0.4% × 8×10⁹ ≈ 32×10⁶ people; Anna/Anne mechanical check is convincing. Block Q’s low average bits but high conditional value is correctly argued.

### 14. Blocks H/I day+month entropy checks out

Six uniform calendar predicates → **5.908 bits** (doc 5.85). Independence from own birth date is structurally right.

### 15. Block B and date dependency register are solid

- H(birth date) ceiling = **14.757** (doc 14.76)
- Documented 12-question Block B = **11.755 bits**
- Dependency #1, #5, #8 claims match `indep.py`
- Weekday questions’ conditional contribution after partial date pinning is legitimate **if** measured jointly (claimed, plausible)

### 16. Q33 = 32.2 bits checkpoint is arithmetically fine

1.00 + 11.76 + 5.95 + 5.95 + 3.80 + 3.70 = **32.16** (doc ~32.2). The narrative point (“still ~4.6B colliding”) follows from the birthday table.

---

## What is actually sound (briefly)

- **Birthday-problem reframing** vs log₂(N) serial addressing: correct and important.
- **Collision table arithmetic** (given the chosen formula): reproduced within rounding.
- **Date-block measurement methodology** (`greedy.py` / `indep.py`): credible.
- **Parent day+month as high-value, independent of own DOB**: correct.
- **Identical-twin impossibility**: correct for inherited-fact questionnaires.

---

## Missing entirely

1. **P(all unique)** — only expectations reported.
2. **Joint entropy across all 76 questions** — never computed; budget is a spreadsheet sum.
3. **Adoption / step-parents / donor conception** — mother’s birth surname, father’s name, maternal-child surname line all break.
4. **Non-Latin scripts** — letter-position questions become romanization-dependent; can collapse or correlate across blocks.
5. **Designed identifiers** (national ID, phone, biometrics) — mentioned only in §9 as the real twin fix, not costed against the questionnaire approach.
6. **Reproducible name measurement script** — absent from the repo despite MEASURED labels.

---

## What I did **not** check

- Real multi-cultural name-frequency corpora (no data on machine).
- Empirical global distributions for address, height-by-country median, multiple-birth rates, or birth-weight splits.
- Full joint simulation of all 76 questions together.
- Optimal reordering search over all block permutations (only tested one obvious counterexample).
- Whether a better mother-year question set could reach the 4.77-bit ceiling after Block B (ceiling may be achievable; **this list does not**).

---

## Severity-ranked summary

| Rank | Finding |
|-----:|---------|
| 1 | “Uniqueness” = E[colliders]≈0.2, not guaranteed uniqueness; P(unique)≈90% at 68.11 bits |
| 2 | Block M overcount ~1.3 bits; Q63 adds 0 bits — dead question |
| 3 | M+N likely ~2–3 bits over budgeted; 68.11 → ~65.5 effective → E[colliders]≈1+ |
| 4 | 64.8-bit “target” uses pairs metric; people metric needs ~65.8 |
| 5 | Effective-bits sum with % discounts is not joint entropy; ±2+ bits uncertainty |
| 6 | Prefix-optimality claim is false (proved at Q37–45) |
| 7 | Name independence “MEASURED” on dictionary words only; no repo script |
| 8 | Several unregistered dependencies (Q63, Q74→75, only-child triple, short-name zeros, M↔N) |
| 9 | Block J estimates and fallback correlation; Block K third question oversold |
| 10 | Q1 conflates identity with birth sex; Block B “greedy” oversell on Q2 |

**Bottom line:** The reframing from 33 to ~65+ bits is right. The collision arithmetic is mostly careful. The **68.1-bit headline and “0.2 people colliding” conclusion are not safe** once M/N overcount, dead Q63, non-joint budgeting, and fallback correlation are accounted for — and even at face value, **uniqueness is only expected, not assured**.The **H(mother year | Block B)** run finished successfully. Main numbers:

- **H(Block B)** = 11.754 (matches the doc’s 11.76)
- **H(mother year | child birth year exact)** = 4.795 (matches the doc’s 4.77 maternal-age ceiling)
- **H(mother year | Block B)** = **5.50 bits** — more residual uncertainty than the 4.77 ceiling, because Block B only partially pins the child’s year

The problem is on the **question side**, not the ceiling argument: the five Block M predicates only add **3.26 bits** on top of full Block B, not the budgeted 4.60. **Q63 (tens digit)** contributes **0.000 bits** after Q60–Q62 — it’s redundant.

Net: Block M is **~1.3 bits over-budgeted**; M+N together likely inflate the total by **~2.7 bits**, which pushes expected colliders from **0.2** toward **~1+** at the true effective bit count. That’s the main follow-on from this run; it’s already reflected in the review above.The **“Verify parent year dependencies, budget sums, prefix optimality”** run was **killed (exit 137)** — almost certainly OOM. The script nested over every birth date, maternal age, and mother day/month combination, which blew up memory before it could finish cleanly.

The important parts were already recovered with lighter reruns:

- **Budget sums** check out (core 54.41, full 68.11; Q33 checkpoint ≈ 32.16 bits)
- **Prefix-optimality** fails around Q37–45 (moving H+I before E+F+G gains ~0.5 bits)
- **Parent-year dependencies** were handled by the later `H(mother year | Block B)` run: Block M adds **3.26 bits** after Block B, not 4.60; Q63 is redundant

Nothing blocking remains from that failed job.
EXIT=0
