"""Do opinion/preference questions carry independent bits, or do they collapse?

The claim in the 77-questions work is that belief questions "re-ask region" and so are worth
far less than their 50/50 splits suggest. That was asserted, never measured.

This measures the mechanism. Opinion answers are modelled the standard way: each question is a
threshold on a latent trait,

    answer_i = 1  iff  lambda_i . z + sqrt(1 - |lambda_i|^2) * e_i > 0

with z the shared latent factors (culture, religiosity, a left/right axis) and e_i independent
idiosyncratic noise. lambda is the factor loading: 0 means the question is pure idiosyncrasy,
0.7 means it is mostly just measuring the latent axis again.

Every question here is exactly 50/50 by construction. So any entropy shortfall is caused purely
by dependence, which is the thing being tested.
"""

import math
import random
from collections import defaultdict

TRIALS = 400_000
SEED = 11


def sample_answers(n_questions, loading, n_factors, rng):
    z = [rng.gauss(0, 1) for _ in range(n_factors)]
    out = []
    for i in range(n_questions):
        # spread each question's loading across the factors it belongs to
        f = i % n_factors
        common = loading * z[f]
        idio = math.sqrt(max(0.0, 1 - loading * loading)) * rng.gauss(0, 1)
        out.append(1 if common + idio > 0 else 0)
    return tuple(out)


def joint_entropy(n_questions, loading, n_factors, trials=TRIALS):
    """Monte-Carlo joint entropy. Reliable while 2^n_questions is well under `trials`."""
    rng = random.Random(SEED)
    counts = defaultdict(int)
    for _ in range(trials):
        counts[sample_answers(n_questions, loading, n_factors, rng)] += 1
    return -sum((c / trials) * math.log2(c / trials) for c in counts.values())


def bits_per_question(loading, n_factors, n=12):
    """Marginal rate: how much each extra question of this kind is worth, at the margin."""
    return joint_entropy(n, loading, n_factors) - joint_entropy(n - 1, loading, n_factors)


def main():
    print("Every question below is EXACTLY 50/50. Any shortfall is dependence alone.\n")
    print("Joint entropy of 12 questions, and the marginal value of the 12th:\n")
    print(f"  {'loading':>8}  {'kind of question':<34} {'12 q =':>8}  {'per q':>7}  {'to reach 65 bits':>17}")

    rows = [
        (0.00, "date parity / structural facts"),
        (0.15, "arbitrary taste (window vs aisle)"),
        (0.30, "mild cultural tint (breakfast)"),
        (0.50, "lifestyle, loosely ideological"),
        (0.65, "political attitude"),
        (0.80, "religious belief"),
    ]
    for loading, label in rows:
        h = joint_entropy(12, loading, n_factors=3)
        per = bits_per_question(loading, n_factors=3)
        need = 65 / per if per > 0.01 else float("inf")
        need_s = f"{need:,.0f} questions" if need < 1e5 else "unreachable"
        print(f"  {loading:8.2f}  {label:<34} {h:8.2f}  {per:7.3f}  {need_s:>17}")

    print("\nSame thing, but varying how many independent axes the opinions span")
    print("(loading fixed at 0.65 - a political attitude):\n")
    for k in (1, 2, 3, 5, 10):
        per = bits_per_question(0.65, n_factors=k)
        print(f"   {k:2} latent factor(s): {per:.3f} bits per question"
              f"  ->  {65/per:,.0f} questions for 65 bits")


if __name__ == "__main__":
    main()
