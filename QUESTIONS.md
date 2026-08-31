# Identifying every living human with yes/no questions

A worked answer to the "33 questions" problem, with the numbers measured rather than assumed.

**Headline: 33 questions does not almost work, it fails completely.** At 33 perfect
independent bits, 4.85 billion of 8 billion people still share their answer pattern with
somebody. The target was never 33. It is about 65.

The list below is **77 questions in logical order**, summing to 65.6 Shannon bits. The first
59 are the core list (54.4 bits, ~2,700 people still colliding); Blocks M-Q close most of the
rest.

Note that 65 is a count of **bits, not questions**. Real questions average 0.88 effective
bits, so 65 bits costs about 74-77 questions.

**Two caveats that the review put there, and both matter more than the headline:**

0. "Unique" has three thresholds 6.6 bits apart, and P(nobody collides) &ge; 0.99 needs
   **71.4 bits** - more than this list has. At 65.6 bits that probability is **0.57**. See
   section 1.
1. Collisions depend on **Renyi-2 entropy, not Shannon**, and names are heavily clustered.
   Correcting for that moves the answer from "1 person still colliding" to somewhere between
   **~5 and ~150**, dominated by real name-frequency data I never obtained. See section 5.
2. Section 9 explains why no number finishes the job: **60 of the 77 questions are answered
   identically by identical twins** by construction, so the last bits must come from questions
   that target within-pair difference, not from more questions of the same kind.

This document has been through an adversarial review by three other models (Sol, Fable, Grok). Every correction
they forced is marked in place rather than quietly folded in, and the dependency register
records who found what.

Measurement scripts live beside this file. Every number tagged MEASURED came out of them.

---

## 1. The premise was wrong, and this is the important part

The draft aimed at log2(8e9) = 32.9, so "about 33 questions". That is the number of bits
needed to *address* 8 billion people - to hand out 8 billion distinct labels if you were free
to assign them.

Nobody is assigning these labels. The answers fall out of facts people already have, so they
land pseudo-randomly across the pattern space and the birthday problem applies. With N people
in M = 2^b buckets, the expected number of colliding pairs is N²/2M. Setting that below 1
gives b = log2(N²/2) = 64.8 bits.

| bits | patterns | people who still share a pattern |
|-----:|---------:|---------------------------------:|
| 33 | 8.59e9 | 4.85e9 (61% of humanity) |
| 34 | 1.72e10 | 2.98e9 |
| 42 | 4.40e12 | 1.45e7 |
| 50 | 1.13e15 | 5.68e4 |
| 55 | 3.60e16 | 1,776 |
| 60 | 1.15e18 | 55 |
| 65 | 3.69e19 | 1.7 |

A serial number needs 33 bits. A set of questions about pre-existing facts needs about 65.
That gap of 32 questions is not a detail to tune away - it is the answer to the question the
file was asking.

### Three different thresholds, and I had been sliding between them

A second review round caught me quoting one metric and tabulating another. There are three,
and they are 6.6 bits apart:

| Target | Bits | Meaning |
|--------|-----:|---------|
| E[colliding pairs] < 1 | **64.80** | what section 1 originally derived |
| E[people not unique] < 1 | **65.80** | what every table in this document actually reports |
| **P(nobody collides) &ge; 0.99** | **71.43** | what "uniquely identifies every living human" plainly means |

The last row is the honest reading of the original question, and nothing in this document
reaches it. At this list's 65.62 bits, **P(all 8 billion unique) = 0.57** - a coin flip. Even
at the 68.11 bits I claimed before the review, it was only 0.90, so roughly one draw in ten
still contained a collision.

So "77 questions gets almost everyone" is true, and "77 questions uniquely identifies every
living human" is false even under the uniformity assumption that section 5 goes on to
demolish. *(Found by Sol, round 2.)*

---

## 2. What limits the count is entropy in the attributes, not cleverness

Every question mines some underlying fact, and no set of questions about a fact can extract
more bits than the fact contains.

- **H(your birth date) = 14.76 bits** MEASURED, over every valid date 1926-2026 weighted by
  an approximate world age distribution. That is a hard ceiling on all date questions
  combined, however many you invent. The draft's strategy of adding more date parities runs
  into this wall, and the wall is the reason the answer is not "just ask 65 date questions".
- A name is bounded by how many letters it has. You cannot ask about the 7th letter of a
  4-letter name.
- The way past the wall is **more people**, not more cleverness about one person: your
  mother's birth day and month is a fresh 8.5-bit pool that your own birth date says nothing
  about. Blocks H and I exploit this and are worth 11.7 bits between them.

---

## 3. Ordering principle: prefix-optimality

Grouped by data source, with blocks ordered so that a prefix of the list is a good identifier
of that length.

> **Known defect, found in review.** An earlier version claimed every prefix is the *best*
> identifier of its length. That is false as written. Blocks E, F and G (0.950 / 0.925 / 0.900
> bits per question) are placed ahead of H and I (0.975 / 0.967), which violates the rule.
> Measured worst-case loss against a purely bits-ranked order: **2.00 bits, at question 59**.
>
> The fix costs nothing and preserves source grouping: move the parents' *date* blocks
> (H, I, M, N) ahead of the parents' *name* blocks (E, F, G), giving the order
> **A B C D H I M N E F G O+P J K L Q**. That cuts the worst-case loss from 2.00 bits to
> **0.34**. That reordering **is applied** in [LIST.md](LIST.md), which is generated
> programmatically rather than renumbered by hand - hand-editing is precisely the operation
> that introduced the zero-bit questions in Blocks M and N. The block numbering below is left
> in its original order so the analysis and the review findings still line up.

Two reasons, and the first is the real one:

1. **Truncation is the normal case.** People abandon long questionnaires. If someone stops at
   question 13 they should be holding the best 13 questions available, not a random 13. So
   blocks are ordered by bits-per-question descending, adjusted for universality.
2. **Lookups are the real cost.** Grouping by source means a person fetches their birth
   certificate once, thinks about their own name once, and calls their mother once, instead
   of bouncing between sources 59 times.

Ordering purely by information content would scatter the sources; ordering purely by source
would bury the strong blocks. This does both: source-grouped, blocks ranked. Within Block B
the order is the exact greedy selection order, so even a partial answer to that block is
optimal for its length.

One caveat worth stating: for a fixed, non-adaptive questionnaire the order carries no
identification information at all - all 59 answers are collected regardless. Ordering matters
for **answer quality and drop-out**, not for entropy. At a 2% per-question error rate, the
chance of getting all 59 right is only 30%, which is a bigger practical threat than any
correlation discussed below.

---

## 4. The questions

### Block A - Sex (1 question, 1.00 bit)

Universal, no lookup, near-perfect split. It goes first.

| # | Question | Yes |
|---|----------|-----|
| 1 | Do you identify as male? *(under ~12: were you recorded male at birth?)* | 50.4% |

### Block B - Your age and birth date (12 questions, 11.76 bits MEASURED)

One lookup, twelve questions averaging 0.98 bits each. Chosen by greedy maximisation of joint
entropy over 29 candidate date predicates, so this is not taste: each question is the one
that adds the most given everything above it.

Question 2 doubles as the age question. Do not add further "born after year X" questions -
once question 2 is asked, "born 2001 or later" adds only 0.202 bits given the full block.
*(An earlier version said 0.188. Recomputed: 0.202 given all twelve questions, 0.364 given the
age question alone - the two reviewers disputed this and were measuring different contexts.)*

| # | Question | Yes | Gain |
|---|----------|-----|------|
| 2 | Were you born in 1995 or later? *(at or below the global median age, ~31 in 2026)* | 53.8% | 1.00 |
| 3 | Were you born in January-March or July-September? | 49.9% | 1.00 |
| 4 | Is your day-of-year an odd number? *(1 January = 1)* | 50.1% | 1.00 |
| 5 | Were you born in January-June? | 49.6% | 1.00 |
| 6 | Is your birth year an even number? | 50.5% | 1.00 |
| 7 | Is your birth day of the month the 16th or later? | 50.7% | 1.00 |
| 8 | Is your birth day of the month in 8-15 or 24-31? | 50.7% | 1.00 |
| 9 | Do the digits of your birth year add up to an odd number? | 49.1% | 1.00 |
| 10 | Were you born on a Monday, Tuesday or Wednesday? | 42.9% | 0.98 |
| 11 | Is your birth day of the month an odd number? | 51.0% | 0.96 |
| 12 | Were you born on a Tuesday, Thursday or Saturday? | 42.9% | 0.94 |
| 13 | Is the last digit of your birth year 0, 1, 2, 3 or 4? | 50.5% | 0.89 |

Stop at 13. The next candidate, "is your birth month odd-numbered", is worth 0.62 bits, and
it falls off a cliff after that.

**Why the weekday questions are legitimate.** Weekday is fully determined by an exact date, so
questions 10 and 12 look like cheating. They are not: questions 2-9 do not pin the date down,
and the greedy search measured their joint contribution on real dates. If you ever added
enough date questions to fix the date exactly, these two would collapse to zero.

### Block C - Your given name (6 questions, ~5.95 bits)

MEASURED, and this was the surprise: A-M cuts at different letter positions are **effectively
independent**. Mutual information between "1st letter A-M" and "2nd letter A-M" is 0.0045
bits; between 2nd and 3rd, 0.0007; between 1st and last, 0.0001. The A-M cut is coarse enough
to average over the phonotactic structure that makes individual letters correlate.

The same is emphatically *not* true of vowel questions: "1st letter is a vowel" and "2nd
letter is a vowel" share 0.278 bits. **Use A-M cuts. Never use vowel questions.**

*Spelling rule, stated once, applying to Blocks C-G:* use the spelling on your primary
government ID or birth certificate. If there is none, use the Latin spelling your family
normally uses. If your name has no Latin form, transliterate phonetically. Ignore hyphens,
apostrophes and spaces. Use your first given name, and your family name in your own culture's
sense of which one that is.

| # | Question | Yes |
|---|----------|-----|
| 14 | Does your first given name start with a letter A-M? | 51.8% |
| 15 | Is the 2nd letter of your first given name A-M? | 49.6% |
| 16 | Is the 3rd letter A-M? *(shorter name: answer no)* | 49.6% |
| 17 | Is the 4th letter A-M? *(shorter name: answer no)* | 54.4% |
| 18 | Is the last letter A-M? | 53.0% |
| 19 | Does your first given name have an odd number of letters? | 49.7% |

### Block D - Your family name (6 questions, ~5.95 bits)

Identical structure on a different name, so identical independence properties.

| # | Question | Yes |
|---|----------|-----|
| 20 | Does your family name start with a letter A-M? | ~51% |
| 21 | Is the 2nd letter of your family name A-M? | ~50% |
| 22 | Is the 3rd letter A-M? *(shorter: no)* | ~50% |
| 23 | Is the 4th letter A-M? *(shorter: no)* | ~54% |
| 24 | Is the last letter A-M? | ~53% |
| 25 | Does your family name have an odd number of letters? | ~50% |

### Block E - Your mother's given name (4 questions, ~3.80 bits)

From here you need someone else's help, which is why these blocks come after your own.
Discounted ~5% for cultural correlation: your mother's name and yours are drawn from
overlapping pools, so the bits are not quite free. This discount is an estimate - measuring it
needs real multi-cultural name-frequency tables, which I did not have.

| # | Question | Yes |
|---|----------|-----|
| 26 | Does your mother's first given name start A-M? | ~51% |
| 27 | Is its 2nd letter A-M? | ~50% |
| 28 | Is its 3rd letter A-M? *(shorter: no)* | ~50% |
| 29 | Is its last letter A-M? | ~53% |

### Block F - Your father's given name (4 questions, ~3.70 bits)

Discounted harder (~7%) for assortative naming: parents' names correlate with each other more
than either correlates with a stranger's.

| # | Question | Yes |
|---|----------|-----|
| 30 | Does your father's first given name start A-M? | ~51% |
| 31 | Is its 2nd letter A-M? | ~50% |
| 32 | Is its 3rd letter A-M? *(shorter: no)* | ~50% |
| 33 | Is its last letter A-M? | ~53% |

**You are now at question 33 with roughly 32.2 effective bits** - exactly what the original
file expected would finish the job. At 32.2 bits, **6.4 billion** people still share a pattern
with somebody. Keep going.

*(An earlier version said 4.6 billion here. That was wrong: I had paired the collision count
from the 33-bit row of the section 1 table with the 32.2-bit sum. 4.6 billion corresponds to
33.1 bits, not 32.2.)*

### Block G - Your mother's birth surname (4 questions, ~3.60 bits)

Discounted ~10%: roughly a fifth of people cannot answer, and "don't know -> no" both loses
the bit and correlates the non-answers with each other.

| # | Question | Yes |
|---|----------|-----|
| 34 | Does your mother's birth surname start A-M? | ~51% |
| 35 | Is its 2nd letter A-M? | ~50% |
| 36 | Is its 3rd letter A-M? *(shorter or unknown: no)* | ~50% |
| 37 | Is its last letter A-M? | ~53% |

### Block H - Your mother's birth day and month (6 questions, ~5.85 bits MEASURED)

**The best untapped source in the problem.** Your own birth date is capped at 14.76 bits, but
your mother's birth date is a completely separate 8.5-bit pool, and her *day and month* are
independent of everything about you. Six questions at 0.99 bits each.

Her birth **year** is deliberately excluded: it correlates with your own age via Block B.
Ask only day and month.

*If you do not know it: answer no to all six and accept the loss. Do not substitute anything
from your own birth date - that silently re-asks Block B.*

| # | Question | Yes | Gain |
|---|----------|-----|------|
| 38 | Was your mother born in January-March or July-September? | 49.9% | 1.00 |
| 39 | Is her day-of-year an odd number? | 50.1% | 1.00 |
| 40 | Was she born in January-June? | 49.6% | 1.00 |
| 41 | Was she born on the 16th or later? | 50.7% | 1.00 |
| 42 | Was she born on a day in 8-15 or 24-31? | 50.7% | 1.00 |
| 43 | Was she born on an odd-numbered day of the month? | 51.0% | 0.92 |

Stop at six. The seventh ("was she born in an odd-numbered month") is worth 0.49 bits.

### Block I - Your father's birth day and month (6 questions, ~5.80 bits)

The same six questions again. Discounted very slightly against Block H for assortative mating
on age, which touches the year but barely touches day and month.

| # | Question | Yes |
|---|----------|-----|
| 44 | Was your father born in January-March or July-September? | 49.9% |
| 45 | Is his day-of-year an odd number? | 50.1% |
| 46 | Was he born in January-June? | 49.6% |
| 47 | Was he born on the 16th or later? | 50.7% |
| 48 | Was he born on a day in 8-15 or 24-31? | 50.7% |
| 49 | Was he born on an odd-numbered day of the month? | 51.0% |

### Block J - Where you live (4 questions, ~3.00 bits)

The weakest universal block. *Fallback chain:* answer about your usual night-time residence;
failing that the address on your birth certificate; failing that your district of birth. If
none applies, answer no to all four and accept the loss - do not substitute a birth-date
fallback.

| # | Question | Yes |
|---|----------|-----|
| 50 | Is your house or building number even? | ~50% |
| 51 | Is the last digit of your house or building number 0-4? | ~50% |
| 52 | Is the numeric part of your postal code even? | ~50% |
| 53 | Does your street name start with a letter A-M? | ~50% |

### Block K - Family structure (3 questions, ~2.00 bits)

Three questions for two bits, because sibling questions overlap: an only child is forced to
answer no to both 54 and 55.

| # | Question | Yes |
|---|----------|-----|
| 54 | Do you have at least one older sibling by the same mother? | ~56% |
| 55 | Do you have at least one younger sibling by the same mother? | ~52% |
| 56 | Did your mother bear an even number of children in total? | ~48% |

### Block L - Body and birth circumstance (3 questions, ~2.00 bits)

Last, because they are the least reliable and most often unknown.

| # | Question | Yes |
|---|----------|-----|
| 57 | Are you taller than the median adult of your sex in your country? | ~50% |
| 58 | Were you born before noon, local time? *(unknown: answer no)* | ~50% |
| 59 | Does your town or city of birth start with a letter A-M? | ~51% |

---

## 4b. Blocks M-Q: getting from 54 bits to 68

The first 59 questions leave ~2,700 people colliding. These 17 close that gap. They come last
because each one costs either universality or answer reliability.

### Block M - Your mother's birth year (5 questions, 4.50 bits MEASURED)

**I originally excluded this, and I was wrong.** The reasoning was that her birth year
correlates with your age, so it is already bought. It is not. Her birth year equals your birth
year minus her age when she had you, and that age is itself uncertain:

**H(maternal age at birth) = 4.77 bits** (from the global age-at-birth distribution,
concentrated 20-34 but spread over 15-49). Once you know your own birth year exactly, her
birth year still carries 4.77 bits you do not have. Excluding both parents' birth years threw
away ~9.7 bits.

> **This block was rewritten after review.** The first version was hand-written rather than
> greedy-selected, and it reintroduced the exact zero-information error this document
> criticises elsewhere. Two of its five questions were worthless - see dependency 15. Blocks
> are now chosen by `greedy_parent.py`, which measures gain *conditional on your own birth
> year already being known*.

| # | Question | Yes | Gain |
|---|----------|-----|------|
| 60 | Is your mother's birth year an even number? | 50.0% | 1.00 |
| 61 | Is her birth year divisible by 4, or 1 more than a multiple of 4? | 50.0% | 1.00 |
| 62 | Was she under 23, or 33 or older, when you were born? | 51.4% | 0.95 |
| 63 | Is the last digit of her birth year 0, 1, 2, 3 or 4? | 50.0% | 0.56 |
| 64 | Was she under 28 when you were born? | 51.6% | *see note* |

Stop at five: the block is capped at 4.77 bits, and these reach 4.50.

**Rejected for this block, with measured gain:** "digits of her birth year sum to odd"
(+0.10), "tens digit of her birth year odd" (+0.11), "was she born in 1970 or later" (+0.01),
and **"was her age at your birth even" (+0.0000 - exactly zero)**, because given your birth
year and her birth-year parity, the parity of the gap is fixed.

### Block N - Your father's birth year (6 questions, 4.69 bits MEASURED)

**H(paternal age at birth) = 4.97 bits**, wider than maternal because the upper tail runs
further, which is why this block affords one more question than Block M.

| # | Question | Yes | Gain |
|---|----------|-----|------|
| 65 | Is your father's birth year an even number? | 50.0% | 1.00 |
| 66 | Is his birth year divisible by 4, or 1 more than a multiple of 4? | 50.0% | 1.00 |
| 67 | Was he between 25 and 34 when you were born? | 45.8% | 0.97 |
| 68 | Is the last digit of his birth year 0, 1, 2, 3 or 4? | 50.0% | 0.90 |
| 69 | Was he under 28 when you were born? | 28.0% | 0.56 |
| 70 | Is the tens digit of his birth year odd? | 50.0% | 0.25 |

**Rejected:** "digits of his birth year sum to odd" (+0.02), "born 1970 or later" (+0.02),
"age at your birth even" (+0.0000).

### Blocks O and P - Deeper into your own names (4 questions, ~3.20 bits)

Cheap bits, discounted because short names force a "no". Roughly a third of given names have
fewer than 6 letters, which is why these are worth ~0.8 bits each rather than 1.0.

| # | Question | Yes |
|---|----------|-----|
| 71 | Is the 5th letter of your first given name A-M? *(shorter: no)* | ~58% |
| 72 | Is the 6th letter of your first given name A-M? *(shorter: no)* | ~65% |
| 73 | Is the 5th letter of your family name A-M? *(shorter: no)* | ~57% |
| 74 | Is the 6th letter of your family name A-M? *(shorter: no)* | ~63% |

Note that these correlate with Blocks C and D through the shared "shorter name: no" rule -
among names under 5 letters, ~49.5% answer no to both the 3rd-letter and 5th-letter question.
The 3.20-bit credit accounts for the short-name skew but not this coupling, so treat it as an
upper bound.

### Block Q - Twin distinguishers (3 questions, 1.154 bits)

These have terrible splits and are here anyway, because they are the **only** questions in the
list that separate identical twins. Every other question is answered identically by both.

| # | Question | Yes | H |
|---|----------|-----|---|
| 75 | Were you born as part of a multiple birth (twin, triplet or more)? | ~2% | 0.141 |
| 76 | If so, were you delivered first? *(not a multiple: answer no)* | ~1% | 0.081 |
| 77 | Was your birth weight above 3.2 kg / 7 lb? *(unknown: answer no)* | ~45% | 0.993 |

**Corrected after review.** This block was credited 1.50 bits. The true joint is **1.154**:
question 76 is *forced* to "no" whenever 75 is "no", so H(Q75, Q76) = 0.161, not the 0.222 you
get by summing marginals. My own first correction to 1.215 made the same mistake in smaller
form. See dependency 16.

Question 76 is worth 0.081 bits averaged over everyone and is the single most valuable
question in the list for the ~56 million people it applies to.

---

## 5. The budget

| Block | Questions | Effective bits | Basis |
|-------|----------:|---------------:|-------|
| A Sex | 1 | 1.00 | known global split |
| B Your age + birth date | 12 | 11.76 | **MEASURED** |
| C Your given name | 6 | 5.95 | **MEASURED** (independence) |
| D Your family name | 6 | 5.95 | **MEASURED** (independence) |
| E Mother's given name | 4 | 3.80 | estimated, -5% |
| F Father's given name | 4 | 3.70 | estimated, -7% |
| G Mother's birth surname | 4 | 3.60 | estimated, -10% |
| H Mother's birth day+month | 6 | 5.85 | **MEASURED** |
| I Father's birth day+month | 6 | 5.80 | **MEASURED**, small discount |
| J Residence | 4 | 3.00 | estimated |
| K Family structure | 3 | 2.00 | estimated |
| L Body / birth | 3 | 2.00 | estimated |
| *core list* | *59* | *54.41* | |
| M Mother's birth year | 5 | 4.50 | **MEASURED** ceiling 4.77 |
| N Father's birth year | 6 | 4.69 | **MEASURED** in isolation |
| less M/N assortative-mating overlap | | -2.19 | dependency 20 |
| O+P Names, 5th-6th letters | 4 | 3.20 | estimated, upper bound |
| Q Twin distinguishers | 3 | 1.154 | **MEASURED** joint |
| Sum | 77 | 65.76 | |
| less Block K vs M/N overlap | | -0.14 | dependency 17 |
| **Shannon total** | **77** | **65.62** | |

### The Shannon total is the wrong number, and this is the review's deepest finding

Collisions do not depend on Shannon entropy. They depend on **Rényi-2 (collision) entropy**,
because expected colliding pairs = N²/2 &times; &Sigma;p&#178;, and &Sigma;p&#178; = 2^(-H&#8322;). And H&#8322; &le; H&#8321; always,
with equality only for a perfectly uniform distribution. Every clustered attribute - and names
are extremely clustered - loses more.

Measured on Block B: H&#8321; = 11.760, **H&#8322; = 11.588**, a 0.17-bit gap. Block B is nearly uniform by
construction, so that is close to a best case. The name blocks are the opposite: a review
estimate using real Chinese surname frequencies put Block D's within-population collision
entropy at ~4.25 against the 5.95 credited, a ~29% loss.

| If the name blocks lose | Effective bits | People still colliding |
|------------------------:|---------------:|-----------------------:|
| 0% (uniform, unreal) | 65.45 | 1.1 |
| 10% | 62.83 | 6.3 |
| 20% | 60.21 | 39 |
| **30% (the Chinese-surname figure)** | **57.59** | **152** |

**So the honest headline is not "0.2 people".** It is somewhere between about five and about a
hundred and fifty, and the width of that range is dominated by one thing I never measured:
real name-frequency data. The original claim of 0.2 assumed both uniformity that does not
exist and independence between the two parents that does not hold.

### Stopping points

| Stopping point | Questions | Shannon bits | People still colliding |
|----------------|----------:|-------------:|-----------------------:|
| Blocks A-G only | 37 | 35.8 | 1.03e9 |
| Core list, A-L | 59 | 54.41 | 2,674 |
| Full list, A-Q | 77 | 65.62 | 1.1 *(uniform assumption)* |
| Full list, realistic H&#8322; | 77 | ~58-63 | **~6 to ~150** |

Two comparisons worth keeping:

- Dropping Blocks H and I (parents' birthdays) costs 12 questions and takes the colliding
  count from 2,674 to **8.6 million**. Those twelve are worth more than the address, sibling
  and body blocks combined.
- Dropping Blocks M and N (parents' birth years) costs 11 questions and takes the colliding
  count from 1.1 to roughly **250**. I nearly left them out on a wrong assumption.

---

## 6. Dependency register

Every dependency found, with how it was established.

| # | Relationship | Status |
|---|--------------|--------|
| 1 | "sum of day+month is even" = NOT XOR("day odd", "month odd") | **PROVEN**, 0 mismatches across 372 day/month pairs. Zero bits. |
| 2 | "born in a leap year" leaks birth-year parity - every leap year is even | **MEASURED**, MI 0.304 bits, plus a 24.8/75.2 split. Rejected. |
| 3 | In an even calendar year, age parity is identical to birth-year parity (2026-Y and Y share parity) | **PROVEN**, 0 exceptions 1926-2026. Never ask "is your age even" alongside question 6. *(Found by Cursor.)* |
| 4 | "is your age odd" is determined by (year parity, born Jan-Jun) for half the population, and 83.2% predictable overall | **PROVEN** *(found by Fable)*. Excluded. |
| 5 | "born day 1-15" is the exact complement of "born day 16 or later" | **MEASURED**, MI 0.9999 bits. |
| 6 | "day > month" correlates with "day 16 or later", and is 100% yes for every date with day >= 16 | **MEASURED**, MI 0.262 bits, 78.6/21.4 split. Rejected. |
| 7 | "month name has an even number of letters" vs "born Jan-Jun" | **MEASURED**, MI 0.089 bits. Redundant given Block B. |
| 8 | "digits of birth year sum odd" vs "birth year even" | **MEASURED**: unconditionally independent (MI 0.0009) but *fully determined given the decade* (conditional MI 0.998). Safe to ask both, as Block B does. |
| 9 | Vowel-position questions correlate strongly with each other | **MEASURED**, MI 0.278 bits between 1st and 2nd letter. Excluded in favour of A-M cuts. |
| 10 | (day+month) mod 3 questions | **MEASURED**: add only 0.015 bits once Block B is in place. Rejected despite looking clever. |
| 11 | "firstborn" is the exact negation of "has an older sibling" | trivially deterministic. Only one is asked. |
| 12 | Parent-name questions vs your own name questions | Estimated 0.1-0.3 bits each through a shared cultural naming pool. **Not measured** - needs real multi-cultural name-frequency data. |
| 13 | Unhoused/unknown fallbacks in Blocks H, I and J | If a fallback borrows a fact from Block B, that block silently re-asks Block B. Handled by answering no instead. |
| 14 | Q55 vs Q56 (younger sibling vs even number of children) | Estimated MI ~0.21 bits. An only child is forced to no on Q54, Q55 and Q56 alike. *(Found by Sol.)* **Not measured.** |
| 15 | "digits of birth year sum to odd" = XOR("year even", "tens digit odd") | **PROVEN**, 0 exceptions over 1900-2099. digitsum(19xx) = 10+tens+last and digitsum(20xx) = 2+tens+last, so its parity is parity(tens) XOR parity(last). This made two questions in the first draft of Blocks M and N worth **exactly zero**. Block B escapes it only because Block B has no tens-digit question. *(Found by Fable.)* |
| 16 | Q76 is forced to "no" whenever Q75 is "no" | **PROVEN** by construction. H(Q75,Q76) = 0.161, not the 0.222 from summing marginals. Block Q's true joint is 1.154, not the 1.50 credited. *(Found by both reviewers.)* |
| 17 | "parent's age at your birth was even" carries zero bits | **PROVEN**: given your birth year and the parent's birth-year parity, the gap's parity is fixed. Rejected by `greedy_parent.py` at +0.0000. |
| 18 | Block K (sibling structure) vs Blocks M/N (parents' birth years) | Having older siblings raises maternal age at birth, which *is* Block M's entropy source. Measured MI 0.035-0.094 bits depending on the sibship model; budgeted as -0.14 across both parents. |
| 20 | Blocks M and N are not independent of each other | **MEASURED, and this one caught me out.** `greedy_parent.py` measures each parent's birth year in isolation, giving 4.50 + 4.69 = 9.19 bits. Parents' ages at your birth are correlated by assortative mating (fathers ~3 years older). Modelling the age gap with sd 2-4 years puts the JOINT ceiling at 7.8-8.8 bits, not 9.74, so the pair is over-credited by ~2.2 bits. **All three reviewers flagged this independently** (Sol 6.70, Fable ~6.5, Grok ~6) and all three were right. |
| 19 | Blocks O+P vs Blocks C/D via the "shorter name: no" rule | Among names under 5 letters, ~49.5% answer no to both the 3rd- and 5th-letter question. *(Found by Sol.)* **Not measured** beyond that figure. |

### Correction to an earlier claim of mine

I previously wrote that "digit sum of birth year odd" duplicated "birth year even" and was
worth well under a bit. That was wrong. Measured over 1926-2026 the two are independent
(MI 0.0009 bits) and the digit-sum question is worth a full 1.00 bits - the greedy search
picks it at position 9. The dependency is real but *conditional*: given the decade, one
determines the other. Both belong in the list.

---

## 7. What was rejected, and why

| Candidate | Split / reason |
|-----------|----------------|
| Northern vs southern hemisphere | 90/10 |
| Right-handed | 88/12 |
| Born on a weekday | 71/29 |
| Day number > month number | 79/21, plus dependency 6 |
| Born in a leap year | 25/75, plus leaks year parity |
| Born in a 31-day month | 59/41 |
| Birth date is a palindrome | ~0.1% yes |
| Prime birth year | ~20/80 across the living band |
| Belief in an afterlife, politics, religion | re-asks region |
| Shoe size even | sizing systems are not comparable across countries |
| Birth latitude/longitude parity | geography proxy dressed up as parity |
| Sum of day + month even | zero bits, dependency 1 |
| (day + month) mod 3 | 0.015 bits, dependency 10 |
| Name spelled backwards starts A-M | deterministic transform of the last-letter question |
| Alphabetical position of initial is even | for Latin script, a relabelling of the A-M cut |
| Even number of living grandparents | tracks age, already bought in Block B |
| Has a middle name | 30-45%, heavily culture-skewed |
| Hyphenated surname | 8-15% |
| Birth time to the minute | ~40% of living people have no recorded birth time |

---

## 8. Honest limits of this analysis

- The date measurements are solid: full enumeration of every valid date 1926-2026, weighted
  by an approximate world age distribution. Different age weights move the splits by fractions
  of a percentage point, not the conclusions.
- The name-independence result uses **English dictionary words as a proxy for names**, because
  no name-frequency corpus was available on this machine. The finding it supports - that A-M
  cuts at different positions barely interact while vowel questions do - is a structural
  property of coarse alphabet splits and should survive a change of corpus. The exact splits
  for real names will differ.
- Blocks E, F, G, J, K and L are estimated, not measured. Their discounts are reasoned
  guesses.
- The 54.41-bit total therefore carries real uncertainty, probably plus or minus 2 bits. That
  moves the "2,674 people" figure by a factor of a few in either direction. It does not move
  the headline.

---

## 9. Why full uniqueness is impossible, not merely expensive

Sections 1-5 treat this as a budget problem: buy enough bits and the collisions vanish. They
do not, and the reason is not statistical.

Consider identical twin sisters, born the same day, to the same parents, at the same address,
named Anna and Anne. Walk them through all 59 questions:

- Block A (sex): identical.
- Block B (birth date): identical.
- Blocks E, F, G (parents' names): identical.
- Blocks H, I (parents' birthdays): identical.
- Blocks J, K (address, siblings): identical.
- Block D (family name): identical.
- Block L: same birth morning, same birth city; only height is a coin flip.
- Block C (given name): **also identical.** Both are 4 letters, both start with A, both have
  N as the 2nd and 3rd letter, and both end in a letter in A-M. I checked all six questions
  mechanically - Anna and Anne produce the same answer to every one.

They differ on **nothing** except possibly question 57, height, which for identical twins is
close to a coin flip and often the same. Fifty-nine questions, and the list cannot tell them
apart.

The near-misses are just as bad: Sofia and Sonia differ on exactly one question of the six,
Anna and Alma on two.

Now count how much of the list this kills. Blocks A, B, D, E, F, G, H, I, J, K, M and N are
answered **identically** by both twins by construction - same sex, same birth date, same
family name, same two parents, same parents' birthdays, same parents' birth years, same
address, same siblings. That is **60 of the 77 questions** (1+12+6+4+4+4+6+6+4+3+5+6 = 61
minus question 56, which twins answer alike anyway), including every one of the high-value
blocks. Only Blocks C, O+P, L and Q can differ at all.

Adding more questions of the same kind cannot help, however many you add. This is the crucial
point about the bit budget: 68 bits is enough *on average*, but the average is not where the
problem is. Identical twins are ~0.4% of births, so roughly **32 million people, 16 million
pairs**, all sitting in the one region of the answer space that extra generic questions do not
reach.

*(An earlier version said 32 million people in 16 million pairs. That understated it about
twofold: I conflated "fraction of deliveries" with "fraction of people". At 3.5 monozygotic
births per 1000 deliveries, MZ twins are ~0.70% of people, not 0.35%.)*

The only questions that separate them are ones that target within-pair difference:

- **Block Q** (multiple birth, delivered first, birth weight) - which is exactly why three
  questions with 2%, 1% and 45% splits are in an otherwise 50/50 list. Question 76 is worth
  0.081 bits on average and is the single most valuable question in the list for the 56 million
  people it applies to.
- **Question 57** (height) - genuinely a coin flip between identical twins.
- **Blocks C, O** (given-name letters) - the only reason Anna and Anne could ever diverge, and
  as shown above, often they do not.

So the honest shape of the answer is not one number:

| | Questions | Result |
|---|---:|---|
| To address 8 billion people | 33 bits | but 61% still collide - the draft's error |
| For expected collisions below 1 | ~65 bits, **~70-76 questions** | achieved by this list |
| To separate identical twins | **no number** | needs targeted or designed attributes |

Getting the general population to uniqueness is a budget problem, and 76 questions solves it.
Getting *everyone* to uniqueness is not a budget problem, and no list of yes/no questions about
inherited facts solves it. That last step needs an attribute unique **by design** rather than
by accident - a national ID, a phone number, a biometric hash - at which point you have stopped
asking questions and started reading an identifier.
