import express from 'express';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { GoogleGenAI } from '@google/genai';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 8080;
const PROJECT = process.env.GOOGLE_CLOUD_PROJECT || 'banercorp-web';
const MODEL = process.env.GEMINI_MODEL || 'gemini-3.8-flash';
const MAX_WORDS = 3000;

const banned = JSON.parse(fs.readFileSync(path.join(__dirname, 'banned.json'), 'utf8'));
const bannedMd = fs.readFileSync(path.join(__dirname, 'banned-ai-words.md'), 'utf8');

const SYSTEM_INSTRUCTION = `You are Orwell, a tool that rewrites AI-generated English into natural, human-sounding English. You are named for George Orwell, who wrote that good prose is like a windowpane: clear, plain, and easy to see through.

Your one job: change the wording, never the content.

Rules you must follow:
1. Preserve completely: every fact, number, date, name, technical claim, conclusion, hedge, and the author's stance. Never add a claim, an example, or a fact the original does not contain. Never drop one either.
2. Protected spans pass through untouched: direct quotations, code, URLs, file paths, email addresses, citations, and data in tables.
3. Keep the register of the original. A formal text stays formal; a casual text stays casual. Keep roughly the same length and the same paragraph breaks. Keep the spelling convention of the original (US, UK, or other).
4. Remove every banned word, dead transition, and structural pattern in the banned list below. Replace them with plain, concrete words.
5. Break these patterns wherever they appear: negative parallelisms ("it is not X, it is Y") become the positive claim stated directly; rule-of-three lists are cut unless three real items are named; "serves as", "stands as", "represents a" become "is" or "has"; trailing "-ing" commentary clauses ("...highlighting the importance of...") are deleted or turned into their own plain sentence; em dashes become periods, commas, colons, or parentheses.
6. Improve coherence and cohesion: one clear idea per paragraph, known information first and new information next, pronouns and short references instead of repeating the same noun.
7. Improve lexical range: exact verbs instead of vague ones (make, do, get), natural collocations, no filler modifiers (very, really, a lot).
8. Improve grammar and rhythm: mix short and long sentences, check agreement and tense, punctuate cleanly.
9. Keep honest technical terms. Plain English does not mean dumbing down.

Return only the rewritten text. No introduction, no explanation, no summary of changes.

Banned list:
${bannedMd}`;

// ---------- Analysis ----------

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const phraseTerms = [...banned.phrases].sort((a, b) => b.length - a.length);
const wordTerms = [...banned.words].sort((a, b) => b.length - a.length);
const jargonRegex = new RegExp(
  '\\b(?:' + [...phraseTerms, ...wordTerms].map(escapeRegex).join('|') + ')\\b',
  'gi'
);

const SENTENCE_PATTERNS = [
  { name: 'Negative parallelism', re: /\bit'?s not\b[^.!?]{0,90}\bit'?s\b/i },
  { name: 'Negative parallelism', re: /\bnot (just|only|about)\b[^.!?]{0,90}\bbut\b/i },
  { name: 'Negative parallelism', re: /\bnot only\b[^.!?]{0,70}\bbut also\b/i },
  { name: 'Indirect wording ("serves as")', re: /\b(serves as|stands as|represents a|marks a|boasts a|features a)\b/i },
  { name: 'Trailing -ing commentary', re: /,\s+(highlighting|underscoring|showcasing|emphasizing|fostering|paving|ensuring)\b/i },
  { name: 'Spotlight frame', re: /\b(the part that|what really matters|here is the part|the one thing to remember)\b/i },
  { name: 'Dead opener', re: /^\s*(in today'?s|in the ever-evolving|it is worth noting|it is important to note|let'?s dive|at the end of the day|moving forward|in conclusion|to summarize|when it comes to)/i },
];

function splitSentences(text) {
  const out = [];
  const re = /[^.!?]+(?:[.!?]+["')\]]*)?/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const s = m[0];
    if (s.trim().length) out.push({ text: s, start: m.index });
  }
  return out;
}

function countWords(text) {
  const m = text.trim().match(/\S+/g);
  return m ? m.length : 0;
}

function analyze(text) {
  const words = countWords(text);
  const sentences = splitSentences(text);
  const sentenceCount = Math.max(sentences.length, 1);

  // Jargon hits (words and phrases), with per-term counts.
  const termCounts = new Map();
  let jargonHits = 0;
  for (const match of text.matchAll(jargonRegex)) {
    jargonHits += 1;
    const key = match[0].toLowerCase();
    termCounts.set(key, (termCounts.get(key) || 0) + 1);
  }

  // Sentence flags.
  let patternHits = 0;
  let longSentences = 0;
  const annotatedParts = [];
  let cursor = 0;
  for (const s of sentences) {
    if (s.start > cursor) annotatedParts.push(escapeHtml(text.slice(cursor, s.start)));
    const reasons = [];
    for (const p of SENTENCE_PATTERNS) if (p.re.test(s.text)) reasons.push(p.name);
    const sw = countWords(s.text);
    if (sw > 30) { reasons.push('Long sentence (' + sw + ' words)'); longSentences += 1; }
    if (reasons.some((r) => r !== 'Long sentence (' + sw + ' words)')) patternHits += 1;

    let inner = '';
    let last = 0;
    for (const match of s.text.matchAll(jargonRegex)) {
      inner += escapeHtml(s.text.slice(last, match.index));
      inner += '<mark class="jargon" title="AI jargon">' + escapeHtml(match[0]) + '</mark>';
      last = match.index + match[0].length;
    }
    inner += escapeHtml(s.text.slice(last));
    if (reasons.length) {
      annotatedParts.push('<span class="flagged" title="' + escapeHtml(reasons.join('; ')) + '">' + inner + '</span>');
    } else {
      annotatedParts.push(inner);
    }
    cursor = s.start + s.text.length;
  }
  if (cursor < text.length) annotatedParts.push(escapeHtml(text.slice(cursor)));

  const avgLen = words / sentenceCount;
  const jargonPer100 = words ? (jargonHits / words) * 100 : 0;

  let score = 100;
  score -= Math.min(50, jargonPer100 * 7);
  score -= Math.min(25, patternHits * 4);
  score -= Math.min(15, (longSentences / sentenceCount) * 30);
  if (avgLen > 22) score -= Math.min(10, (avgLen - 22) * 0.8);
  score = Math.max(1, Math.min(100, Math.round(score)));

  return {
    score,
    words,
    sentences: sentences.length,
    jargonHits,
    patternHits,
    longSentences,
    avgWordsPerSentence: Math.round(avgLen * 10) / 10,
    topTerms: [...termCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([term, count]) => ({ term, count })),
    annotatedHtml: annotatedParts.join(''),
  };
}

// ---------- Transform ----------

let aiClient = null;
function getClient() {
  if (!aiClient) {
    aiClient = new GoogleGenAI({ vertexai: true, project: PROJECT, location: 'global' });
  }
  return aiClient;
}

async function transform(text) {
  const ai = getClient();
  const resp = await ai.models.generateContent({
    model: MODEL,
    contents: text,
    config: { systemInstruction: SYSTEM_INSTRUCTION, temperature: 0.3, maxOutputTokens: 8192 },
  });
  return (resp.text || '').trim();
}

// ---------- Server ----------

const app = express();
app.use(express.json({ limit: '1mb' }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/health', (_req, res) => res.json({ ok: true }));

app.post('/api/orwell', async (req, res) => {
  const text = typeof req.body?.text === 'string' ? req.body.text : '';
  if (!text.trim()) return res.status(400).json({ error: 'Paste some text first.' });
  const words = countWords(text);
  if (words > MAX_WORDS) {
    return res.status(400).json({ error: 'That is ' + words + ' words. The limit is ' + MAX_WORDS + ' words.' });
  }
  const analysis = analyze(text);
  try {
    const transformed = await transform(text);
    if (!transformed) throw new Error('Empty response from the model.');
    res.json({ analysis, transformed });
  } catch (err) {
    console.error('Transform failed:', err?.message || err);
    res.status(502).json({ analysis, transformed: null, error: 'The rewrite failed just now. Your rating and highlights are ready; please try the rewrite again.' });
  }
});

app.listen(PORT, () => console.log('Orwell listening on port ' + PORT));
