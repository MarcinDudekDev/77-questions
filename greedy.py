"""Greedily choose the birth-date questions that extract the most real entropy.

At each step, pick the candidate predicate that maximises the joint entropy of the set chosen
so far. That automatically refuses zero-information questions (FLAW 1) and heavily discounts
near-duplicates, because neither raises the joint entropy.

The ceiling is H(birth date) itself, so this also shows exactly where the date runs dry.
"""

import datetime
import math
from collections import defaultdict

THIS_YEAR = 2026
OLDEST = 1926
AGE_BAND_SHARE = [
    8.6, 8.5, 8.4, 8.3, 8.2, 8.0, 7.6, 7.0, 6.4, 5.8,
    5.2, 4.5, 3.8, 3.0, 2.2, 1.5, 0.9, 0.4, 0.15, 0.05,
]

MONTH_NAME = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]


def year_weight(year):
    return AGE_BAND_SHARE[min((THIS_YEAR - year) // 5, len(AGE_BAND_SHARE) - 1)] / 5.0


def population():
    for year in range(OLDEST, THIS_YEAR + 1):
        w = year_weight(year)
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    yield datetime.date(year, month, day), w
                except ValueError:
                    continue


CANDIDATES = {
    "day is odd":                       lambda d: d.day % 2 == 1,
    "day is 16th or later":             lambda d: d.day >= 16,
    "day is in 8-15 or 24-31":          lambda d: 8 <= d.day <= 15 or d.day >= 24,
    "day mod 4 is 0 or 1":              lambda d: d.day % 4 in (0, 1),
    "day's last digit is 0-4":          lambda d: d.day % 10 <= 4,
    "month is odd":                     lambda d: d.month % 2 == 1,
    "month is Jan-Jun":                 lambda d: d.month <= 6,
    "month is Jan-Mar or Jul-Sep":      lambda d: d.month <= 3 or 7 <= d.month <= 9,
    "month name has even letters":      lambda d: len(MONTH_NAME[d.month]) % 2 == 0,
    "year is even":                     lambda d: d.year % 2 == 0,
    "year's tens digit is odd":         lambda d: (d.year // 10) % 2 == 1,
    "year's last digit is 0-4":         lambda d: d.year % 10 <= 4,
    "year mod 4 is 0 or 1":             lambda d: d.year % 4 in (0, 1),
    "year is 1976 or later":            lambda d: d.year >= 1976,
    "year is in a 'young' 25y band":    lambda d: (THIS_YEAR - d.year) % 50 < 25,
    "year digit sum is odd":            lambda d: sum(int(c) for c in str(d.year)) % 2 == 1,
    "day-of-year is odd":               lambda d: d.timetuple().tm_yday % 2 == 1,
    "day-of-year in 2nd half":          lambda d: d.timetuple().tm_yday > 183,
    "ISO week is odd":                  lambda d: d.isocalendar()[1] % 2 == 1,
    "ISO week mod 4 is 0 or 1":         lambda d: d.isocalendar()[1] % 4 in (0, 1),
    "weekday is Mon-Wed":               lambda d: d.weekday() <= 2,
    "weekday index is odd":             lambda d: d.weekday() % 2 == 1,
    "(day+month) mod 3 == 1":           lambda d: (d.day + d.month) % 3 == 1,
    "(day+month) mod 3 == 2":           lambda d: (d.day + d.month) % 3 == 2,
    "(day+month) is even":              lambda d: (d.day + d.month) % 2 == 0,
    "day > month":                      lambda d: d.day > d.month,
    "leap year":                        lambda d: (d.year % 4 == 0 and d.year % 100 != 0) or d.year % 400 == 0,
    "born on a weekday":                lambda d: d.weekday() < 5,
    "month has 31 days":                lambda d: d.month in (1, 3, 5, 7, 8, 10, 12),
}


def entropy_of(keys, table):
    counts = defaultdict(float)
    total = 0.0
    for row, w in table:
        counts[tuple(row[k] for k in keys)] += w
        total += w
    return -sum((v / total) * math.log2(v / total) for v in counts.values() if v > 0)


def main():
    names = list(CANDIDATES)
    table = []
    for d, w in population():
        table.append(({n: CANDIDATES[n](d) for n in names}, w))

    ceiling = entropy_of(names, table)
    total_w = sum(w for _, w in table)
    print(f"H(birth date) ceiling = {ceiling:.3f} bits\n")

    chosen = []
    prev = 0.0
    print(f"{'#':>2}  {'gain':>6}  {'cum':>6}  {'yes%':>5}  question")
    while len(chosen) < 18:
        best, best_h = None, prev
        for n in names:
            if n in chosen:
                continue
            h = entropy_of(chosen + [n], table)
            if h > best_h + 1e-9:
                best, best_h = n, h
        if best is None:
            break
        gain = best_h - prev
        if gain < 0.02:
            print(f"\n  -- stopping: best remaining candidate adds only {gain:.4f} bits --")
            break
        p = sum(w for row, w in table if row[best]) / total_w
        chosen.append(best)
        prev = best_h
        print(f"{len(chosen):>2}  {gain:6.3f}  {best_h:6.3f}  {p*100:5.1f}  {best}")

    print(f"\nchosen {len(chosen)} date questions -> {prev:.3f} bits "
          f"({prev/len(chosen):.3f} bits per question, ceiling {ceiling:.3f})")

    print("\nREJECTED (never selected - they add nothing the chosen set does not already have):")
    for n in names:
        if n not in chosen:
            h = entropy_of(chosen + [n], table)
            print(f"  +{h - prev:.4f} bits   {n}")


if __name__ == "__main__":
    main()
