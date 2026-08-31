"""Same greedy selection, but restricted to questions a person can answer without arithmetic.

Compares the entropy reachable with 'natural' phrasings against the unrestricted optimum, so the
readability tax is a measured number rather than an opinion.
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


# Every one of these is answerable by reading a date off a document, with no mental arithmetic
# beyond "odd or even" and "is it before X".
FRIENDLY = {
    "Is your birth day of the month an odd number?":
        lambda d: d.day % 2 == 1,
    "Is your birth day the 16th or later?":
        lambda d: d.day >= 16,
    "Is your birth day in the range 8-15 or 24-31?":
        lambda d: 8 <= d.day <= 15 or d.day >= 24,
    "Is your birth month an odd-numbered month (Jan, Mar, May, Jul, Sep, Nov)?":
        lambda d: d.month % 2 == 1,
    "Were you born in January-June?":
        lambda d: d.month <= 6,
    "Were you born in Jan-Mar or Jul-Sep?":
        lambda d: d.month <= 3 or 7 <= d.month <= 9,
    "Is your birth year an even number?":
        lambda d: d.year % 2 == 0,
    "Is the last digit of your birth year 0, 1, 2, 3 or 4?":
        lambda d: d.year % 10 <= 4,
    "Is the tens digit of your birth year odd (e.g. 1987 -> 8 -> no)?":
        lambda d: (d.year // 10) % 2 == 1,
    "Do the digits of your birth year add up to an odd number?":
        lambda d: sum(int(c) for c in str(d.year)) % 2 == 1,
    "Were you born in 1976 or later?":
        lambda d: d.year >= 1976,
    "Were you born in 2001 or later?":
        lambda d: d.year >= 2001,
    "Were you born in 1951 or later?":
        lambda d: d.year >= 1951,
    "Were you born on a Monday, Tuesday or Wednesday?":
        lambda d: d.weekday() <= 2,
    "Were you born on a Tuesday, Thursday, Saturday (2nd, 4th, 6th day)?":
        lambda d: d.weekday() % 2 == 1,
    "Was the day you were born an odd-numbered day of the year?":
        lambda d: d.timetuple().tm_yday % 2 == 1,
}


def entropy_of(keys, table, total):
    counts = defaultdict(float)
    for row, w in table:
        counts[tuple(row[k] for k in keys)] += w
    return -sum((v / total) * math.log2(v / total) for v in counts.values() if v > 0)


def main():
    names = list(FRIENDLY)
    table = [({n: FRIENDLY[n](d) for n in names}, w) for d, w in population()]
    total = sum(w for _, w in table)

    chosen, prev = [], 0.0
    print(f"{'#':>2}  {'gain':>6}  {'cum':>6}  {'yes%':>5}  question")
    while len(chosen) < len(names):
        best, best_h = None, prev
        for n in names:
            if n in chosen:
                continue
            h = entropy_of(chosen + [n], table, total)
            if h > best_h + 1e-9:
                best, best_h = n, h
        if best is None or best_h - prev < 0.05:
            break
        p = sum(w for row, w in table if row[best]) / total
        chosen.append(best)
        print(f"{len(chosen):>2}  {best_h - prev:6.3f}  {best_h:6.3f}  {p*100:5.1f}  {best}")
        prev = best_h

    print(f"\n{len(chosen)} human-friendly date questions -> {prev:.3f} bits")
    print(f"unrestricted optimum at 13 questions was 12.695 bits; ceiling 14.757")
    for n in names:
        if n not in chosen:
            print(f"  dropped (+{entropy_of(chosen + [n], table, total) - prev:.4f}): {n}")


if __name__ == "__main__":
    main()
