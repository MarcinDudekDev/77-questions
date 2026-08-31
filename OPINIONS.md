# Appendix: were the opinion questions wrongly thrown out?

The original 2013 draft rejected belief and preference questions because "they re-ask region".
[QUESTIONS.md](QUESTIONS.md) inherited that judgement and repeated it. Neither ever measured it.

Marcin's reaction on reading the finished list was that he had been picturing something else
entirely - divisive questions about religion, politics, taste - and that the answer had come
back built purely on structural facts. That is a fair challenge, so here is the measurement.

Run it: `python3 opinions.py`

## The model

Opinion answers are modelled the standard psychometric way. Each question is a threshold on a
latent trait:

```
answer_i = 1  iff  lambda * z_f + sqrt(1 - lambda^2) * e_i > 0
```

`z` is the shared latent factor (culture, religiosity, a left/right axis), `e_i` is
question-specific noise, and `lambda` is the factor loading. Loading 0 is pure idiosyncrasy;
0.8 is a question that mostly just measures the axis again.

**Every question is exactly 50/50 by construction**, so any entropy shortfall is caused purely
by dependence - which is the thing under test.

## Result

Joint entropy of 12 such questions, and the marginal value of the twelfth:

| Loading | Kind of question | 12 q | per q | to reach 65 bits |
|--------:|------------------|-----:|------:|-----------------:|
| 0.00 | date parity, structural facts | 11.99 | 0.996 | 65 questions |
| 0.15 | arbitrary taste (window vs aisle) | 11.99 | 0.996 | 65 questions |
| 0.30 | mild cultural tint (sweet vs savoury breakfast) | 11.95 | 0.989 | 66 questions |
| 0.50 | lifestyle, loosely ideological | 11.71 | 0.950 | 68 questions |
| 0.65 | political attitude | 11.21 | 0.877 | 74 questions |
| 0.80 | religious belief | 10.18 | 0.743 | 88 questions |

**The blanket rejection was wrong.** Even religious belief - the most latent-loaded case here -
costs 88 questions instead of 65. That is a 35% tax, not a collapse. Arbitrary taste questions
are indistinguishable from date parity.

## Why the collapse does not happen

Because conditional on the latent trait, the answers are independent. A shared factor is **one
number**, so it can only ever explain away about `log2(n)` bits in total, however many
questions load on it:

| n questions (loading 0.80, one factor) | joint H | bits lost | log2(n) |
|---:|---:|---:|---:|
| 2 | 1.85 | 0.15 | 1.00 |
| 4 | 3.40 | 0.60 | 2.00 |
| 8 | 6.23 | 1.77 | 3.00 |
| 12 | 8.93 | 3.07 | 3.58 |
| 14 | 10.23 | 3.77 | 3.81 |

The loss tracks `log2(n)`, not `n`. Each question keeps its own idiosyncratic noise no matter
how strongly it loads.

I had claimed, off the cuff, that "thirty such questions might carry six effective bits".
Extrapolating the table, thirty would carry roughly **24**. I was out by a factor of four, in
the direction that conveniently supported the approach I had already taken.

## What actually kills opinion questions

Not latent structure - **near-duplicate questions**. "Do you believe in God?", "Do you pray?"
and "Do you attend services?" are not three draws on a latent trait with independent noise.
They are close to the same question asked three times, and *that* is a genuine collapse.

Which is the same failure mode as ["sum of day and month is even"](QUESTIONS.md) sitting
alongside day-parity and month-parity: a question that is a function of the others. It is a
curable design error, not a property of the subject matter.

## Conclusion

A list built from preferences would work. It would need roughly 15-35% more questions than this
one, and it would need exactly the same dependency discipline applied - which nobody has done,
because measuring dependence between opinion questions needs real survey microdata rather than
a closed-form model.

It would also fix this list's worst practical flaw: **the 77 questions here require a birth
certificate and two living parents.** A preference-based list requires nothing but the person.

That is a better trade than this project assumed, and the assumption went unexamined for the
same reason the original 2013 repo's did - it was inherited, sounded right, and nobody checked.
