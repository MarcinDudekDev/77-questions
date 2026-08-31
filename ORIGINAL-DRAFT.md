# Yes/No Questions to Uniquely Identify Humans

A working list of binary questions meant to give every living person a unique answer pattern.

Theoretical floor: log₂ of world population. For ~8 billion people that is about 33 questions. For a hard cap under 10 billion, 34 questions. That only works if every question splits the population near 50/50 *and* the questions are independent of each other.

The hard part is independence. Most human traits cluster (region, religion, language, age, politics). Structural / parity questions stay useful longer than opinion or geography questions.

---

## From our conversation

These are the ones we already trusted, or at least treated as usable.

### Structural / parity (best class)

1. Was your birthday on an odd-numbered day of the month?
2. Does your mother's first name start with a letter from A to M?
3. Is the street / house number where you live even?
4. Were you born in an even-numbered year?
5. Does the first letter of your first name come before N in the Latin alphabet?

### Demographic cuts that can be close to 50/50

6. Do you identify as male?
7. Are you at or below the current world median age? (about 30–31; this threshold drifts)

### Mentioned, then rejected or weakened

- Northern vs southern hemisphere — roughly 90/10
- Belief in an afterlife — closer to balanced than most opinions, but tightly correlated with religion, region, and politics
- Birth year is prime — sparse in the 1950–2010 band, closer to 80/20
- Born in a month with 31 days — about 58/42
- Shoe size is even — sizing systems differ by country; distribution is not symmetric
- Number of letters in full name is even — usable in principle, messy across scripts and naming customs

---

## New candidates

Rules used: prefer properties of numbers, letters, and dates the person already has; avoid population clusters; avoid asking the same underlying trait twice.

### More name / letter parity

8. Does your family / last name start with a letter from A to M?
9. Does your father's first name start with a letter from A to M?
10. Does the second letter of your first name come before N?
11. Does your first name have an odd number of letters (in its usual Latin or local-script spelling)?
12. Does your last name have an odd number of letters?
13. Is the last letter of your first name a vowel (A, E, I, O, U, and Y if you count Y)?
14. Do you have a middle name (or more than one given name)?

### More date / calendar parity

15. Is your birth month an odd-numbered month (January, March, May, July, September, November)?
16. Were you born in the first half of the month (day 1–15)?
17. Were you born in the first half of the year (January–June)?
18. Is the sum of your birth day and birth month an even number?
19. Is the sum of the digits of your birth year odd?
20. Were you born in a leap year?
21. Does the English name of your birth month have an even number of letters?
    (February, June, July, August, November, December)
22. If you write your birthday as day-then-month (for example 29 August → 29 and 8), is the day number larger than the month number?

### More address / place-as-number (arbitrary on purpose)

23. Is the last digit of your house / building number 0, 1, 2, 3, or 4?
24. Does the street name start with a letter from A to M?
25. Is the postal / ZIP code (or its numeric part) an even number?
26. If you take the longitude of your birthplace rounded to the nearest degree, is that number even?
27. If you take the latitude of your birthplace rounded to the nearest degree, is that number even?
    (Latitude *parity* is not the same as north/south of the equator.)

### Body / life facts that are not obviously clustered

28. Were you born during daylight hours local time (after sunrise, before sunset)?
    Approximate stand-in if exact sunrise is unknown: after 6 a.m. and before 6 p.m. local.
29. Are you right-handed?
    (This is *not* 50/50 — right-handers are ~85–90%. Keep only as a later, weaker splitter.)
30. Do you have at least one older sibling born to the same mother?
31. Are you taller than the median adult height in your birth-sex group?
    (Correlated with sex and region — weaker than it looks.)
32. Is the number of living grandparents you have even (0, 2, or 4)?

### Slightly weirder, still structural

33. Is the Unicode / alphabetical position of the first letter of your first name an even number (B, D, F…)?
34. Does your first name contain the letter E?
    (Common in many languages; not a clean 50/50, but fairly independent of house-number parity.)
35. Does your last name contain a hyphen, apostrophe, space, or other break (compound / multipart surname)?
36. Were you born on a weekday (Monday–Friday) rather than a weekend?
    (About 5/7, so not ideal — better as a late question.)
37. Is your birth date a palindrome in at least one common numeric format (for example 21-12-12, 10-02-2001)?
    Rare. Bad splitter. Listed only so we remember not to use it.
38. If you spell your first name backwards, does it still start with a letter from A to M?

---

## Best short list to actually try first

Use these first. They are the least entangled.

1. Odd birthday (day of month)
2. Even birth year
3. First name A–M
4. Last name A–M
5. Mother's first name A–M
6. Father's first name A–M
7. Even house number
8. Identify as male
9. At or below world median age
10. First name has an odd letter count
11. Last name has an odd letter count
12. Born day 1–15
13. Odd-numbered birth month
14. Even rounded birth-longitude
15. Even rounded birth-latitude
16. Sum of birth day + month is even
17. Sum of birth-year digits is odd
18. Have a middle name
19. Last digit of house number is 0–4
20. Street name A–M

Twenty independent-ish bits would make 2²⁰ = 1,048,576 groups. Against ~8 billion people that is still about 7,600 people per pattern. You would still need another 13–14 clean questions to reach one person.

---

## Traps to keep avoiding

- Geography that follows where people actually live (hemisphere, “are you in Asia,” equator, prime meridian as a *side* of the world).
- Opinions and beliefs (afterlife, politics, religion). They re-ask region.
- Any cut that is only good at one threshold (age), then drifts.
- Traits most people share (right-handed, brown eyes, lives in the northern hemisphere).
- Questions that secretly repeat an earlier bit (even year *and* last digit of year even).
- Anything a child, a person without an address, or a person with a non-Latin name cannot answer the same way.

---

## Status

This is a toy / information-theory list, not a finished identifier. The 2013 GitHub project “33 Questions” (MarkDunne) posed the same problem and still only listed two draft questions. Nobody has published a working set of 33 independent 50/50 questions.

Last updated: 30 August 2026
