<p align="center">
  <a href="http://www.extremeprogramming.org/when.html">
    <img src="logo.png" alt="XP Gates logo linking to Extreme Programming origin" width="120">
  </a>
</p>

<h1 align="center">XP Gates</h1>

<p align="center">
  <strong>Constraints That Cut Code.</strong><br>
  4 gates. 90% less AI-generated bloat.
</p>

---

## The Problem

AI generates bloated code: error handlers for impossible states, interfaces for single implementations, configuration for fixed values.

Most of it is **anticipatory**—code written for scenarios that will never occur.

![Code comparison showing environment validator implementation: left side displays 75 lines of over-engineered code with classes, dataclasses, type validators, and fluent builder pattern; right side shows the same functionality in just 7 lines using a simple list comprehension](before-after.png)

*Same prompt. Same AI. Left: without gates (75 lines). Right: with gates (7 lines).*

---

## Results

| Task | Without Gates | With Gates | Reduction |
|------|---------------|------------|-----------|
| Env Validator | 75 lines | 7 lines | 91% |
| Health Checker | 166 lines | 14 lines | 92% |
| SMS Service | 249 lines | 28 lines | 89% |
| **Total** | **490 lines** | **49 lines** | **90%** |

Same AI. Same prompts. Different instructions.

---

## The 4 Gates

Sequential, blocking constraints. Each gate poses a question—if unanswered, the task halts.

| Gate | Blocking Question | Proceeds When |
|------|-------------------|---------------|
| **1. Spike** | Is the approach validated? | Uncertainty resolved via minimal experiment |
| **2. TDD** | What failing test requires this code? | Test exists and fails |
| **3. YAGNI** | Is this in the current requirements? | Explicit requirement confirmed |
| **4. Simple Design** | Is this the simplest passing implementation? | No simpler alternative exists |

> Gates evaluate in order. Blocked at Gate 1? Never reaches Gate 2.

---

## Why It Works

The 90% reduction comes from **elimination**, not optimization.

| Gate | What It Blocks |
|------|----------------|
| **Spike** | Wrong approaches—blocks implementation before validation |
| **TDD** | Defensive code—blocks code without failing tests |
| **YAGNI** | Speculative features—blocks code without explicit requirements |
| **Simple Design** | Abstraction layers—blocks indirection without justification |

Most AI-generated bloat is anticipatory. XP Gates block anticipation at the source.

---

## The Tradeoff

The 90% reduction is real—but not all eliminated code is waste. XP Gates enforce strict interpretation: if it's not in the requirements, it doesn't get built.

- Ambiguous prompts → minimal output
- Convention-based features get cut (docstrings, convenience returns)
- You must specify what you actually need

> XP Gates don't read minds. They read requirements.

See [`docs/RESEARCH.md`](./docs/RESEARCH.md#tradeoffs) for detailed tradeoff analysis and examples.

---

## Quick Start

Add the prompt file to your AI's system instructions. No tooling required.

### Claude Code
```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/en-yao/xp-gates/main/prompts/CLAUDE.md
```

### Gemini CLI
```bash
curl -o GEMINI.md https://raw.githubusercontent.com/en-yao/xp-gates/main/prompts/GEMINI.md
```

### ChatGPT
Copy [`prompts/CHATGPT.txt`](./prompts/CHATGPT.txt) → Settings → Custom Instructions

### How It Works

1. Add prompt file to system instructions
2. Every task passes through all four gates
3. Gates block silently—no code until all pass

| Format | Platform |
|--------|----------|
| `CLAUDE.md` | Claude Code |
| `GEMINI.md` | Gemini CLI |
| `CHATGPT.txt` | ChatGPT |

See [`prompts/README.md`](./prompts/README.md) for platform differences and usage details.

> The constraint set is fixed. Customization defeats the purpose.

---

## Origin

XP Gates derive from [Extreme Programming](http://www.extremeprogramming.org/when.html) (Kent Beck, 1999):

| XP Practice | XP Gate |
|-------------|---------|
| Spike Solutions | Spike Gate |
| Test-First Programming | TDD Gate |
| You Aren't Gonna Need It | YAGNI Gate |
| Simple Design | Simple Design Gate |

**Key distinction:** XP is a human discipline requiring judgment. XP Gates are machine-readable constraints—binary checks that block progress until satisfied.

XP assumes practitioners internalize principles. XP Gates assume nothing.

---

## Examples

See [`examples/`](./examples/) for actual code comparisons:

| Directory | Description | Lines |
|-----------|-------------|-------|
| `with-gates/` | Code produced with XP Gates | 49 |
| `without-gates/` | Code produced without gates | 490 |

---

## Research

Methodology and detailed test results: [`docs/RESEARCH.md`](./docs/RESEARCH.md)

---

## License

MIT
