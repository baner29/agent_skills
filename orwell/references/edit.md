# Edit mode: the full pass

The default job. Take a finished text and return it simpler: same point, same needed facts, less weight. The core rules in SKILL.md govern throughout: read the context first, keep what the reader needs, cut what adds nothing in context, and rebuild sentences freely when a rebuild is clearer.

## Before you start

- Where a shell is available, run `scripts/scan.py` on the text. Work from its hits instead of hunting by eye.
- Read references/banned-ai-words.md so the current list, including the user's own additions, is enforced.
- If a sentence and a rule pull apart at any point, consult references/orwell-judgment.md before forcing the rule.

## Step 1: Settle the context

Write down, for yourself, before touching a word:

- **Purpose:** what this text must do (inform, ask, decide, instruct, persuade, report, reply).
- **Reader:** who reads it, what they already know, and what they must be able to do or understand after reading.
- **Point per paragraph:** one line each. A paragraph with no point is a cut candidate. A paragraph with two points may need a split.

If the user gave no context beyond the text, take the purpose and reader from the text itself. If both stay unclear, edit with care: cut filler, repetition, and machine habits only, and keep every detail that could matter.

## Step 2: Lock what must stay

Separate the load-bearing content from the weight around it.

- **Keep completely:** the main point and stance, conclusions, facts, numbers, dates, and names the reader needs, conditions, limits, risks, causes, evidence, and hedges that change certainty.
- **Protected spans pass through untouched:** direct quotations, code and code blocks, URLs and file paths, email addresses, citations, and data inside tables. A pass that rewrites a quote or a link has corrupted the content.
- **Preserve the register.** Simple does not mean informal. Match the original's formality and audience.
- **Preserve the spelling convention** already in the text.
- Never invent an example, add an external claim, or soften an explicit conclusion to sound balanced.

Length and shape are no longer locked. The output may be shorter than the input, and usually should be. It may not be shorter because a needed fact was dropped to save words.

## Step 3: Cut what adds nothing in context

Work paragraph by paragraph. Apply the cut test to every clause, detail, and sentence: if this goes, does the reader lose anything they need to act, decide, judge, or understand the point?

Cut, in this order:

1. **Irrelevant details.** True facts that change nothing here: reasons, motives, background, and personal preferences the reader does not need and did not ask for.
2. **Restatement.** Sentences or clauses that repeat the question, the previous sentence, or a point already made.
3. **Unasked answers.** Clauses that explain something nobody in this context needs explained.
4. **Delay.** Openers and scene-setting that postpone the point ("I am writing to inform you that...", "As mentioned in our previous discussion regarding...").
5. **Duplicate proof.** A second example, statistic, or anecdote that proves the same point as the first, unless the list itself is the point.
6. **Empty qualifiers.** "In my personal opinion", "it is important to note that", "due to the fact that" and their kin. Cut the frame, keep the claim.

### Worked example: the counter test

Context: a customer answering a food counter worker who asked what to add or remove.

**Before:** "Yes, please remove the tomatoes from my burger, as I do not like tomatoes and I find that they tend to make the burger soggy for my taste."

**After:** "Yes, no tomatoes, please."

The request survives whole. The reason goes because the worker needs the instruction, not the reason, to act. In a different context the same reason stays: in a review, a recipe note, or a letter about an allergy, why the tomatoes come out is part of the point. Relevance is judged in context, never from the sentence alone. An allergy, a deadline, a cost limit, or any detail that changes what the reader should do is load-bearing and stays in every context.

When a cut removes a full sentence or a named fact, and the user has asked for a change summary, list the cuts and the reason for each in one line. Otherwise return the text only.

## Step 4: Remove needless complexity

With the weight gone, simplify what is left. Sentence structure is open: rebuild any sentence that reads more clearly in a new shape.

1. **Unstack clauses.** A sentence carrying three or more subordinate clauses gets split or rebuilt so each idea lands once, in order.
2. **Put the actor and the action first.** "A decision was made by the team to postpone" becomes "The team postponed it", unless the passive is the honest form (see references/orwell-judgment.md).
3. **Turn noun piles back into verbs.** "Make an assessment of" becomes "assess". "In the event that" becomes "if". "Has the ability to" becomes "can".
4. **Cut word-level padding.** Apply Orwell's Rule 3 word by word after the clause-level cuts: if a word can go and the meaning stays, it goes.
5. **One idea per sentence, in the order the reader needs it.** Known information first, new information next. Move a clause earlier or later inside the paragraph when the current order forces the reader to hold too much in mind.
6. **Keep needed precision.** A condition, a number, or a technical term that carries the point is not complexity. It stays, in its exact form.

### Worked example: complexity

**Before:** "In today's fast-paced digital landscape, organizations must leverage cutting-edge cloud solutions to unlock seamless scalability. It is not just about reducing hardware costs; it is about fostering an innovative, resilient, and agile ecosystem, ultimately underscoring the pivotal role of modern infrastructure in the facilitation of organizational growth and the enhancement of operational efficiency."

**After:** "Organizations now use modern cloud platforms to scale capacity as demand changes, without buying hardware up front. The gain is lower hardware costs, systems that hold up under load, and room to change as needs change."

What went: the opener, the banned words, the negative parallelism, the trailing commentary, and the final clause, which restated the point in bigger words. What stayed: scaling, lower hardware costs, holding up under load, and adapting. Nothing was added.

## Step 5: Scrub the machine patterns

Remove every match from the banned list, then work through the sentence habits:

1. **Banned vocabulary and dead transitions.** Replace flagged words (*delve*, *leverage*, *utilize*, *tapestry*, *pivotal*, *seamless*) and hollow openers ("In today's...", "It is worth noting", "Let's dive in") with plain, concrete language, or cut them where the sentence stands without them.
2. **Negative parallelisms.** Cut setups like "It is not X, it is Y" or "Less X, more Y". State the positive claim directly.
3. **Rule-of-three padding.** Break up rhythmic three-adjective or three-noun lists ("fast, reliable, and secure") unless three distinct items are factually required.
4. **Indirect copula inflation.** Replace "serves as", "stands as", "represents a" with "is" or "has".
5. **Trailing -ing commentary.** Remove tacked-on participle clauses ("...highlighting the importance of...", "...underscoring the need for...").
6. **Spotlight frames.** Cut "the part that matters", "what really counts is...", and other stage directions that announce importance instead of stating the point.
7. **False ranges.** Rewrite "whether you are X or Y" and "from X to Y" constructions that sweep without saying anything specific.
8. **Em-dash overuse.** Replace em dashes with periods, commas, colons, or parentheses, so pauses read as choices rather than habit.
9. **Flag, do not fix, vague attributions.** "Experts say" and "studies show" with no named source are machine tells, but inventing a source breaks the content lock. Leave the claim as written and note it for the user after the text, or cut it if the claim itself adds nothing the reader needs.

## Step 6: Verify before returning

- Re-read the output against the source, paragraph by paragraph. Every load-bearing fact, number, name, date, condition, and conclusion is still present and unchanged in meaning.
- List your cuts to yourself. Each one passes the cut test: the reader loses nothing they need. Any cut you cannot justify in one line goes back in.
- Confirm no new claim, example, or qualifier appeared.
- Scan once more against the banned list and the Step 5 patterns. A rewrite often introduces a fresh cliché while removing another.
- Confirm protected spans are byte-identical to the source.
- Confirm register and spelling convention match the original.
- Ask Orwell's sixth question of the whole: have I said anything that is avoidably ugly? A fix that makes a sentence stiffer than the fault it cured fails Rule 6. Undo it.
- Final check on length: if the output is about the same length as the input and the input was heavy, look again. Simplicity that cuts nothing is usually a pass that stopped early. If the output is much shorter, check Step 2 again before trusting it.

**Output:** return the edited text only, unless the user asks for a change summary. List any flagged vague attributions briefly after the text.

## Optional: the burstiness pass

Off by default. Run it only when the user asks for it ("add burstiness", "vary the rhythm", or the option switched on where the skill is offered as an app). Sentence splitting and joining are already part of the normal pass. This pass goes further on rhythm alone: it varies sentence openings and paragraph lengths on purpose, even where the plain pass would leave them.

What the pass may do:

- Vary sentence openings so three in a row never share the same grammatical shape.
- Move a sentence break so paragraph lengths vary, from a single sentence to about six.
- Let a short sentence stand alone for weight where the writer's point earns it.

What it still may not do:

- Add a specific detail, example, or number the draft does not contain. Real burstiness comes from real detail. Invented detail is fabrication, not rhythm.
- Reorder paragraphs, change the register, or touch protected spans.
- Bring back a detail the relevance cut removed, or cut a load-bearing fact for rhythm.

Run Steps 3 to 5 first, then this pass, then the Step 6 verification as usual. If the user asks for a change summary, state that the burstiness pass ran.

## Gotchas

- **Cutting the qualifier.** "The treatment may help some patients" cut to "The treatment helps patients" is not simplicity. It is a stronger claim than the writer made. Hedges that change certainty are load-bearing.
- **Cutting the condition.** "If the payment clears, we ship Friday" cut to "We ship Friday" drops the fact the reader most needs. Conditions stay.
- **Relevance without context.** A detail that looks spare in isolation may be the point in the reader's context. When in doubt, keep it. A kept extra detail costs a line. A cut needed detail costs the reader.
- **Over-editing into blandness.** Removing AI jargon does not mean stripping legitimate domain terms. *Semantic layer*, *gradient descent*, and *latency* stay.
- **Summarizing by accident.** If whole points are disappearing, the pass has left editing and become summarizing. Restore the points. Cut only the weight around them.
- **Meaning drift in paraphrase.** Rebuilding a complex sentence can invert cause and effect or drop a qualifier. The Step 6 re-read exists for this.
- **Connector swaps.** Replacing "Moreover" with "Furthermore" at every sentence start still reads like a machine. Logical order first, connectors second.
- **Register drift.** Editing often slides text toward casual. Check formality against the source, not against a generic idea of natural.
- **Stale list.** The banned list changes. Read it fresh on every edit job.
