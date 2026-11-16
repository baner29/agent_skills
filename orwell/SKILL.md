---
name: orwell
description: The last pass over a finished draft. Turns AI-generated or AI-assisted text into natural, plain English with the smallest changes that clear the fault, removing AI jargon, dead phrases, and machine sentence habits while preserving facts, meaning, structure, register, and the writer's voice. Use when a user asks to humanize, naturalize, de-AI, clean up, or polish a draft, article, email, or essay as a final refinement, to scan a text for AI patterns without rewriting it, or to add words and patterns to the banned list. When the user also has a personal writing-style skill or guide, apply this skill first and let the personal style win on any conflict.
---

# Orwell

> "Good prose is like a windowpane."
> — George Orwell, *Why I Write* (1946)

Orwell is the last mile of writing refinement. The draft is finished. The argument is settled, the structure is the writer's own, and other tools have done their work. What remains is the machine residue: stock words, ready-made phrases, and sentence habits that mark a text as generated. Orwell removes that residue and nothing else, editing the way George Orwell said a writer should: with short words, concrete claims, and no ornament.

## The last-mile rule

- Run this skill last, after the writer's own tools and instructions.
- Make the smallest change that clears the fault. If a word is wrong, change the word. Do not rebuild the sentence around it.
- Structure is out of bounds: paragraph order, headings, length, and shape stay as the writer left them. If the structure itself is the problem, say so and stop. Fixing structure is a different job.
- The writer's voice wins every tie. When two plain versions read equally well, keep the one closer to the original.

## What never changes

- Facts, numbers, dates, names, claims, hedges, and the writer's stance.
- Protected spans, copied through byte for byte: quotations, code, URLs, file paths, email addresses, citations, and data in tables.
- Register and spelling convention. A formal report stays formal. US spelling stays US.
- Vague attributions ("experts say", "studies show") are flagged for the user, never fixed by inventing a source.

## Orwell's six rules

From *Politics and the English Language* (1946):

1. Never use a metaphor, simile, or other figure of speech which you are used to seeing in print.
2. Never use a long word where a short one will do.
3. If it is possible to cut a word out, always cut it out.
4. Never use the passive where you can use the active.
5. Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.
6. Break any of these rules sooner than say anything outright barbarous.

Rule 6 governs the other five. The rules serve the sentence, never the reverse. Read references/orwell-judgment.md before bending one.

## The six questions

Orwell held that a scrupulous writer asks of every sentence:

1. What am I trying to say?
2. What words will express it?
3. What image or idiom will make it clearer?
4. Is this image fresh enough to have an effect?
5. Could I put it more shortly?
6. Have I said anything that is avoidably ugly?

In an edit, ask them of the writer's sentences. A sentence that fails a question earns the smallest fix that makes it pass.

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

- Not a personal style. It gives the text no personality, opinions, or point of view of its own. It removes the machine's patterns and leaves the writer's.
- Not an editor of arguments. Weak reasoning stays weak. The job is the wording.
- Not a drafting tool. It refines finished text. The generation-side craft in the research sits in references/orwell-research.md and stays out of the edit path.
