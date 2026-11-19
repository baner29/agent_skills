# Learn mode: keep the banned list alive

The list at references/banned-ai-words.md is a living file. This mode covers every change to it.

## Direct requests

When the user asks to ban or allow a word, phrase, or pattern, make the change at once and confirm it in one line. Bans go to the Custom User Additions section unless the term plainly belongs in an existing category of sections 1 to 3. Removals come out of whichever section holds them.

## Proposals from the agent

When the user edits an edited draft and repeatedly removes or flags the same word, transition, or phrasing as sounding like AI, propose adding it to the list. State the term, the plain alternative, and the evidence (how often it was flagged). Add it only after the user confirms.

Silent learning, adding terms without asking, applies only when the user has explicitly switched it on. It stays off by default, and it switches off again the moment the user questions an addition.

## Format and hygiene

- Each entry records the term and a preferred plain-English alternative.
- Check for duplicates and inflected variants before adding. Matching is case-insensitive and covers inflections: *delve* already covers *delving* and *delved*.
- Keep entries in the style of their section: single words with the vocabulary, quoted phrases with the transitions, named patterns with the clichés.
- scripts/scan.py reads the list file at run time, so a list change needs no code change.

## What learning is not

- One flagged word in one draft is an edit, not a rule. Propose only on repetition or on a direct request.
- A word the user merely dislikes in one context is not banned. The list records machine tells, not taste.
- Never learn from text the user pasted for editing alone. The signal is the user's own edits and flags, not the contents of their drafts.
