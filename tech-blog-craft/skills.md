---
name: tech-blog-craft
description: >-
  Guides the writing of human, first-person, narrative-driven technical blog posts
  and case studies about any software, hardware, or engineering project. Use when the user
  asks to write a blog post, article, or technical story about a codebase or architecture,
  ensuring it avoids preachy lecturing and AI-writing markers.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: "technical-writing"
  tags: "blogging,engineering,storytelling,clarity,anti-ai,human-voice"
---

# Tech Blog Craft

A universal skill for writing technical blogs that sound like an authentic practitioner sharing lessons from the trenches. It turns technical decisions into an engaging human story across any tech stack—web applications, mobile apps, systems programming, backend architectures, developer tooling, or cloud platforms.

---

## 1. The Human Practitioner Voice

### The "First-Person" Principle
* **Anchor in the Author's Experience**: Speak primarily in the first person (`I`, `we`, `my team`, `our users`). The narrative must feel like personal testimony, not a textbook or user manual.
* **Eliminate Preachy Second-Person Lecturing**: Avoid wagging a finger at the reader with `you must`, `you should`, or `you need to understand`. Replace instructions with personal realizations:
  * *Instead of*: "You must never store state in container memory because Cloud Run will wipe it."
  * *Write*: "I quickly learned that storing state in container memory was a mistake—the moment our instances recycled, user sessions vanished."
* **Humility over Authority**: Present solutions as hard-earned answers to specific problems and constraints, not as universal dogmas. Acknowledge what didn't work and what surprised you.

---

## 2. The Core Narrative Arc

Every compelling technical blog post follows a four-part journey:

1. **The Hook (Theory vs. Practice)**:
   Start with the initial expectation, tutorial promise, or naive assumption, and describe the exact moment it failed when tested against real-world reality.
2. **The Non-Negotiable Constraint**:
   Identify the primary pressure that forced the architecture to be designed the way it is:
   * *Web Frontend*: Core Web Vitals, hydration lag, bundle size, cross-browser rendering, SEO hydration.
   * *Mobile (Android / iOS)*: Background OS kills, battery life, screen fragmentation, configuration changes.
   * *Backend & Distributed Systems*: Race conditions, database lock contention, network latency, partition tolerance.
   * *Enterprise & Cloud*: Compliance audits (SOC 2, ISO, OneTrust), procurement delays, zero-trust security, stateless scaling.
3. **The Design & Trade-offs**:
   Walk through the actual architecture. Show *why* components are arranged as they are. Explain what alternative designs were rejected and what trade-offs were consciously accepted. (Good engineering is picking trade-offs you can live with).
4. **The Battle Scar**:
   Include at least one specific, hard-won debugging moment: a subtle race condition, an unexpected runtime error, an undocumented API quirk, or an async garbage collection bug. Authentic war stories build immediate credibility.
5. **The Takeaway / Relief**:
   Close on the concrete relief or operational benefit of the chosen design. Frame advice humbly as a pattern worth considering for peers facing similar constraints.

---

## 3. Project-Agnostic Context Discovery

Before drafting, extract the factual core of the project. If working in a workspace, inspect the repository; if given prompt notes, extract these key details:

1. **Project Mission**: What does this project do in plain language? What is its core responsibility?
2. **The Stack & Boundaries**: What languages, frameworks, runtime environments, and external systems are involved?
3. **The Problem It Solves**: Why wasn't the standard or simplest approach good enough?
4. **Key Technical Decisions**: What are the 2 or 3 defining structural choices in the code?
5. **The Relief**: How does this save time, prevent bugs, or simplify life for the author and their users?

---

## 4. Anti-AI Writing Invariants (Strict Guardrails)

Adhere strictly to human writing standards and eliminate markers identified in *Wikipedia: Signs of AI Writing* and Clarity guidelines:

* **Zero AI Vocabulary**: Never use:
  * *delve, tapestry, landscape, pivotal, testament, crucial, robust, seamless, beacon, foster, enhance, bolster, overarching, multifaceted, notably, cornerstone, align with, resonate with*.
* **No Robotic Copulative Evasion**:
  * Avoid replacing simple verbs with high-sounding phrases like *serves as a bridge*, *acts as a mechanism*, or *stands as a testament*. Use direct verbs: *is*, *handles*, *routes*, *stores*.
* **No Participial Tails**:
  * Ban trailing `-ing` clauses tacked onto the end of sentences to simulate analytical depth (*"...thereby ensuring optimal performance", "...highlighting its critical importance"*). State the actor and the concrete mechanism directly.
* **No Canned Transitions**:
  * Ban formulaic transition words: *Moreover, Furthermore, In conclusion, Ultimately, Looking ahead, At its core, It is important to note*.
* **No Formulaic Symmetry**:
  * Avoid negative parallelisms (*not only X, but also Y* or *not X, but Y*).
  * Avoid the rhythmic "Rule of Three" (*scalable, fast, and secure*). Vary your cadences naturally.
* **No Bold-Lead Bullet Dumps**:
  * Avoid repetitive `**Feature Name**: Description` list formatting. Write connected, explanatory prose that flows naturally.
* **Natural Texture & Contractions**:
  * Use conversational contractions (*it's, didn't, wasn't, can't, we'd*).
  * Use limited, natural phonological reductions (*gonna, kinda, 'em*) where it fits an informal, authentic engineering storytelling rhythm.

---

## 5. Pre-Publish Audit Checklist

Review the draft against this checklist before finishing:

- [ ] **First-Person Authenticity**: Is the post told from the author's point of view (`I` / `we`) without finger-pointing `you` lectures?
- [ ] **Grounded Constraints**: Does it clearly explain the real-world pressures (performance, lifecycle, security, or compliance) that dictated the design?
- [ ] **No AI Tells**: Are all banned AI buzzwords, canned transitions, and trailing participial clauses completely absent?
- [ ] **Real Engineering Texture**: Is there at least one specific technical trade-off, war story, or concrete code mechanism discussed?
- [ ] **Natural Ending**: Does the post stop cleanly on the last useful technical thought, rather than fading into a generic motivational conclusion?
