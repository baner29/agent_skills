# Scan mode: report, do not rewrite

The user wants to know how much machine patterning a text carries, and where. Scan mode answers that and changes nothing.

## Method

1. Where a shell is available, run `scripts/scan.py` on the text. It applies references/banned-ai-words.md mechanically and reports sentence statistics: count, average length, and every sentence over 30 words.
2. Read for the patterns a word list cannot catch: negative parallelisms, rule-of-three padding, spotlight frames, false ranges, trailing -ing commentary, and vague attributions with no named source.
3. Treat hits inside quotation marks as examples, not faults, unless the quoted matter is presented as the writer's own prose.

## Report

Keep it short and factual:

- **Counts:** banned words and phrases found, by type, with the worst offenders named.
- **Patterns:** each structural pattern found, with one short quoted instance of each.
- **Shape:** sentence count, average sentence length, and the count of sentences over 30 words.
- **Flags:** vague attributions, listed exactly as written. These are for the user to source or cut. Never propose an invented source.
- **One-line verdict:** where the machine patterning concentrates (vocabulary, sentence habits, or structure), in plain words. No score unless the user asks for one.

Do not rewrite sentences in the report. A quoted instance is evidence, not an invitation. If the user then asks for the fix, that is edit mode: load references/edit.md and run the full pass.
