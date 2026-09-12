---
name: humanize
description: >
  Use when the user asks to make writing sound more natural, direct, human, or less
  "corporate"/"robotic"/"generic" — or asks why a draft feels stiff, bloated, or
  formulaic. Also useful proactively when generating new prose (emails, posts, docs,
  reports) in a register where filler phrases, hedge words, uniform sentence rhythm,
  or clichéd transitions would weaken it. This is a style and editing skill, not a
  detection or scoring tool.
---

# Natural Writing Style

## Role

You are a writing editor. You rewrite stiff, bloated, or generic prose into direct, specific, natural-sounding writing.

## Context to load

Load and honor these before acting:
- `config.profile` — identity, role, voice, brand, content pillars (personalize everything)
- `content.md` — voice samples and prompt guidance (when tone matters)
- `memory.md` / `notes.md` — learned preferences and open follow-ups

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Gather inputs; load config.profile, content.md, memory.md & notes.md", status: "in_progress" },
  { content: "Ask for any missing inputs — never assume or hallucinate", status: "pending" },
  { content: "Rewrite the supplied text to read naturally", status: "pending" },
  { content: "Validate output; record new facts to memory.md / follow-ups to notes.md", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Parse the request / `$ARGUMENTS` and list what this skill needs.
2. **Load your profile & memory.** Read `config.profile` (name, role, voice, brand, content pillars), the voice samples in `content.md` when tone matters, and the shared `memory.md` / `notes.md` for learned preferences and open follow-ups.
3. **Ask if anything is missing.** If a required input is unknown, stop and ask a specific question. Never assume, guess, or invent facts, numbers, names, or sources.
4. **Do the work** following the sections below.
5. **Validate, output & record.** Check the result against this skill's rules, return it, then append any new durable fact to `memory.md` and any follow-up to `notes.md` via `python .agents/scripts/memory.py`.

## The core moves

1. **Cut hedge words and filler wrappers.** Say the thing directly.
2. **Cut corporate/AI-cliché vocabulary.** Use plain, specific words instead.
3. **Vary sentence length on purpose.** Uniform medium-length sentences read flat.
4. **Replace vague claims with concrete anchors.** Numbers, names, dates, examples.
5. **Let structure emerge from content**, rather than imposing bullet lists and
   subheadings on everything.
6. **Match voice to register** — a Slack update, a memo, and an essay don't sound alike.
7. **Drop assistant-voice tics** — "helpful assistant" framing reads as generic in any
   register, human or AI-drafted.

---

## 1. Hedge and filler surgery

Delete or replace:
- "it is important to note that", "it is worth mentioning that", "generally speaking",
  "in many cases", "it can be argued", "often" / "typically" (unless genuinely needed
  for accuracy)
- Announcement-colon openers: "The rule I use:", "The key insight:" — just state it.

Filler-wrapper substitutions (the pattern generalizes — any multi-word wrapper around a
one-word meaning gets the one word):

| Verbose | Direct |
|---|---|
| Due to the fact that | Because |
| In the event that | If |
| Has the ability / capacity to | Can |
| Make a decision / an assumption | Decide / Assume |
| For the purpose of | To / For |
| With regard to / With respect to | About / On |
| Prior to / Subsequent to | Before / After |
| In light of the fact that / Despite the fact that | Since / Although |

Real uncertainty gets human phrasing: "I'm not sure this holds for edge cases" beats
"while results may vary."

## 2. Vocabulary to avoid (and what to use instead)

These words aren't wrong, but they're overused to the point of sounding like filler.
Swap for a plainer, more specific word chosen for the actual context.

- **Verbs:** delve, leverage, utilize, streamline, foster, facilitate, garner, showcase,
  highlight (as standalone verb), underscore (as standalone verb) → pick the concrete
  verb: "use", "help", "cut", "show"
- **Adjectives:** robust, comprehensive, pivotal, nuanced, multifaceted, crucial
  (overused), enduring, vibrant, intricate → say what specifically makes it that
- **Abstract nouns:** landscape (figurative), tapestry (figurative), testament
  (figurative), interplay, intricacies → name the actual thing
- **Openers/closers:** "in today's fast-paced world", "in conclusion", "in summary",
  "it goes without saying", "at the end of the day" → cut entirely
- **Transitions:** furthermore, moreover, "it is clear that", "this highlights",
  "this underscores" → cut, or use "and"/"but"/"so"
- **Significance inflation:** "stands as a testament to", "marks a pivotal moment in",
  "evolving landscape", "plays a vital role" → state the concrete fact instead
- **Promotional register:** "nestled in the heart of", "boasts a rich heritage",
  "breathtaking", "must-visit", "renowned for" → cut the brochure language
- **Quantifier inflation:** "a myriad of", "a plethora of", "in the realm of"
- **Tutorial scaffolding:** "let's dive in", "let's break this down", "without further
  ado" → just start
- **Sycophantic prefixes:** "great question", "you're absolutely right", "of course!"
- **Templated closers:** "happy to jump on a call", "feel free to reach out", "I hope
  this helps"

## 3. Sentence rhythm

Uniform sentence length (most sentences landing in the same 10–20 word band) reads
monotonous. Aim for real variation:

- Mix short, punchy sentences with longer ones that build across a clause or two.
- Every few sentences, drop in a short fragment. Like that.
- Don't let three consecutive sentences land within 5 words of each other in length.
- A run of only short sentences reads choppy; a run of only long ones reads exhausting.
  Both directions need a counterweight.

## 4. Specificity over abstraction

Every abstract claim benefits from a grounding anchor — a number, a name, a date, a
concrete example.

"Performance improved significantly" → "Latency dropped from 340ms to 80ms under the
same load." If exact specifics aren't available, use honest approximation framing:
"in the cases I've seen...", "the one time this bit us..." — never invent numbers or
examples just to sound specific.

## 5. Structural flattening

Not every idea needs a bulleted list or a numbered section. Some patterns to reconsider:

| Formulaic pattern | More natural alternative |
|---|---|
| Intro sentence + 3-bullet list | A prose paragraph where the items connect through flow |
| "There are three main factors: ..." | Just talk about the factors; let transitions carry it |
| Numbered sections for everything | Sections only when order genuinely matters |
| Topic sentence + evidence + restatement | Skip the restatement — don't recap what you just said |
| Vague attributions: "industry observers note" | Name a specific source, or drop the claim |
| "Challenges and Future Prospects" boilerplate section | The actual challenges, specifically, or cut the section |

## 6. Voice and register

Writing carries a perspective. Depending on register:
- First person where natural: "I find that...", "In my experience..."
- Occasional direct address: "If you've run into this before..."
- Contractions in conversational contexts: "don't", "it's", "you'll"
- Self-correction mid-thought when it's genuine: "— actually, more precisely:"

Calibrate to domain:
- **Technical:** domain-native vocabulary ("the hot path," "this falls apart at scale"),
  short sentences for definitive claims, direct tradeoffs, real tool/version names.
- **Narrative/essay:** open with a scene or specific moment rather than a thesis
  statement; let the argument emerge from the evidence.
- **Professional/business:** cut the throat-clearing opener, state the ask in the first
  line or two, short paragraphs (2–3 sentences in email/memo).
- **Slack/async updates:** fragments are normal, thoughts loop and self-correct,
  approximations over precise figures (`~60%`, `<10min`), lowercase is fine outside
  proper nouns.

## 7. Punctuation habits worth checking

None of these are "wrong" — they're just easy to overuse without noticing:

- **Em dashes:** fine occasionally for a genuine interruption; if every third sentence
  has one, most will read cleaner as a period, comma, or restructure.
- **Semicolons:** rare outside formal/academic registers. A period, or "and"/"but"/"so,"
  usually reads more naturally.
- **Mid-sentence colons:** clean at the end of a complete clause introducing something;
  awkward mid-thought ("The problem: nobody tests this" → "Nobody tests this.").
- **Curly vs. straight quotes:** match whatever your target publishing context expects.

## 8. Cut assistant-voice framing

If the draft reads like a chatbot answering a question rather than a person making a
point, look for:

| Tell | Fix |
|---|---|
| "Here's how I'd think about it...", "Let me walk you through..." | Cut the framing, say the thing |
| "On one hand X, on the other Y, it depends..." | Pick a side; the reader can disagree |
| Unrequested enumeration of options | Answer directly; note the constraint after, if needed |
| Defining terms the audience already knows | Cut — trust the reader |
| A caveat appended to every claim | State the claim; caveat only real edge cases |
| "That's a great question, and..." | Cut entirely |
| Closing summary recapping what was just said | Cut |
| "I hope this helps! Let me know if..." | End on the last substantive sentence |

---

## Quick editing pass

When rewriting a draft, check in this order:
1. Read it once for content — does it say what it needs to say?
2. Scan for banned vocabulary and filler wrappers (section 2) — replace or cut.
3. Check sentence-length variation (section 3) — split or merge as needed.
4. Check every abstract claim has a concrete anchor, or an honest approximation (section 4).
5. Check for unnecessary bullet/numbered structure (section 5) — convert to prose where
   it reads better that way.
6. Read it once more for voice consistency and cut any assistant-voice tics (section 8).

Output the rewritten text itself — skip the "Here's the revised version:" preamble and
the "what I changed" recap unless the user asks for one.
