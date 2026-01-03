# Prompts

Platform-specific XP Gates prompt files for AI code assistants.

> See the [main README](../README.md) for project overview and quick start.

## Files

| File | Platform | Format |
|------|----------|--------|
| `CLAUDE.md` | Claude Code | Markdown (system instructions) |
| `GEMINI.md` | Gemini CLI | Markdown (system instructions) |
| `CHATGPT.txt` | ChatGPT | Plain text (custom instructions) |

## Platform Differences

**CLAUDE.md / GEMINI.md:** Identical content in markdown format. CLI tools support longer system instructions with full formatting.

**CHATGPT.txt:** Condensed version for ChatGPT's custom instructions field, which has stricter character limits and renders plain text.

## Usage

Add the appropriate file to your AI tool's system instructions:

- **Claude Code:** Place `CLAUDE.md` in your project root
- **Gemini CLI:** Place `GEMINI.md` in your project root
- **ChatGPT:** Copy contents of `CHATGPT.txt` to Settings > Custom Instructions
