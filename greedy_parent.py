"""Choose the questions about a parent's birth YEAR by measured entropy gain.

Blocks M and N were hand-written, which reintroduced exactly the zero-information error the
document criticises elsewhere: "digit sum odd" is the XOR of "year even" and "tens digit odd",
so asking all three wastes a question.

This runs the same greedy selection used for Block B. The ceiling is H(parent's age at birth),
because given your own birth year their birth year is determined by that gap.
"""

import math
from collections import defaultdict

YOUR_YEAR_RANGE = range(1930, 2027)

MATERNAL_BANDS = {(15, 19): .11, (20, 24): .25, (25, 29): .26, (30, 34): .21,
                  (35, 39): .12, (40, 44): .04, (45, 49): .01}
PATERNAL_BANDS = {(18, 22): .08, (23, 27): .20, (28, 32): .25, (33, 37): .22,
                  (38, 42): .14, (43, 49): .08, (50, 60): .03}


def expand(bands):
    d = {}
    for (lo, hi), p in bands.items():
        for age in range(lo, hi + 1):
            d[age] = p / (hi - lo + 1)
    total = sum(d.values())
    return {k: v / total for k, v in d.items()}


CANDIDATES = {
    "their birth year is even":                 lambda y, a: y % 2 == 0,
    "last digit of their birth year is 0-4":    lambda y, a: y % 10 <= 4,
    "tens digit of their birth year is odd":    lambda y, a: (y // 10) % 2 == 1,
    "digits of their birth year sum to odd":    lambda y, a: sum(int(c) for c in str(y)) % 2 == 1,
    "their birth year mod 4 is 0 or 1":         lambda y, a: y % 4 in (0, 1),
    "they were born in 1970 or later":          lambda y, a: y >= 1970,
    "they were under 28 when you were born":    lambda y, a: a < 28,
    "they were under 23, or 33+, at your birth": lambda y, a: a < 23 or a >= 33,
    "their age at your birth was even":         lambda y, a: a % 2 == 0,
    "their age at your birth was 25-34":        lambda y, a: 25 <= a <= 34,
}


def build(age_dist):
    """Rows grouped BY your own birth year.

    Your birth year is already known from Block B, so the information these questions add is
    the CONDITIONAL entropy given that year, averaged over years. Pooling years instead would
    re-earn bits Block B already bought - which is how an earlier version of this script
    reported 8.2 bits against a 4.77-bit ceiling.
    """
    groups = []
    for your_year in YOUR_YEAR_RANGE:
        rows = [(your_year - age, age, p) for age, p in age_dist.items()]
        groups.append(rows)
    return groups, len(groups)


def entropy(keys, groups, n_groups):
    """H(answers | your birth year), averaged over your birth year."""
    total_h = 0.0
    for rows in groups:
        counts = defaultdict(float)
        w_sum = 0.0
        for y, a, w in rows:
            counts[tuple(CANDIDATES[k](y, a) for k in keys)] += w
            w_sum += w
        total_h += -sum((v / w_sum) * math.log2(v / w_sum) for v in counts.values() if v > 0)
    return total_h / n_groups


def run(label, bands):
    age_dist = expand(bands)
    ceiling = -sum(p * math.log2(p) for p in age_dist.values() if p > 0)
    groups, n_groups = build(age_dist)

    print(f"\n=== {label} ===")
    print(f"ceiling H(age at your birth) = {ceiling:.3f} bits\n")
    chosen, prev = [], 0.0
    while len(chosen) < len(CANDIDATES):
        best, best_h = None, prev
        for name in CANDIDATES:
            if name in chosen:
                continue
            h = entropy(chosen + [name], groups, n_groups)
            if h > best_h + 1e-9:
                best, best_h = name, h
        if best is None or best_h - prev < 0.25:
            break
        flat = [r for g in groups for r in g]
        tw = sum(r[2] for r in flat)
        yes = sum(w for y, a, w in flat if CANDIDATES[best](y, a)) / tw
        chosen.append(best)
        print(f"  {len(chosen)}  gain {best_h - prev:.3f}  cum {best_h:6.3f}  yes {yes*100:4.1f}%  {best}")
        prev = best_h

    print(f"\n  -> {len(chosen)} questions, {prev:.3f} bits")
    print("  not selected:")
    for name in CANDIDATES:
        if name not in chosen:
            print(f"     +{entropy(chosen + [name], groups, n_groups) - prev:.4f}  {name}")
    return len(chosen), prev


if __name__ == "__main__":
    qm, bm = run("Block M - mother's birth year", MATERNAL_BANDS)
    qn, bn = run("Block N - father's birth year", PATERNAL_BANDS)
    print(f"\nDocument claimed: 5 q / 4.60 bits and 5 q / 4.40 bits = 10 q / 9.00 bits")
    print(f"Measured:         {qm} q / {bm:.2f} bits and {qn} q / {bn:.2f} bits = {qm+qn} q / {bm+bn:.2f} bits")
