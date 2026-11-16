![Orwell](poster.png)

# Orwell

> "Good prose is like a windowpane."
> — George Orwell, *Why I Write* (1946)

**Try it live:** [orwell.banerworks.com](https://orwell.banerworks.com)

## About this repository

AI writing sounds like AI writing, and readers spot it in a line or two. This skill takes that sound out: give it a paragraph an AI wrote for you, and it hands the paragraph back in plain, simple English, shorter where the original carried weight the reader did not need. Ask a machine for a paragraph and you get words like "leverage", "delve", and "seamless", sentences that begin with "In today's fast-paced world", and claims dressed up to sound bigger than they are. People do not talk this way. A reader who spots the machine in your text trusts it less, even when they cannot say why.

George Orwell spent his career fighting this kind of language. His rule was simple: never use a long word where a short one will do, and never use a foreign or technical phrase when a plain English one says the same thing. Good prose, he wrote, is like a windowpane. You look through it and see the meaning. You do not stop to admire the glass. The rule still does its work on today's drafts. A sentence like "Our team will leverage cutting-edge solutions to streamline your workflow and unlock valuable insights" comes back as "Our team will use modern tools to simplify your workflow and find valuable insights." The claim is the same. The words now sound like a person wrote them.

Orwell is an agent skill built on that idea. Its job is narrow, and it stays narrow: it keeps your point and cuts the weight around it. You give it text that an AI produced. It takes out the machine words and the machine habits, rebuilds sentences that tangle, and cuts details that add nothing in the context where the text will be read. Then it gives the text back. The point stays the same. Every fact the reader needs stays. The writer's tone stays the same. What goes is the wording and detail a reader never needed, so what is left is short, plain, honest English that any reader can follow on the first pass.

The cut is judged in context. A customer at a food counter, asked what to add or remove, might write: "Yes, please remove the tomatoes, as I do not like tomatoes." Orwell returns: "Yes, no tomatoes, please." The worker needs the instruction, not the reason. In a review or a recipe note, the same reason is part of the point, and it stays.

## What it does

- It reads your text against a list of banned words and phrases, the ones machines reach for again and again, and swaps each one for a plain word.
- It breaks the habits that give machine writing away: sentences built as "it is not X, it is Y", lists of three adjectives where one would do, verbs hidden inside phrases like "serves as", and clauses tacked on the end of a sentence to make it sound grand.
- It cuts what adds nothing in context: reasons and background the reader does not need, points stated twice, and clauses that answer a question nobody asked.
- It rebuilds tangled sentences: long sentences are split, noun piles become verbs, and each idea lands once, in the order the reader needs it.
- It rates nothing and judges nothing about your ideas. Weak reasoning stays weak. The skill cleans the glass. It does not change the view.

## What it never does

- It never adds a fact, an example, or a claim that your text did not already make.
- It never drops a fact the reader needs: a number, a condition, a risk, a cause, or a hedge that changes how certain a claim is.
- It never cuts a point to save space. It is not a summary tool. It cuts only what adds nothing in context.
- It never touches quotes, code, links, or tables. Those pass through word for word.
- It never gives your text a personality it did not have. A formal report stays formal. A casual email stays casual. This skill is not a personal style guide. It removes the machine's habits and leaves the writer's.

## Installation

Install with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add baner29/agent_skills --skill orwell
```

Or copy the `orwell` folder into your agent's skills folder by hand. The skill is a plain `SKILL.md` package and works with any agent that reads the Agent Skills format.

## Usage

Ask your agent to clean up any draft an AI helped write:

- "Run this article through Orwell before I publish it."
- "Make this email sound human. Keep every fact and keep the formal tone."
- "Clean up this draft, and add 'synergize' to the banned list."
- "Tidy this essay so the sentences flow and the grammar is sound, and keep its point and every fact I need."
- "Tell me what makes this draft sound like AI. Change nothing yet."

The agent hands back the cleaned text on its own, unless you ask for a list of what changed.

## How it works

1. **The context is read first.** Before a single word is touched, the agent settles what the text must do, who will read it, and what each paragraph's point is. Every later cut is judged against that context.
2. **What must stay is locked.** The agent sets aside everything load-bearing: the point, the facts, numbers, dates, names, conditions, and claims the reader needs, plus quotes, code, and links, which pass through untouched.
3. **The weight comes out.** Details that add nothing in context are cut. The machine words come out too: the agent reads the banned list in `references/banned-ai-words.md` and removes every match, along with the sentence patterns listed above. If your text credits a claim to "experts" or "studies" without naming one, the agent points at it and tells you. It will not invent a source to fill the gap.
4. **The language is put in order.** Tangled sentences are rebuilt or split. Repeated nouns give way to short references. Vague verbs are swapped for exact ones, and grammar and punctuation are checked line by line.
5. **The banned list keeps growing.** The list is yours to edit at any time. When you cross the same word out of draft after draft, the agent can suggest adding it. It adds the word only when you say yes, unless you have told it to learn from your edits on its own.
6. **The result is checked against the source.** The agent reads the cleaned text side by side with yours, paragraph by paragraph. Every needed claim must still be there, each cut must pass the test that the reader loses nothing they need, nothing new may appear, and quotes and code must match letter for letter. If the rewrite picked up a fresh cliché on the way, it comes out before you see the text.

That is the full pass, and it is the last step of a writing process, not the first: run it when the draft is finished and your own tools have done their work. The skill also works in a smaller way. Ask for a scan and it reports the machine patterns in a text without changing a word. The counting half of the check can run as a script (`scripts/scan.py`), so the agent spends its attention on judgment instead of counting.

## The banned list

The list lives in `references/banned-ai-words.md`. It has three parts: single words, set phrases and sentence openers, and sentence patterns. A fourth part is left empty for your own additions. Write each addition as the term, plus the plain word you would rather see. Matching ignores capital letters and covers the word's other forms, so "delve" also catches "delving" and "delved".

A word on the list is a word to question, not always a word to cut. If a term is the exact, correct word in a technical text, it stays. The list exists so the choice is made by a person, on purpose, and not by a machine, by habit.

## Using Orwell with a personal style guide

Orwell works well next to a personal style guide, and the two do different jobs. Run Orwell first to strip out the machine habits. Then run your own guide to give the text your voice. If the two ever disagree, your guide wins.

## Files

| File | What it is |
| --- | --- |
| `SKILL.md` | The core: the simplicity rule, the cut test, Orwell's six rules and six questions, and the map to the files below |
| `references/edit.md` | The full pass, step by step |
| `references/scan.md` | How to report a text's machine patterns without rewriting it |
| `references/learn.md` | How the banned list grows and stays clean |
| `references/orwell-judgment.md` | When a rule should bend, in Orwell's own practice, with worked examples |
| `references/orwell-research.md` | The scholarship behind the rules, kept as background |
| `references/banned-ai-words.md` | The banned list, kept open for edits and additions |
| `scripts/scan.py` | A script that applies the banned list and counts sentences, so the agent judges instead of counting |
| `poster.png` | The title poster |
