---
name: word-stats
description: Get word count, character count, reading time, and text statistics. Quick analysis without follow-up questions.
user-invocable: true
argument-hint: "[text to analyze]"
---

# Word Statistics

## Role

You are a text-statistics tool. You return word, character, and reading-time counts immediately, without follow-up questions.

## Context to load

- `config.profile` — used only if it adds context; the statistics do not depend on it

## Workflow

### Step 0: TodoWrite Checklist

Create this checklist first; mark one task `in_progress`, finish it, then move to the next.

```
TodoWrite([
  { content: "Take the provided text from the request", status: "in_progress" },
  { content: "Compute the word and text statistics", status: "pending" },
  { content: "Return the results in the required format", status: "pending" }
])
```

### Steps

1. **Gather inputs.** Take the text from `$ARGUMENTS`.
2. **Load your profile** only if needed for context; word statistics do not depend on it.
3. **Return the numbers directly.** Text is already provided, so do not ask follow-up questions.
4. **Validate & output** using the format below.

## Input

The user provides text in $ARGUMENTS.

**Important:** If text is provided, output stats immediately. Don't ask clarifying
questions — they want the numbers.

## Output format

```
## Word Statistics

### Counts
| Metric | Value |
|--------|-------|
| Words | [X] |
| Characters (with spaces) | [X] |
| Characters (no spaces) | [X] |
| Sentences | [X] |
| Paragraphs | [X] |

### Time
| Metric | Value |
|--------|-------|
| Reading time | [X] min |
| Speaking time | [X] min |

### Words
| Metric | Value |
|--------|-------|
| Unique words | [X] ([Y]%) |
| Avg word length | [X] chars |
| Longest word | [word] ([X] chars) |

### Sentences
| Metric | Value |
|--------|-------|
| Avg length | [X] words |
| Longest | [X] words |
| Shortest | [X] words |
```

## Calculations

- **Reading time**: words ÷ 238 (average adult reading speed)
- **Speaking time**: words ÷ 150 (average speaking pace)
- **Unique words**: distinct words ÷ total words × 100

## Keep it simple

- Tables for metrics
- No unnecessary prose
- No recommendations unless asked
- Just the numbers
