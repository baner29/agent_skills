---
name: orwell
description: Transforms AI-generated text into natural, human-sounding English by removing AI jargon, structural clichés, and banned vocabulary while strictly preserving facts, meaning, intent, and register. Use when a user asks to humanize, naturalize, de-AI, rewrite, or polish an AI-generated draft, article, email, or essay, judged on Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy. This skill removes machine patterns only; it does not impose a personal voice. When the user also has a personal writing-style skill or guide, apply this skill first and let the personal style win on any conflict.
---

# Orwell

> "Good prose is like a windowpane."
> — George Orwell, *Why I Write* (1946)

Named for George Orwell, who argued that clear language and clear thinking are the same discipline. This skill transforms AI-generated prose into clear, natural English by eliminating synthetic phrasing and applying proven linguistic standards for Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy. Preserve every fact, argument, and core meaning of the original text without altering its substance.

## What this skill is not

- It is not a personal style skill. It does not give the text a personality, a persona, opinions, or a point of view the author did not already express. It removes the machine's patterns and leaves the author's.
- It is not a fact-checker or an editor of arguments. Weak reasoning stays weak; the job is to make it read naturally, not to fix the thinking.
- It does not restructure a document. Paragraph order, headings, and the author's chosen structure stay unless the user asks for restructuring.

## When to use

- The user asks to humanize, naturalize, de-AI, rewrite, or polish text that an AI generated or helped generate.
- The user wants AI buzzwords, repetitive sentence structures, and filler transitions stripped from a draft without changing what the text says.
- The user wants new banned AI words or patterns added to the standing watchlist based on their edits or feedback.
- When drafting new prose from scratch, this skill may be applied as a final pass over the draft. It is not a substitute for the user's own style guidance while drafting.

## Steps

### Step 1: Lock the content invariant

Before editing a single word, separate **substance** from **expression**:

- **Preserve completely:** all facts, numbers, dates, named entities, technical claims, logical conclusions, hedges and qualifiers, and the author's intended stance.
- **Edit exclusively:** word choice, paraphrasing, sentence structure, paragraph transitions, grammar, and punctuation.
- Never invent new examples, add external claims, or soften an explicit conclusion to sound "balanced."
- **Protected spans — copy through untouched:** direct quotations, code and code blocks, URLs and file paths, email addresses, citations, and data inside tables. A naturalizer that rewrites a quote or a link has corrupted the content.
- **Preserve the register:** match the original's level of formality and its audience. A casual email stays casual; an academic abstract stays formal. Natural does not mean informal.
- **Preserve length and shape:** keep the paragraph count and roughly the original length. Naturalizing is not summarizing and not expanding.
- **Preserve the spelling convention** already in the text (US, UK, or other). Do not convert dialects.

### Step 2: Scrub AI patterns and banned vocabulary

Read [references/banned-ai-words.md](references/banned-ai-words.md) in this skill directory and remove every matching word, transition, and structural pattern from the draft:

1. **Delete banned vocabulary and dead transitions:** replace flagged AI buzzwords (such as *delve*, *leverage*, *utilize*, *tapestry*, *pivotal*, *seamless*) and hollow openers (*"In today's..."*, *"It is worth noting"*, *"Let's dive in"*) with plain, concrete language.
2. **Eliminate synthetic rhetorical patterns:**
   - **Negative parallelisms:** cut setups like *"It is not X, it is Y"* or *"Less X, more Y"* and state the positive claim directly.
   - **Rule-of-three triplets:** break up rhythmic three-adjective or three-noun lists (*"fast, reliable, and secure"*) unless three distinct items are factually required.
   - **Indirect copula inflation:** replace *"serves as"*, *"stands as"*, or *"represents a"* with direct verbs like *"is"* or *"has"*.
   - **Trailing `-ing` commentary:** remove tacked-on participle clauses (*"...highlighting the importance of..."*, *"...underscoring the need for..."*).
   - **Spotlight frames:** cut *"the part that matters"*, *"what really counts is..."*, and similar stage directions that announce importance instead of stating the point.
   - **False ranges and pairings:** rewrite *"whether you are X or Y"* and *"from X to Y"* constructions that sweep without saying anything specific.
   - **Em-dash overuse:** replace em dashes with periods, commas, colons, or parentheses so pauses feel deliberate rather than formulaic.
3. **Flag, do not fix, vague attributions:** claims like *"experts say"* or *"studies show"* with no named source are an AI tell, but inventing a source would break the content invariant. Leave the claim as written and note it for the user.

### Step 3: Elevate through the three linguistic pillars

Refine the scrubbed draft across the three core pillars of natural English:

1. **Coherence and Cohesion:**
   - Keep each paragraph focused on one clear central idea introduced by its opening sentence.
   - Flow from known information at the end of one sentence to new information at the start of the next.
   - Replace mechanical noun repetition with natural reference and substitution (*this approach*, *such systems*, *the shift*, *they*).
   - Use unobtrusive discourse markers (*however*, *consequently*, *meanwhile*, *granted*) only where the logical link is not already obvious.

2. **Lexical Resource:**
   - Vary recurring nouns, verbs, and adjectives within a paragraph using contextually accurate synonyms.
   - Replace vague, all-purpose verbs (*make*, *do*, *get*, *fix*) and filler modifiers (*very*, *really*, *a lot*) with exact verbs and specific qualifiers.
   - Use natural collocations (words that native speakers pair effortlessly, such as *commit an error* rather than *do a mistake*) and verify exact word forms.

3. **Grammatical Range and Accuracy:**
   - Vary sentence length and rhythm by mixing short declarative sentences with compound and complex structures.
   - Check subject-verb agreement, tense consistency, parallel list structure, and modifier placement across multi-clause sentences.
   - Apply punctuation accurately (commas for non-restrictive clauses, semicolons for closely linked independent clauses, colons for explanations).

#### Example transformation

- **Before (AI-generated):**
  *"In today's fast-paced digital landscape, organizations must leverage cutting-edge cloud solutions to unlock seamless scalability. It is not just about reducing hardware costs; it is about fostering an innovative, resilient, and agile ecosystem — ultimately underscoring the pivotal role of modern infrastructure."*

- **After (naturalized):**
  *"Organizations now use modern cloud platforms to scale capacity up or down as demand changes, without buying hardware up front. Lower hardware costs are only part of the gain; the systems also hold up under load and adapt as needs change. Modern infrastructure sits at the center of how organizations run."*

  Every claim in the original survives: scaling, reduced hardware costs, resilience, adaptability, and the central role of infrastructure. Nothing was added. If a rewrite needs a fact the original does not contain, the rewrite is wrong.

### Step 4: Maintain the living banned-words list

Keep [references/banned-ai-words.md](references/banned-ai-words.md) current over time:

- **Manual updates:** when the user asks to ban or allow specific words or phrases, update the file directly and confirm the change.
- **Agent learning:** when the user edits a naturalized draft and repeatedly removes or flags a specific word, transition, or phrasing pattern as "sounding like AI," propose adding it to the Custom User Additions section. Add it only after the user confirms, unless the user has explicitly told the agent to learn from edits without asking.
- **Format and hygiene:** each addition records the term and a plain-English alternative. Check for duplicates and inflected variants (for example *delve*, *delving*, *delved*) before adding; matching is case-insensitive and covers those variants.

### Step 5: Verify before returning

Run this pass on every naturalized text before handing it back:

- Re-read the output against the source, paragraph by paragraph. Every number, name, date, and claim in the source is still present and unchanged in meaning.
- Confirm no new claim, example, or qualifier appeared, and none was dropped.
- Scan once more for the banned list and the Step 2 patterns; a rewrite often introduces a fresh cliché while removing another.
- Confirm protected spans (quotes, code, URLs, tables) are byte-identical to the source.
- Confirm the register and spelling convention match the original.

**Output:** return the naturalized text only, unless the user asks for a change summary. If vague attributions were flagged in Step 2, list them briefly after the text.

## Gotchas

- **Over-editing into blandness:** removing AI jargon does not mean stripping out legitimate domain terminology. Keep precise technical nouns (for example, *semantic layer*, *gradient descent*, *latency*) intact.
- **Changing the meaning while paraphrasing:** rewriting a complex sentence can accidentally invert cause and effect or drop a qualifier. Re-read the output against the source paragraph to verify every claim still holds.
- **Overusing transitional adverbs:** replacing *"Moreover"* with *"Furthermore"* at the start of every sentence still reads like a machine. Rely on logical sentence order first and connectors second.
- **Register drift:** naturalizing often slides text toward casual. Check the output's formality against the source, not against a generic idea of "natural."
- **Tampering with quotes and code:** quoted speech, code, and data are content, not expression. Leave them exactly as they are, even when they contain a banned word.
- **Forgetting to check the reference file:** always read [references/banned-ai-words.md](references/banned-ai-words.md) before editing so newly added terms are enforced.
