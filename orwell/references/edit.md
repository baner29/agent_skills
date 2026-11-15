# Edit mode: the full pass

The default job. Take a finished text and return the same text with the machine residue removed. The core rules in SKILL.md govern throughout: last mile, smallest change, nothing structural, the writer's voice wins ties.

## Before you start

- Where a shell is available, run `scripts/scan.py` on the text. Work from its hits instead of hunting by eye.
- Read references/banned-ai-words.md so the current list, including the user's own additions, is enforced.
- If a sentence and a rule pull apart at any point, consult references/orwell-judgment.md before forcing the rule.

## Step 1: Lock the content invariant

Separate substance from expression before touching a word.

- **Preserve completely:** facts, numbers, dates, named entities, technical claims, logical conclusions, hedges and qualifiers, and the writer's intended stance.
- **Edit only:** word choice, sentence structure within the writer's own shape, transitions, grammar, and punctuation.
- Never invent an example, add an external claim, or soften an explicit conclusion to sound balanced.
- **Protected spans pass through untouched:** direct quotations, code and code blocks, URLs and file paths, email addresses, citations, and data inside tables. A pass that rewrites a quote or a link has corrupted the content.
- **Preserve the register.** Natural does not mean informal. Match the original's formality and audience.
- **Preserve length and shape.** Keep the paragraph count and roughly the original length. This pass is not a summary and not an expansion.
- **Preserve the spelling convention** already in the text.

## Step 2: Scrub the machine patterns

Remove every match from the banned list, then work through the sentence habits:

1. **Banned vocabulary and dead transitions.** Replace flagged words (*delve*, *leverage*, *utilize*, *tapestry*, *pivotal*, *seamless*) and hollow openers ("In today's...", "It is worth noting", "Let's dive in") with plain, concrete language, or cut them where the sentence stands without them.
2. **Negative parallelisms.** Cut setups like "It is not X, it is Y" or "Less X, more Y". State the positive claim directly.
3. **Rule-of-three padding.** Break up rhythmic three-adjective or three-noun lists ("fast, reliable, and secure") unless three distinct items are factually required.
4. **Indirect copula inflation.** Replace "serves as", "stands as", "represents a" with "is" or "has".
5. **Trailing -ing commentary.** Remove tacked-on participle clauses ("...highlighting the importance of...", "...underscoring the need for...").
6. **Spotlight frames.** Cut "the part that matters", "what really counts is...", and other stage directions that announce importance instead of stating the point.
7. **False ranges.** Rewrite "whether you are X or Y" and "from X to Y" constructions that sweep without saying anything specific.
8. **Em-dash overuse.** Replace em dashes with periods, commas, colons, or parentheses, so pauses read as choices rather than habit.
9. **Flag, do not fix, vague attributions.** "Experts say" and "studies show" with no named source are machine tells, but inventing a source breaks the invariant. Leave the claim as written and note it for the user after the text.

## Step 3: Refine what is left

Work the three checks below only where a fault remains. The smallest-change rule governs this step: a sentence that already reads naturally is finished, however it is built.

1. **Coherence and cohesion.** Each paragraph keeps one central idea. Sentences flow from known information to new. Replace mechanical noun repetition with natural reference ("this approach", "they") where the repetition is the machine's, not the writer's emphasis. Use connectors ("however", "consequently") only where the logical link is not already obvious.
2. **Word choice.** Prefer the exact verb over a vague one with a modifier. Keep precise technical nouns intact: domain terminology is not jargon. Use natural collocations, the pairings native speakers make without thinking.
3. **Grammar and rhythm.** Check agreement, tense consistency, parallel structure, and modifier placement. Keep the writer's own mix of sentence lengths. Do not manufacture variety the draft does not have, and do not flatten variety it does.

### Worked example

**Before:** "In today's fast-paced digital landscape, organizations must leverage cutting-edge cloud solutions to unlock seamless scalability. It is not just about reducing hardware costs; it is about fostering an innovative, resilient, and agile ecosystem — ultimately underscoring the pivotal role of modern infrastructure."

**After:** "Organizations now use modern cloud platforms to scale capacity up or down as demand changes, without buying hardware up front. Lower hardware costs are only part of the gain; the systems also hold up under load and adapt as needs change. Modern infrastructure sits at the center of how organizations run."

Every claim in the original survives: scaling, reduced hardware costs, resilience, adaptability, and the central role of infrastructure. Nothing was added. If a rewrite needs a fact the original does not contain, the rewrite is wrong.

## Step 4: Verify before returning

- Re-read the output against the source, paragraph by paragraph. Every number, name, date, and claim is still present and unchanged in meaning.
- Confirm no new claim, example, or qualifier appeared, and none was dropped.
- Scan once more against the banned list and the Step 2 patterns. A rewrite often introduces a fresh cliché while removing another.
- Confirm protected spans are byte-identical to the source.
- Confirm register and spelling convention match the original.
- Ask Orwell's sixth question of the whole: have I said anything that is avoidably ugly? A fix that makes a sentence stiffer than the fault it cured fails Rule 6. Undo it.

**Output:** return the edited text only, unless the user asks for a change summary. List any flagged vague attributions briefly after the text.

## Gotchas

- **Over-editing into blandness.** Removing AI jargon does not mean stripping legitimate domain terms. *Semantic layer*, *gradient descent*, and *latency* stay.
- **Meaning drift in paraphrase.** Rewriting a complex sentence can invert cause and effect or drop a qualifier. The Step 4 re-read exists for this.
- **Connector swaps.** Replacing "Moreover" with "Furthermore" at every sentence start still reads like a machine. Logical order first, connectors second.
- **Register drift.** Editing often slides text toward casual. Check formality against the source, not against a generic idea of natural.
- **Stale list.** The banned list changes. Read it fresh on every edit job.
