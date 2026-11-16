---
name: orwell
description: The last pass over a finished draft. Turns AI-generated or AI-assisted text into simple, plain English by removing machine words, needless complexity, and details that add nothing in context, while keeping every point the reader needs. Sentences may be rebuilt, split, joined, or cut when that makes the text clearer. Use when a user asks to humanize, naturalize, de-AI, clean up, simplify, shorten, or polish a draft, article, email, or essay as a final refinement, to scan a text for AI patterns without rewriting it, or to add words and patterns to the banned list. When the user also has a personal writing-style skill or guide, apply this skill first and let the personal style win on any conflict.
---

# Orwell

> "Good prose is like a windowpane."
> — George Orwell, *Why I Write* (1946)

Orwell is the last mile of writing refinement. The draft is finished and the writer's point is settled. What remains is weight the reader does not need: machine words, long constructions where a short one says the same thing, and details that may be true but add nothing in the context where the text will be read. Orwell removes that weight. It keeps the point, the facts the reader needs, and the writer's voice.

A man at a food counter is asked if he wants anything added or removed. "Yes, no tomatoes, please" is complete. "Yes, no tomatoes, please, as I do not like tomatoes" adds a true fact that changes nothing. The counter staff do not need his reason to act. Orwell cuts the second kind of detail and keeps the first.

## The simplicity rule

- Run this skill last, after the writer's own tools and instructions.
- Keep things simple. Prefer the shortest clear form that carries the writer's point.
- Sentence structure is open to edit. Split a long sentence, join two short ones, rebuild a tangled one, reorder clauses inside a sentence, or cut a sentence that adds nothing. Structure serves clarity now. It is not protected.
- Paragraph order, headings, and the order of the argument stay as the writer left them, unless the user asks for restructuring. Cutting a detail inside the argument is an edit. Rebuilding the argument is a different job.
- The writer's voice wins every tie. When two simple versions read equally well, keep the one closer to the original.

## First, read the context

Before editing, settle three things from the text and the conversation around it:

1. **Purpose.** What is this text trying to do? Inform, ask, decide, instruct, persuade, report, or reply?
2. **Reader.** Who will read it, what do they already know, and what do they need to do or understand after reading it?
3. **Point.** What is the one point each paragraph makes?

When the context is unclear, be careful. Cut only what is plainly filler, repetition, or machine habit. Keep any detail that might carry weight for a reader you cannot identify.

## What stays, what goes

**Keep:**

- The writer's main point, stance, and conclusions.
- Facts, numbers, dates, and names the reader needs to act, decide, judge, or understand the point.
- Conditions, limits, risks, causes, and evidence that change what the point means.
- Hedges and qualifiers that change how certain a claim is.
- Protected spans, copied through byte for byte: quotations, code, URLs, file paths, email addresses, citations, and data in tables.
- Register and spelling convention. A formal report stays formal. US spelling stays US.

**Cut:**

- Details that are true but add nothing in this context: reasons, motives, background, or personal preferences the reader does not need and did not ask for.
- Restatements of the question, the previous sentence, or the obvious.
- Clauses that answer a question nobody in this context is asking.
- Background that does not change the action, the decision, or the reader's understanding of the point.
- Polite filler, throat-clearing, and scene-setting that delays the point.
- A second example that proves the same point the first example already proved, unless the writer is building a list on purpose.

**The cut test.** For each clause, detail, and sentence, ask: if this goes, does the reader lose anything they need to act, decide, judge, or understand the point? If no, cut it. If yes, keep it. If unsure, keep it and, in an app or chat where notes are allowed, flag it after the text.

Vague attributions ("experts say", "studies show") are flagged for the user, never fixed by inventing a source. A vague attribution that carries no claim the reader needs may be cut with the sentence around it.

## Orwell's six rules

From *Politics and the English Language* (1946):

1. Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
2. Never use a long word where a short one will do.
3. If it is possible to cut a word out, always cut it out.
4. Never use the passive where you can use the active.
5. Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
6. Break any of these rules sooner than say anything outright barbarous.

Rule 3 now applies to clauses and details as well as single words. Rule 6 governs the other five. The rules serve the sentence, never the reverse. Read references/orwell-judgment.md before bending one.

## The six questions

Orwell held that a scrupulous writer asks of every sentence:

1. What am I trying to say?
2. What words will express it?
3. What image or idiom will make it clearer?
4. Is this image fresh enough to have an effect?
5. Could I put it more shortly?
6. Have I said anything that is avoidably ugly?

Add one question in front of his six: does this sentence, or this part of it, need to be here at all in this context? A sentence that earns its place gets the smallest clear form. A sentence that does not earn its place is cut, however well it is written.

## Modes

Load only the file the job needs.

| Job | Load |
| --- | --- |
| Edit a text (the default) | references/edit.md, plus references/banned-ai-words.md |
| Edit with varied rhythm (the burstiness pass, only when the user asks for it) | references/edit.md, the burstiness section |
| Scan a text and report its AI patterns, without rewriting it | references/scan.md |
| Add or remove banned words and patterns | references/learn.md |
| A rule and the sentence seem to pull apart | references/orwell-judgment.md |
| Background on the research behind the rules | references/orwell-research.md |

Where a shell is available, run scripts/scan.py on the text first. It applies the banned list mechanically, at no reading cost, and reports sentence statistics. Judgment stays with you. Counting does not need it.

## What this skill is not

- Not a personal style. It gives the text no personality, opinions, or point of view of its own. It removes weight and leaves the writer's point and voice.
- Not a summary tool. It does not compress a text to a target length or drop points to save space. It cuts only what adds nothing in context.
- Not an editor of arguments. Weak reasoning stays weak. If a needed fact is missing, flag the gap. Do not invent it and do not hide it by cutting the claim.
- Not a drafting tool. It refines finished text. The generation-side craft in the research sits in references/orwell-research.md and stays out of the edit path.
