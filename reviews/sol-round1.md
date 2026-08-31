## Adversarial review: prioritised findings

I re-ran `greedy.py`, `indep.py`, and `friendly.py`, recomputed collision math, and built additional checks for Block M/N conditioning, cross-block MI, and prefix ordering.

---

### Severity 1 — Headline bit budget is overstated (~2–4 bits)

**Blocks M and N (Q60–69) are credited ~1.3–2.3 bits more than they deliver after Block B.**

The document budgets Block M at **4.60 bits** and Block N at **4.40 bits** (§5 budget table; §4b claims both are **MEASURED** against ceilings of 4.77 / 4.97).

Recomputed with a realistic maternal-age distribution (H(age) ≈ 4.84 bits):

| Metric | Mother (M) | Father (N) |
|--------|------------|------------|
| H(parent year \| Block B) | 5.53 | 5.71 |
| H(parent year \| Block B + block questions) | 2.24 | 2.30 |
| **Actual incremental bits** | **3.29** | **3.41** |
| **Budgeted** | **4.60** | **4.40** |

Q63/Q68 (“tens digit odd”) add only **~0.014–0.032 bits** given the other year questions — essentially dead weight, not listed in the dependency register.

**Impact:** True total is closer to **~65.8 bits** than **68.11**. At 65.8 bits expected non-unique people ≈ **1.0** (still under 1). At **~64.5 bits** (if estimated blocks E–L are also optimistic), expected non-unique people rises to **~10–100**. The “0.2 people colliding at 76 questions” figure is fragile.

---

### Severity 2 — Q33 checkpoint contradicts its own collision formula

After Q33 the document claims **~32.2 effective bits** and **“about 4.6 billion people still share a pattern”** (Block F closing text).

Using the document’s own formula `N(1 − e^(−(N−1)/M))` with N = 8×10⁹:

- **32.2 bits → ~6.4 billion** non-unique (not 4.6B)
- **4.6 billion** non-unique requires **~33.1 bits**

The narrative checkpoint mixes bit sum (~32.2) with a collision count that matches ~33.1 bits. One of those numbers is wrong.

---

### Severity 3 — “Prefix-optimality” is overstated

§3 claims **every prefix** is the best identifier of that length.

Counterexamples found:

1. **Q2 “born 1995 or later”** has marginal H = **0.996 bits**; **“Jan–Mar or Jul–Sep”** has **1.000 bits**. Q2 is placed first in Block B for human readability (“doubles as age question”), not entropy — §3 admits truncation matters but still claims prefix-optimality.

2. **Block ordering** is source-grouped, not globally greedy. Blocks H/I (~0.97 bits/question) sit after E/F/G (~0.90–0.95) largely because of lookup cost, not bit rate.

3. Within Block B, document order totals **11.755 bits**; greedy order on the same predicates reaches the same ceiling — but **Q2’s listed gain of 1.00** is rounded; actual first-step gain for “born 1995+” is **0.996**.

**Verdict:** Prefix-optimality holds approximately within Block B’s greedy construction, not globally across the full 76-question list.

---

### Severity 4 — Effective-bits accounting is not joint entropy

The budget sums per-block estimates with hand percentage discounts (E −5%, F −7%, G −10%, etc.). That is **not** H(all answers) and can overstate when:

- Discounts are wrong (document admits ±2 bits on core; §8)
- Cross-block correlations are omitted (parent names ↔ child names: register item 12, **not measured**)
- “Don’t know → no” fallbacks correlate non-answers (H, I, G, J, L, Q)

Estimated blocks E–L carry **~3.9 bits** of discounts vs raw ~1-bit-per-question marginals. If discounts should be larger, core list loses several bits before M/N issues.

**Where overstatement is largest:** M/N (proven above), then E/F/G (unmeasured cultural correlation), then Block Q (below).

---

### Severity 5 — Missing / understated dependencies

**Not in the register (13 listed), but provable or strongly indicated:**

| Relationship | Evidence |
|--------------|----------|
| **Q56 partially redundant with Q55** | Rough sibling model: MI(Q55, Q56) ≈ **0.21 bits**. Only-child + Q54=no + Q55=no forces Q56=no. Register notes Q54/Q55 overlap but not Q55/Q56. |
| **Q63/Q68 near-zero given other year questions** | Gain **0.014–0.032 bits** after Block B + other year parities. |
| **Block M Q62 digit-sum vs Q60 year-even** | Within-decade MI ≈ **0.98 bits** (same conditional structure as Block B Q9/Q6; register item 8). Safe in Block B because decade is unresolved; in Block M decade is also partially unresolved, so overlap is real but unquantified in budget. |
| **Block O+P ↔ Block C/D short-name “no” correlation** | Names &lt;5 letters: **49.5%** have both Q16(3rd letter) and Q70(5th letter) = no. Document notes short-name penalty on O+P but not correlation with C. |
| **Q75 determined by Q74** | “If so, delivered first?” — non-multiples forced to no. Joint H(Q74,Q75) ≈ **0.16 bits** vs marginal sum **0.22**. Acknowledged in prose but not in register. |

**Blocks M/N vs H/I:** Mother/father **day+month vs birth year** are independent by construction. **No meaningful MI** between sibling structure and mother-year parity (≈0.0000 in my model). Block K does **not** materially interact with H/I; the M/N issue is vs **Block B**, not H/I.

---

### Severity 6 — Block Q budget overstated

Claimed **1.50 bits** for Q74–76. Recomputed:

- Marginal sum (if independent): **1.21 bits**
- Joint (rough, with Q75⊥Q74 and 40% unknown→no on Q76): **~1.15 bits**

Not catastrophic alone, but combined with M/N it matters near the collision threshold.

---

### Severity 7 — Universality failures and silent correlation

| Question | Problem |
|----------|---------|
| **G (Q34–37)** | ~20% cannot answer mother’s birth surname → all **no**, correlated across four questions. Discount (−10%) may be insufficient. |
| **H/I (Q38–49)** | “Don’t know → all six no” creates a **6-bit correlated block** of losses. Correctly warned not to substitute Block B; still a universality hole. |
| **J (Q50–53)** | Fallback chain; unhoused → four correlated nos. Weak block (~3.0 bits estimated). |
| **L Q58** | ~40% unknown birth time → no. Effective H ≈ **0.88 bits**, not ~1.0. |
| **Q Q76** | Unknown birth weight → no. Skews the 45% split and correlates non-answers. |
| **C/D “shorter name: no”** | Mechanical coupling across letter-position questions; independence holds for dictionary proxy but **non-answers cluster**. |

---

### Severity 8 — Birthday-problem framing: mostly sound, one metric slip

**Sound:**

- log₂(N) = **32.9** for addressing; log₂(N²/2) = **64.8** for expected pairs &lt; 1 — **verified**.
- Table in §1 (33→65 bits): **people-not-unique** column matches `N(1−e^(−(N−1)/M))` to ~1%.
- Dropping H+I: **42.76 bits → 8.59×10⁶** non-unique (claimed 8.6M) ✓
- Dropping M+N from full list: **59.11 bits → 103** non-unique (claimed ~103) ✓

**Slip:** §1 derives threshold from **expected colliding pairs** N²/(2M), but §4b/§5 “people still colliding” uses **people-not-unique** (roughly **2× pairs** at these bit levels). Not wrong, but the metric switches without labelling. At 68.11 bits: pairs **0.10**, people-not-unique **0.20**.

---

### Severity 9 — Split estimates likely off (material cases)

| Claim | Issue |
|-------|-------|
| **Block K ~2.00 bits** | Marginal H from stated splits ≈ **2.99 bits**; document’s 2.00 implies ~1 bit overlap. MI(Q55,Q56) ≈ 0.21 not fully accounted. |
| **Block J ~3.00 bits** | Four ~50% marginals on the **same address** — true joint likely **&lt;3** unless house number, postal code, and street are modeled as independent (they aren’t). |
| **Block L ~2.00 bits** | Q58 alone ≈ **0.88 bits** after unknown→no; block may be **~2.0** only if Q57/Q59 are ~1 each — plausible but unmeasured. |
| **C/D “MEASURED”** | Independence verified on **English dictionary words**, not name-frequency data (§8 admits). Structural A-M independence likely holds; **splits ~51%** may not. |
| **Q2 “born 2001 adds 0.188 bits after 1995”** | Recomputed gain ≈ **0.36 bits** — directionally right (don’t add more year thresholds), number wrong. |

---

### Severity 10 — Section 9 (twins) is sound; one nuance

Anna/Anne identical on all six given-name questions: **verified** mechanically.

57 of 76 questions identical for monozygotic twins: **correct by construction**.

**Nuance:** §9 says Block C is the only way Anna/Anne diverge — true for those names, but **Block O+P (Q70–71)** is another letter-resolution path the prose underplays (though useless for Anna/Anne).

Impossibility claim for inherited facts: **sound**. Block Q + height are correctly framed as within-pair distinguishers, not general-population bit sources.

---

### What is actually sound (brief)

- Core birthday-problem reframing (33 vs ~65 bits): **correct**.
- Block B date entropy (**H ≈ 14.76**, best 12 questions ≈ **11.76 bits**): **reproduced**.
- Dependency register items 1, 2, 5, 8, 9, 10, 11: **confirmed** by `indep.py`.
- A-M letter independence (dictionary proxy): **confirmed** at stated MI values.
- Blocks H/I as high-value, independent of own birth date: **confirmed** (H(day+month) ceiling ≈ 8.51; six questions ≈ 5.92).
- Parents’ birth years are **not** redundant with child age alone: H(age) ≈ 4.8 bits — **confirmed**.
- Core list collision at 54.41 bits → **~2,674** non-unique: **confirmed**.

---

### What I did NOT check

- Real multi-cultural **name-frequency corpora** (E, F, G correlations).
- **Residence** (Block J) with real address/postal distributions.
- **Height** (Q57) by country/sex.
- **Global sibling-structure** demographics beyond rough models.
- **Adaptive** questioning (document correctly scopes to fixed questionnaires).
- Whether a **different** question set could extract more of H(mother year \| Block B) than the chosen five parities.
- **Population count** sensitivity (7.9B vs 8.1B — minor).
- **Living cohort** born before 1926 (edge case, negligible).

---

### Bottom line

The central thesis — **~33 bits addresses people but ~65 bits are needed for random-like patterns under the birthday problem** — survives. The delivered **68.11-bit** total and **“0.2 people colliding”** headline do not: **Blocks M/N are over-credited by ~2.3 bits**, estimated blocks may cost another **1–2 bits**, and the **Q33 checkpoint mixes incompatible numbers**. Corrected total **~64–66 effective bits** still approaches uniqueness for the median case but is **not** as comfortably below the threshold as claimed; identical-twin impossibility remains the harder honest limit.
