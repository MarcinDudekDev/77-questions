# Adversarial review of QUESTIONS.md

2026-08-30. Recomputed the collision table, re-ran greedy.py / indep.py / friendly.py,
measured the written Block B set, simulated parent years from GBD ASFRs, reproduced
the name numbers on /usr/share/dict/words.

The 64.8-bit birthday target is right. The 68.11 / 0.2 headline is not.

## Ranked findings

### F1 — The 0.2 colliding-people row cannot sit next to section 9
**Severity 1.** Section 1 formula and table are arithmetically correct
(log2(N²/2) = 64.795; every published row matches N(1-e^(-(N-1)/M))).
M = 2^{H_Shannon} is the right bucket count only for a near-uniform hash.
Section 9 then describes ~16 million identical-twin pairs who share most
answers by construction. That is a point mass. The 0.2 figure is the Poisson
answer under independence. Both cannot be operational claims about the same
list. People-not-unique < 1 also needs ~65.8 bits, not 64.8 (they optimised
pairs < 1 and published people).

### F2 — Blocks M+N are not 9.00 bits; Q62/Q67 are linearly dead
**Severity 1.** Tagged MEASURED 4.60 / 4.40. No script in this directory
measures those ten predicates. On 1900–2026, Q62 = NOT(Q60 XOR Q63) with
0 mismatches — the same GF(2) fact they recorded as dependency 8 and called
safe in Block B because Block B does not ask tens digit. Block M asks all
three. Extra info in Q62 given the rest of M and Block B: 0.007 bits.
Same triple in N (Q65, Q67, Q68).

Simulation (their AGE_BAND_SHARE × GBD 2017 ASFR, paternal = maternal + N(2.5, 4)):

| quantity | claimed | measured |
|---|---:|---:|
| H(M 5 preds) | 4.60 | 3.95 |
| H(M, N) | 9.00 | 6.81 |
| H(M, N \| Block B year preds) | 9.00 | **6.07** |
| MI(Q2, Q64) | not listed | **0.59** |

H(maternal age) itself is fine (I get 4.68–4.72 vs their 4.77).
I(Block H; Block M) = 0.023 bits, almost all from Q39 leaking leap year.
The late-add damage is M/N vs B and M/N internally, not vs H/I.
Correcting −2.93 bits turns 68.11 into 65.18 → 1.53 people colliding,
not 0.2, under their own formula.

### F3 — H/I measured under full knowledge, then unknown → all-no
**Severity 1.** The 5.85 is joint entropy of six calendar predicates
assuming everyone knows the day (I get 5.97; they shaved 0.12). The
fallback dumps every non-answer onto one pattern. Collision entropy of
H at 25% unknown drops from 5.85 to ~3.67. A 10% unknown rate on H+I
already produces 6.5 colliding people inside that group at the remaining
56.46 bits, which dominates the 0.2 headline. I do not have a global
"knows mother's birthday" rate; the table in the HTML report is a sweep
over u. Universality ranking is backwards: more people know mother's
year than mother's day-of-year parity.

### F4 — Name bits were measured on dictionary words
**Severity 2.** /usr/share/dict/words reproduces the published splits
and MIs to the printed digits (51.8%, MI 1st vs 2nd = 0.0045, etc.).
Mean dictionary length 9.57; P(L ≤ 4) = 2.9%. Given names are shorter
(P(L ≤ 4) ≈ 27% in a typical length mix), so Q18 duplicates Q14–Q17 for
those people. Block O yes-rates (~58%, ~65%) are incompatible with
shorter→no, which can only pull yes below 50%. Claimed 0.8 bits each
from "a third shorter than 6 letters" plus 65% yes would require
P(A-M | L ≥ 6) = 0.97. O+P overcount vs a length model: ~0.5 bits.
A-M independence on dictionary words is real; the MEASURED tag on
names is not.

### F5 — Prefix-optimality is false
**Severity 2.** Source-grouped order, not bpq order. H (0.975 bpq) sits
after E/F/G. M (0.92 claimed) sits after J/K/L (0.67–0.75). Alternative
59-question prefix A–I + M + N + O/P is 59.61 claimed bits vs their
54.41; still 56.68 after the M+N correction. Within Block B, friendly.py
does not emit the published order (starts with a month cut, puts last
digit 0-4 4th). The published 12-question *set* does measure at 11.755
bits. 1995+ is not even a candidate in greedy.py / friendly.py.

### F6 — Q57 is not 50/50 among the living
**Severity 2.** "Taller than the median adult of your sex in your
country": children fail. Ages 0–17 ≈ 31% on their AGE_BAND_SHARE.
P(yes) ≈ 34.5%, MI(is_child, Q57) ≈ 0.24 bits already paid in Block B.

### F7 — 3.03 bits of own date left on the table
**Severity 2.** H(date) 14.79, Block B 11.76. After the published 12,
month-odd still adds 0.62. That beats K/L/Q. Unrestricted greedy in
their script continues to 18 questions / 14.68 bits. Mother's day+month
similarly has 2.54 bits unextracted.

### F8 — Twin counts are off; the qualitative point stands
**Severity 3.** "47 of the first 59" omits K (same siblings) → 50.
"57 of the 76" omits K → 60, and P is identical too → 62.
MZ is ~3.5/1000 deliveries ≈ 7/1000 people, not 0.4% of people.
Q76 often fails to split a twin pair (both light). Block Q joint
≈ 1.15 bits with that dependence, not 1.50.

### F9 — Q58 re-imports a rejection
**Severity 3.** Section 7 rejected minute-level birth time at ~40%
unknown. Q58 is AM/PM, unknown→no, printed ~50% yes. 40% unknown and
a 50/50 known half gives P(yes) = 30%. Extra no-mass tracks geography.

### F10 — Smaller register misses
Q50 vs Q51 MI = 0.029 (inside Block J's 1.00 discount, still undocumented).
Patronymic cultures: family name is a function of father's given name
where that system applies; unmeasured globally.

## Sound

- 33 vs ~65 as assigned-label vs random-attribute targets.
- Section 1 table applied to *their* bit counts.
- Block B as a set: 11.76 bits, yes-rates match.
- Date dependency register 1–8, 10 (indep.py).
- Parents' day+month is a fresh ~8.5-bit pool; excluding year from H was right.
- Dictionary A-M vs vowel result.

## Not checked

Real name-frequency × sex × ethnicity; global "knows mother's birthday"
rate; Q54/Q56 vs maternal age (exists, unquantified); dizygotic twins as
a second cluster; joint entropy of all 76; non-integer addressing systems;
cursor.out / fable.out beyond what QUESTIONS.md already absorbed.

Scripts: `/Users/cminds/claude-tmp/unique-human-questions/verify_math.py`
and `verify_more.py`.
