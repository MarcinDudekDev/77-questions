"""Measure marginal splits and mutual dependence for birth-date-derived yes/no questions.

Enumerates every valid birth date for the living population window, weights each year by an
approximate world age distribution, then reports:
  - the honest marginal split of each predicate
  - pairwise mutual information (bits) between predicates
  - which predicates are EXACTLY determined by a pair of others

Weights are approximate UN-style 5-year band shares; they shift the numbers by a fraction of a
percent, not by the conclusions.
"""

import datetime
import itertools
from collections import defaultdict

THIS_YEAR = 2026
OLDEST = 1926

# Approximate share of world population per 5-year age band (0-4 .. 95-99), normalised below.
AGE_BAND_SHARE = [
    8.6, 8.5, 8.4, 8.3, 8.2, 8.0, 7.6, 7.0, 6.4, 5.8,
    5.2, 4.5, 3.8, 3.0, 2.2, 1.5, 0.9, 0.4, 0.15, 0.05,
]


def year_weight(year):
    age = THIS_YEAR - year
    band = min(age // 5, len(AGE_BAND_SHARE) - 1)
    return AGE_BAND_SHARE[band] / 5.0


def all_dates():
    """Yield (date, weight) for every valid birth date in the window."""
    for year in range(OLDEST, THIS_YEAR + 1):
        w = year_weight(year)
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    d = datetime.date(year, month, day)
                except ValueError:
                    continue
                yield d, w


MONTH_NAME = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

# Each predicate answers a yes/no question about a birth date.
PREDICATES = {
    "day_odd":            lambda d: d.day % 2 == 1,
    "month_odd":          lambda d: d.month % 2 == 1,
    "daymonth_sum_even":  lambda d: (d.day + d.month) % 2 == 0,
    "year_even":          lambda d: d.year % 2 == 0,
    "yeardigits_odd":     lambda d: sum(int(c) for c in str(d.year)) % 2 == 1,
    "day_1_15":           lambda d: d.day <= 15,
    "month_jan_jun":      lambda d: d.month <= 6,
    "leap_year":          lambda d: (d.year % 4 == 0 and d.year % 100 != 0) or d.year % 400 == 0,
    "monthname_even_len": lambda d: len(MONTH_NAME[d.month]) % 2 == 0,
    "day_gt_month":       lambda d: d.day > d.month,
    "weekday":            lambda d: d.weekday() < 5,
    "iso_week_odd":       lambda d: d.isocalendar()[1] % 2 == 1,
    "dayofyear_odd":      lambda d: d.timetuple().tm_yday % 2 == 1,
    "month_31days":       lambda d: d.month in (1, 3, 5, 7, 8, 10, 12),
    "day_ge_16":          lambda d: d.day >= 16,
    "quarter_h1":         lambda d: d.month <= 3 or 7 <= d.month <= 9,
}


def build_table():
    rows = defaultdict(float)
    names = list(PREDICATES)
    for d, w in all_dates():
        key = tuple(PREDICATES[n](d) for n in names)
        rows[key] += w
    total = sum(rows.values())
    return names, rows, total


def marginals(names, rows, total):
    out = {}
    for i, n in enumerate(names):
        p = sum(w for k, w in rows.items() if k[i]) / total
        out[n] = p
    return out


def entropy(p):
    import math
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def mutual_info(names, rows, total, i, j):
    import math
    joint = defaultdict(float)
    for k, w in rows.items():
        joint[(k[i], k[j])] += w
    mi = 0.0
    for (a, b), w in joint.items():
        pab = w / total
        pa = sum(v for (x, y), v in joint.items() if x == a) / total
        pb = sum(v for (x, y), v in joint.items() if y == b) / total
        if pab > 0:
            mi += pab * math.log2(pab / (pa * pb))
    return mi


def find_determined(names, rows):
    """Report predicates exactly determined by a PAIR of other predicates."""
    hits = []
    for target in range(len(names)):
        for a, b in itertools.combinations([x for x in range(len(names)) if x != target], 2):
            mapping = {}
            ok = True
            for k in rows:
                key = (k[a], k[b])
                if key in mapping and mapping[key] != k[target]:
                    ok = False
                    break
                mapping[key] = k[target]
            if ok:
                hits.append((names[target], names[a], names[b]))
    return hits


def main():
    names, rows, total = build_table()
    marg = marginals(names, rows, total)

    print(f"Birth dates {OLDEST}-{THIS_YEAR}, population-weighted. {len(rows)} distinct answer patterns.\n")
    print("MARGINAL SPLITS (yes%)")
    for n in sorted(names, key=lambda x: -abs(marg[x] - 0.5)):
        skew = abs(marg[n] - 0.5) * 100
        flag = "  <-- weak" if skew > 5 else ""
        print(f"  {n:22s} {marg[n]*100:5.1f}%   H={entropy(marg[n]):.4f} bits   skew {skew:4.1f}pp{flag}")

    print("\nEXACTLY DETERMINED BY A PAIR (carries ZERO new information)")
    hits = find_determined(names, rows)
    if not hits:
        print("  none")
    for t, a, b in hits:
        print(f"  {t:22s} = f({a}, {b})")

    print("\nHIGH PAIRWISE DEPENDENCE (mutual information > 0.02 bits)")
    pairs = []
    for i, j in itertools.combinations(range(len(names)), 2):
        mi = mutual_info(names, rows, total, i, j)
        if mi > 0.02:
            pairs.append((mi, names[i], names[j]))
    for mi, a, b in sorted(pairs, reverse=True):
        print(f"  {mi:6.4f} bits  {a} <-> {b}")


if __name__ == "__main__":
    main()
