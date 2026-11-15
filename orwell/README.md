![Orwell](poster.png)

# Orwell

> "Good prose is like a windowpane."
> — George Orwell, *Why I Write* (1946)

**Try it live:** [orwell.banerworks.com](https://orwell.banerworks.com)

## The idea

AI writes in a fog. Ask a machine for a paragraph and you get words like "leverage", "delve", and "seamless", sentences that begin with "In today's fast-paced world", and claims dressed up to sound bigger than they are. People do not talk this way. Readers feel the fog at once, even when they cannot name it, and they trust the text less.

George Orwell spent his career fighting this kind of language. His rule was simple: never use a long word where a short one will do, and never use a foreign or technical phrase when a plain English one says the same thing. Good prose, he wrote, is like a windowpane. You look through it and see the meaning. You do not stop to admire the glass.

Orwell is an agent skill built on that idea. You give it text that an AI produced. It takes out the machine words and the machine habits, fixes the grammar, and joins the sentences so they read in a natural order. Then it gives the text back. The facts stay where they were. The meaning stays the same. The writer's tone stays the same. Only the wording changes, and it changes toward short, plain, honest English that any reader can follow on the first pass.

## What it does

- It reads your text against a list of banned words and phrases, the ones machines reach for again and again, and swaps each one for a plain word.
- It breaks the habits that give machine writing away: sentences built as "it is not X, it is Y", lists of three adjectives where one would do, verbs hidden inside phrases like "serves as", and clauses tacked on the end of a sentence to make it sound grand.
- It tidies the language itself: one clear idea per paragraph, sentences in an order the reader can follow, exact verbs in place of vague ones, and a mix of short and long sentences so the text has a natural rhythm.
- It rates nothing and judges nothing about your ideas. Weak reasoning stays weak. The skill cleans the glass. It does not change the view.

## What it never does

- It never adds a fact, an example, or a claim that your text did not already make.
- It never drops a fact to make a sentence smoother.
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
- "Tidy this essay so the sentences flow and the grammar is sound, and change nothing it says."

The agent hands back the cleaned text on its own, unless you ask for a list of what changed.

## How it works

1. **The meaning is locked first.** Before a single word is touched, the agent sets aside everything that must not change: facts, numbers, dates, names, claims, quotes, code, and links. Only wording, sentence shape, and grammar are open to edit.
2. **The machine words come out.** The agent reads the banned list in `references/banned-ai-words.md` and removes every match, along with the sentence patterns listed above. If your text credits a claim to "experts" or "studies" without naming one, the agent points at it and tells you. It will not invent a source to fill the gap.
3. **The language is put in order.** Sentences are joined so each one follows from the last. Repeated nouns give way to short references. Vague verbs are swapped for exact ones. Sentence lengths are varied, and grammar and punctuation are checked line by line.
4. **The banned list keeps growing.** The list is yours to edit at any time. When you cross the same word out of draft after draft, the agent can suggest adding it. It adds the word only when you say yes, unless you have told it to learn from your edits on its own.
5. **The result is checked against the source.** The agent reads the cleaned text side by side with yours, paragraph by paragraph. Every claim must still be there, nothing new may appear, and quotes and code must match letter for letter. If the rewrite picked up a fresh cliché on the way, it comes out before you see the text.

## The banned list

The list lives in `references/banned-ai-words.md`. It has three parts: single words, set phrases and sentence openers, and sentence patterns. A fourth part is left empty for your own additions. Write each addition as the term, plus the plain word you would rather see. Matching ignores capital letters and covers the word's other forms, so "delve" also catches "delving" and "delved".

A word on the list is a word to question, not always a word to cut. If a term is the exact, correct word in a technical text, it stays. The list exists so the choice is made by a person, on purpose, and not by a machine, by habit.

## Using Orwell with a personal style guide

Orwell works well next to a personal style guide, and the two do different jobs. Run Orwell first to strip out the machine habits. Then run your own guide to give the text your voice. If the two ever disagree, your guide wins.

## Files

| File | What it is |
| --- | --- |
| `SKILL.md` | The skill itself: when to use it, the five steps, and the traps to avoid |
| `references/banned-ai-words.md` | The banned list, kept open for edits and additions |
| `poster.png` | The title poster |
| `app/` | A small web app that runs Orwell in the browser, with the jargon marked and the original rated out of 100 |
