# Adversarial review: QUESTIONS.md (76-question human-uniqueness list)

Reviewer: Fable (fresh context). Every numeric claim below was recomputed with python3;
"PROVEN" means I have an exact derivation or an exhaustive/enumerated computation,
"MEASURED" means a simulation or proxy-corpus computation with stated assumptions,
"SUSPECTED" means a reasoned argument I could not fully quantify with data on this machine.

Verdict up front: the framework (birthday problem, ~65-bit target) is right and the
arithmetic in sections 1 and 5 is internally correct, but **Blocks M and N contain a
proven zero-bit question each and a mostly-redundant threshold question each**, Block Q's
total is impossible, and the effective-bits accounting overstates the joint total by
roughly 3 bits — enough to push the headline "expected collisions 0.2, below one" back
above one **by the document's own methodology**. Structural effects (cultural clustering,
correlated fallbacks) push the true collision count orders of magnitude higher still.

---

## Finding 1 (SEVERE, PROVEN): Q62 and Q67 carry exactly zero bits

For every year 1900-2099, **digit-sum parity is an exact function of (year parity,
tens-digit parity)**. Sum of digits of `19XY` = 10 + X + Y and of `20XY` = 2 + X + Y; both
century prefixes are even, so digit-sum parity = parity(X) XOR parity(Y). I brute-forced
all years 1800-2099: **0 exceptions per century, and the 1900s and 2000s mappings are
identical**, so the dependency holds across the whole plausible parent-birth-year range
(a parent born before 1900 requires a respondent born ~1926 with a 49-year-old mother —
negligible mass).

- Block M asks Q60 (year even) + Q63 (tens digit odd) + Q62 (digit sum odd). Q62 ≡
  Q60 XOR Q63 (up to a fixed sign). **Zero information.**
- Block N asks the same triple as Q65 + Q68 + Q67. Same result. **Zero information.**

The bitter part: **the document's own scripts already knew this.** `greedy.py` reports
"year's tens digit is odd: +0.0000 bits" once parity and digit-sum are chosen, and
`friendly.py` prints `dropped (+0.0000): Is the tens digit of your birth year odd`. Block B
correctly asks only two of the three. Blocks M and N were hand-written without rerunning
the machinery, and both include the full XOR triple. This is precisely the "conditional"
dependency the doc celebrates catching in register #8 and in the "Correction to an earlier
claim" — caught for Block B, then reintroduced twice in the blocks added last.

Note the doc's register #8 says "safe to ask both" about parity + digit-sum, which is true
**only if you don't also ask the tens digit**. M and N do.

## Finding 2 (SEVERE, MEASURED): Blocks M+N deliver ~6.5 bits, not the 9.00 credited

Beyond Finding 1, Q64 ("mother born 1970 or later") is heavily redundant with Q2 ("you
born 1995 or later"), and Q69 with both. I enumerated (your year ~ the scripts' age
distribution) x (maternal age at birth, discrete Gaussian calibrated so H = 4.78, matching
the doc's claimed 4.77) x (parental age gap, calibrated H = 4.70, generous):

- MI(Q2, Q64) = **0.62 bits**; MI(Q64, Q69) = **0.65 bits**.
- Q64 adds only **~0.30 bits** given Block B's year questions and M's other questions
  (its ~0.99-bit marginal is mostly already known).
- Joint result: **Block M adds 3.27 bits given Block B (credited 4.60); Block N adds 3.22
  given B and M (credited 4.40). Total 6.50 vs 9.00 — overstated by ~2.5 bits.**
  With narrower (more realistic) distributions the overstatement grows to ~2.8.

The doc's own warning in Block M — "do not also ask age-gap questions ... those are the
same information restated" — describes exactly what Q64 does through the back door: given
your birth year, "mother born >= 1970" IS an age-at-birth threshold question.

The stated ceiling logic is also subtly wrong in direction: H(maternal age) = 4.77 is the
conditional entropy given your **exact** birth year, but Block B does not pin the year
exactly, so 4.77 is not a hard cap on the fresh information; the real problem is the five
questions extract far less than either number, per above.

## Finding 3 (SEVERE, PROVEN): the headline "collisions below one" fails on its own terms

Block Q's claimed 1.50 bits is impossible. Q75 is deterministically "no" whenever Q74 is
"no" (98% of people), so H(Q74, Q75) <= H(0.02) + 0.02·1 = 0.161, and with Q76 at
h(0.45) = 0.993 the block's joint entropy is **at most 1.154 bits** (even the sum of the
three stated marginal entropies is only 1.215). Overstated by >= 0.35 bits.

Correcting only the proven/measured overstatements: 68.11 − 2.5 (M+N) − 0.35 (Q) ≈
**65.3 bits → expected colliding people ≈ 1.5-1.7, not 0.2.** The full list no longer
clears the "expected collisions below one" finish line that is its central deliverable.
(The comparative claim "dropping M and N takes 0.2 to 103" also shrinks: from ~1.5 to
~60-70.)

## Finding 4 (SEVERE, STRUCTURAL, partly MEASURED): the accounting itself — Shannon sums
## + hand discounts + a uniform-bucket birthday formula — systematically understates collisions

Three distinct errors compound here:

1. **Wrong entropy.** The expected-colliding-pairs formula N²/2M with M = 2^b is exact
   only for a uniform distribution over patterns. For a non-uniform distribution the
   correct exponent is the **collision (Rényi-2) entropy** of the joint distribution,
   which is always <= the Shannon entropy being summed. For the stated 76 marginal splits
   treated as independent the gap is small (73.97 vs 73.59 bits — I computed both), but
   correlations reduce H2 faster than H1, so every unmodelled dependency hits the
   collision count harder than the Shannon accounting suggests. The 0.2 figure is a lower
   bound on a quantity the method cannot upper-bound.

2. **Cultural clustering.** Collisions concentrate in the largest homogeneous
   subpopulations, and per-block bits are global averages. Concrete computation: using
   published approximate frequencies of the top 30 Chinese surnames in pinyin (62.9%
   coverage, remainder generously spread uniformly over all 64 patterns), the six Block D
   questions have **Shannon 5.03 and collision entropy 4.25 bits within China** vs the
   5.95 credited — the top 30 surnames land on only 17 of 64 patterns, and two random
   Chinese share a Block D pattern with probability 0.0525 vs the 0.0162 the doc's number
   implies. That is a 1.7-bit within-China deficit from one block; India (given-name and
   surname concentration), Vietnam (Nguyen ~40%), and Korea (Kim+Lee+Park ~45%) are worse.
   The doc's honest-limits section admits the dictionary-word proxy but treats it as a
   splits issue; it is a collision-structure issue.

3. **Correlated fallbacks across blocks.** Each "if unknown, answer no" rule is discounted
   inside its own block, but unknown-ness is one shared latent variable (do you know your
   biological parents / do you have documents). A person who cannot answer E, F, G, H, I,
   M, N (closed adoption, foundling, donor-conceived, orphaned young) gives a deterministic
   all-no on ~28 questions and loses ~32 bits as a **cluster**, not as independent per-block
   shavings. Even at 0.1% of humanity (8M people, surely an underestimate — the doc itself
   says ~20% cannot answer Block G alone), 8e6 people with ~35 effective bits yields
   **~1,900 expected colliding people in that cluster alone**; at 1% it is ~10^5. No
   per-block percentage discount can represent this. SUSPECTED in magnitude, PROVEN in
   direction.

So: summing per-block effective bits after hand discounts is defensible as a rough Shannon
budget, but plugging that sum into the uniform birthday formula and reporting "0.2 people"
to one decimal place is not. The number is presented with a precision the method cannot
support, and every unmodelled effect pushes it the same way — up.

## Finding 5 (MODERATE, PROVEN): "prefix-optimality" is false as written, by the doc's own numbers

Section 3 claims "every prefix of the list is itself the best identifier of that length"
and that "blocks are ordered by bits-per-question descending". Neither holds:

- Bits/question by block (doc's own budget): C/D 0.992 > B 0.980; H 0.975 sits **after**
  E 0.950, F 0.925, G 0.900; M 0.920 and N 0.880 sit **after** J 0.750, K 0.667, L 0.667.
- Concretely: reordering only M and N before J, K, L gives a 59-question prefix worth
  **56.41 bits vs the published 54.41** (doc's own per-block numbers) — a 2.00-bit better
  prefix at the same length, i.e. ~4x fewer collisions for a questionnaire abandoned at 59.
- The stated defence ("M-Q cost universality or reliability") does not apply to M/N: a
  mother's birth **year** is more widely known than her exact day-and-month (Block H,
  placed 22 questions earlier).

Also, within Block B the doc claims "the order is the exact greedy selection order". It is
not: `friendly.py`'s greedy picks the quarter question first and "born 2001 or later"
(44.3% yes) eighth; the doc moved a rephrased age question ("1995 or later", 53.8%, gain
0.996 not 1.00) to position 1. The block's 12 questions do jointly reach 11.755 bits
(verified — the 11.76 total is honest), but the per-position optimality claim is false.

## Finding 6 (MODERATE, PROVEN): the twin section's counts are internally inconsistent,
## and Block K actually distinguishes twins

- Section 9 lists blocks "A, B, D, E, F, G, H, I, J, K, M and N" as answered identically
  by twins. Those blocks contain **60** questions, not the claimed **57**. The intro's
  "47 of the first 59" corresponds to the same list **without K** (1+12+6+4+4+4+6+6+4 = 47).
  So the intro excludes K, section 9 includes it, and 57 = 60 − 3 matches neither text.
- On the merits the intro is right: **Q54/Q55 are answered differently by co-twins** if
  the co-twin counts as an "older/younger sibling by the same mother" — the second-delivered
  twin has an older sibling the first does not. Either the question distinguishes twins
  (contradicting section 9's list) or "sibling" silently excludes co-twins (an ambiguity
  the spelling-rule-style precision elsewhere would not tolerate).
- Consequence: an **unregistered dependency**. For twins with no elder non-twin siblings,
  Q75 ("delivered first") ≈ NOT Q54 ("has older sibling") — register #11 catches the
  firstborn/older-sibling negation in general but misses that Q75 re-asks it for exactly
  the subpopulation Block Q exists to serve.

## Finding 7 (MINOR-MODERATE, MEASURED): Blocks O+P — impossible splits, small unregistered MIs

- The stated yes-rates (Q70 58%, Q71 65%, Q72 57%, Q73 63%) are inconsistent with the
  doc's own claim that "roughly a third of given names have fewer than 6 letters": with
  A-M covering ~52% of 6th letters, Q71's yes-rate is bounded near 0.67·0.52 ≈ 35%, not
  65%. Under a realistic name-length distribution I get Q70 ≈ 43% yes, Q71 ≈ 24% yes. The
  printed numbers look like complements ("no" rates). The ~0.8-bit-per-question credit
  survives because binary entropy is symmetric — but it means these splits were written
  down, not computed, while sitting in a table whose neighbours say MEASURED.
- Unregistered dependencies, measured on the dictionary proxy reweighted to name-like
  lengths: MI(Q70, Q18) = 0.055 bits and MI(Q71, Q18) = 0.057 (for a 5-letter name the
  5th letter IS the last letter, so Q70 partially re-asks Q18); MI(Q70, Q71) = 0.024;
  MI(Q71, Q19) = 0.026. Total leak across O+P ~0.2 bits, roughly what the "short-name
  penalty" already gives away, so the 3.20 credit is about right — but the independence
  story ("identical structure, identical independence properties") is not, and none of
  these appear in the register. The doc's position-1-4 independence claims themselves
  I reproduced and confirm (MI < 0.005).

## Finding 8 (MINOR, PROVEN/MEASURED): small numeric errors and optimistic splits

- "Once question 2 is asked, 'born 2001 or later' adds only 0.188 bits": measured **0.202**
  given the full block, **0.364** given Q2 alone. Wrong under either reading.
- Q2's gain is 0.996, printed as 1.00; P(born >= 1995) = 53.84% ✓.
- Stopping table "A-G, 35.8 bits → 1.1e9 colliding": computes to **1.0e9**.
- "Real questions average 0.92 effective bits": 68.11/76 = **0.896** (0.92 is the core
  list only).
- Q58 ("born before noon, unknown: no", stated ~50%): the doc's own rejection table says
  ~40% of living people have no recorded birth time, so the operational split is nearer
  30/70 and the "no" answers correlate with age/region (hospital-birth prevalence) — the
  very "re-asks region" sin for which belief questions were rejected. Block L's 2.00
  credit absorbs some of this, but the 50% label is not honest.
- Q39/Q45 (parents' day-of-year parity) leak parents' year parity via leap years once the
  other day/month questions constrain the date: measured MI(all 6 H answers; mother's year
  even) = **0.0197 bits**. Immaterial, but the claim "her day and month are independent of
  everything about you" technically fails for day-of-**year** questions. Checked so you
  don't have to.

## What is sound (verified, briefly)

- The central reframe (log2(N²/2) = 64.79 vs log2 N = 32.90) and the birthday formulas
  are correct, and **every row of the section 1 and section 5 collision tables reproduces**
  to the stated precision (33→4.85e9, 65→1.73, 54.41→2674, 68.11→0.2009, 42.76→8.59e6,
  59.11→102.9).
- Block B: joint entropy of the doc's exact 12 questions = **11.755 bits** ✓; H(birth
  date) ceiling 14.757 ✓; "13th question worth 0.62" ✓ (0.614).
- Dependency register items 1-11 all reproduce from `indep.py`/`greedy.py` output
  (daymonth-sum = 0 bits, leap-year MI 0.304, day>month MI 0.262, vowels MI 0.278,
  (day+month) mod 3 = 0.015, digit-sum/parity unconditional independence).
- The Anna/Anne walkthrough is correct: all six Block C questions match (I checked each
  letter), and Sofia/Sonia differ on exactly one, Anna/Alma on exactly two, as claimed.
- Block K's interaction with Block M via maternal age at birth (older-sibling → older
  mother → earlier birth year) — the brief specifically asked; I simulated it and it is
  real but small: **MI(older-sibling; Block M answers | Block B) ≈ 0.035 bits**. Not a
  problem. Blocks H/I vs M/N interact only through the 0.02-bit leap-year channel above.
- Twin prevalence arithmetic (0.4% → 32M people, 16M pairs) ✓, and the section 9
  conclusion (uniqueness for twins is not a budget problem) stands regardless of the
  count errors in Finding 6.

## What I did NOT check

- The discount magnitudes for Blocks E, F, G (parent-name cultural correlation, -5/-7/-10%)
  — no multi-cultural name-frequency corpus on this machine; the doc flags this too.
- Block J's splits (house numbers, postal codes) and the size of the no-address population;
  Block L's height and birth-city splits; the sex split 50.4%; sibling splits (56/52/48).
- The world age distribution baked into the scripts (I reused it as given; the doc's claim
  that reweighting moves splits by fractions of a point is plausible but untested).
- Real name data anywhere: all name measurements (mine and the doc's) ride on the
  /usr/share/dict/words proxy plus my assumed name-length distribution; my Chinese-surname
  frequencies are approximate public figures from memory, marked as such.
- cursor.out, fable.out, and ORIGINAL-DRAFT.md were skimmed for provenance only; I did not
  re-verify their claims.
- Whether 8.0e9 is the right N for "every living human" in 2026 (~8.2e9 would shift every
  collision figure by ~5%, no conclusion changes).
