# 77 Questions

**How many yes/no questions does it take to uniquely identify every living human?**

Not 33. That is the whole finding.

In 2013, [MarkDunne/33-questions](https://github.com/MarkDunne/33-questions) posed this
problem, gathered 361 stars, and stopped after two questions. Thirteen years and 39 forks
later it still lists `3. ...`. Nobody finished it.

This repo finishes it, and explains why nobody could have finished it at 33.

**[→ LIST.md — the 77 questions](LIST.md)**

---

## The error in the original

The original README contains the mistake in two consecutive sentences:

> We could give everybody on the planet a unique series of 33 1s and 0s, and identify anyone by
> their personal series. But that would be boring.
>
> What if, instead of assigning 1s and 0s, we had 33 'Yes' or 'No' general questions that, when
> answered correctly, uniquely identified everyone on the planet.

Those are not the same problem, and the gap between them is 32 questions.

`log2(8e9) = 32.9` bits is what it costs to **assign** 8 billion serial numbers, when you
control the assignment. Answers to questions about facts people already have are not assigned.
They land pseudo-randomly, so the **birthday problem** applies: expected colliding pairs is
`N²/2M`, and pushing that below 1 needs `log2(N²/2) = 64.8` bits.

**At 33 perfect, independent, exactly-50/50 bits, 4.85 billion of 8 billion people still share
their answer pattern with somebody.** Not "a few collisions". Sixty-one percent of humanity.

It gets worse, because "unique" has three thresholds:

| Target | Bits |
|--------|-----:|
| E[colliding pairs] < 1 | 64.80 |
| E[people not unique] < 1 | 65.80 |
| **P(nobody collides) ≥ 0.99** | **71.43** |

The last row is what the question plainly means. This list reaches 65.6 bits, so
**P(all 8 billion unique) ≈ 0.57** — a coin flip. That is stated up front rather than buried,
because the honest answer to the original question is "you can't, and here is how close you
get".

## What is measured, not assumed

Every number tagged MEASURED came out of the scripts in this repo. Highlights:

- **`H(birth date) = 14.76 bits`**, over every valid date 1926–2026 weighted by world age
  distribution. A hard ceiling on all date questions combined, however many you invent — which
  is why "add more date parities" cannot work.
- **The best 12 human-answerable date questions extract 11.76 bits** (0.98 each). The 13th is
  worth 0.62 and it collapses from there.
- **The readability tax is zero.** Restricting to questions answerable without arithmetic costs
  nothing measurable.
- **A–M letter cuts at different positions of a name are effectively independent**
  (MI < 0.005 bits). Vowel-position questions are *not* (MI 0.278). The A–M cut is coarse
  enough to average over the phonotactics that make individual letters correlate.
- **A parent's birth day+month is a fresh 5.9-bit pool** your own birth date says nothing
  about. The way past the entropy ceiling is more *people*, not more cleverness about one
  person.
- **"Sum of day + month is even" carries exactly zero bits** given day parity and month parity.
  Brute-forced: 0 mismatches across all 372 day/month pairs.

## Where this is wrong

Kept deliberately, because a list like this is only useful with its error bars:

- The name-independence result uses **English dictionary words as a proxy for names**. No
  name-frequency corpus was to hand. The structural finding should survive a change of corpus;
  the exact splits will not.
- **Six of the sixteen blocks are estimated, not measured** — both parents' given names, the
  mother's birth surname, residence, family structure, body.
- Collisions depend on **Rényi-2 entropy**, not Shannon, and names cluster hard. Correcting for
  that moves the answer from ~1 person colliding to somewhere between **6 and 150**. The width
  of that range is set entirely by the name data that is missing.

## The part no number fixes

Identical twin sisters, same day, same parents, same address, named **Anna and Anne**.

Sixty of the 77 questions are identical for them by construction. And the given-name block —
the one thing that should separate them — does not: both are four letters, both start with A,
both have N as the 2nd and 3rd letter, both end in a letter in A–M. Checked mechanically, they
give **the same answer to all six**. Sofia and Sonia differ on one. Anna and Alma on two.

No number of added questions fixes this, because the questions interrogate *shared facts*. The
collisions that survive are not scattered at random; they concentrate exactly where two
people's lives overlap. Roughly **28 million identical twin pairs** sit in the one region extra
generic questions never reach.

That is why the list ends with three questions whose splits are 2%, 1% and 45%. They are the
only ones that can separate twins. Question 76 is worth 0.081 bits averaged over everyone, and
is the single most valuable question in the list for the 56 million people it applies to.

**Getting the general population to uniqueness is a budget problem, and 77 questions nearly
solves it. Getting everyone there is not a budget problem, and no list of yes/no questions
about inherited facts solves it.** That needs an attribute unique by design — a national ID, a
phone number, a biometric hash — at which point you have stopped asking questions and started
reading an identifier.

## Files

| File | What it is |
|------|-----------|
| [`LIST.md`](LIST.md) | **The 77 questions, in order. Start here.** |
| [`QUESTIONS.md`](QUESTIONS.md) | The working: entropy budget, 20-entry dependency register, every correction marked in place |
| [`ORIGINAL-DRAFT.md`](ORIGINAL-DRAFT.md) | Where this started, before any of it was measured |
| `greedy.py` | Picks the date questions by joint-entropy gain over 29 candidates |
| `indep.py` | Dependency scan: marginals, pairwise mutual information, exact-determination search |
| `friendly.py` | The same selection restricted to questions answerable without arithmetic |
| `greedy_parent.py` | Picks the parents' birth-year questions |
| [`reviews/`](reviews/) | Four adversarial reviews that found ten errors in this work |

```
python3 indep.py         # finds the zero-information questions
python3 greedy.py        # the date block, and where birth dates run dry
python3 friendly.py      # human-answerable variant
python3 greedy_parent.py # the parents' birth-year blocks
```

Standard library only.

## On the reviews

The four files in `reviews/` are adversarial critiques of this work by three different language
models (Cursor's Sol twice, plus Fable and Grok). They found ten real errors, including two
questions I had introduced that carried **exactly zero bits** — the same class of mistake this
repo criticises the original draft for.

They are kept in full, unedited, because the corrections are more interesting than the list.
The most useful single moment: all three independently said one block was worth ~6.5 bits when
the budget claimed 9.19. All three were right.

## Credit

Builds directly on [MarkDunne/33-questions](https://github.com/MarkDunne/33-questions) (2013),
which asked exactly the right question with the wrong number. The framing is theirs. None of
the content is — that repo contains two questions, and this one disagrees with both of them.

## Licence

MIT. Take the questions, take the scripts, and if you have real multi-cultural name-frequency
data, please open an issue — that is the single measurement this analysis is missing.
