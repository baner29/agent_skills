# The research behind Orwell

Background only. This file records what the scholarship says about how Orwell wrote, and which parts of it the skill uses. It is not a set of instructions. The edit path runs on SKILL.md, the mode files, and references/orwell-judgment.md. Load this file when a design question needs its evidence, not during an edit.

## Sources

The craft material rests on Orwell's own essays: *Politics and the English Language* (1946), the source of the six rules and the diagnostic questions; *Why I Write* (1946), the source of the windowpane ideal; and *The Prevention of Literature* (1946), on the freedom to report what one has seen and felt. The counter-evidence on the passive comes from Geoffrey Pullum's "Fear and Loathing of the English Passive" (*Language and Communication*, 2014) and from counts of Orwell's own usage in the scholarship. The corpus figures come from a stylistic study of seven Orwell essays applying Halliday's lexical density measure.

## What the numbers say

Lexical density is the share of content words (nouns, main verbs, adjectives, adverbs) in a text. Across seven essays, Orwell's density holds in a narrow band:

| Essay | Density |
| --- | --- |
| Politics and the English Language | 54.94% |
| Why I Write | 54.79% |
| A Hanging | 54.12% |
| The Prevention of Literature | 51.97% |
| Marrakech | 51.94% |
| Looking Back on the Spanish War | 51.54% |
| Shooting an Elephant (narrative) | 37.80% |

Analytical prose runs dense, about 52 to 55 percent. Narrative runs loose, about 38 percent, because pronouns, prepositions, and auxiliaries carry speed. The lesson for an editor is narrow: density is a property of genre, not a target. A user's narrative edited toward essay density would be ruined, and this skill does not try.

## Burstiness, and why it stays out of the edit path

Detectors separate machine text from human text partly by burstiness: the variation in sentence length and complexity. Machine prose runs flat; Orwell's runs spiked, a 31-word cumulative sentence against a 5-word question. A drafting tool can be told to build that contrast in. An editor cannot impose it on finished text without restructuring, which the last-mile rule forbids. So burstiness lives here, as background: it explains why machine text feels flat, and it tells the editor what to protect when a writer's own contrast is present. It never licenses manufacturing contrast. See the rhythm section of references/orwell-judgment.md.

## The four-stage workflow, mapped

The research proposes a four-stage pipeline for an Orwellian writing agent. Mapped onto this skill:

1. **Pre-draft concrete referent check.** Drafting-side. Before prose exists, name the claim and the physical facts under it. Not an edit step; the editor receives the draft as given.
2. **Lexical hygiene.** Edit-side. This is Step 2 of references/edit.md and the whole of references/scan.md.
3. **Burstiness and punctuation restraint.** Mostly drafting-side. The edit path takes only the restraint half: scarce semicolons, no manufactured rhythm.
4. **Pruning and calibration.** Edit-side. Rule 3 cutting, then Rule 6 calibration, which is Step 4 of references/edit.md and the substance of references/orwell-judgment.md.

## Traits that are his, not the user's

Orwell's voice has marks this skill must never import into a user's text: emphatic negation and deliberate overstatement as critical weapons, a conversational demotic register earned in journalism and radio, and strong directional purpose in everything he wrote. The skill borrows his standards for clarity. His personality stays in his essays, where it belongs. A text edited by this skill should sound like its own writer on a clear day, and like no one else.
