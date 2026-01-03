# Examples

Side-by-side comparison of AI-generated code with and without XP Gates.

## Structure

| Directory | Description |
|-----------|-------------|
| `with-gates/` | Minimal implementations produced with XP Gates enforced |
| `without-gates/` | Over-engineered implementations produced without constraints |

## Test Cases

| File | Prompt | With Gates | Without Gates |
|------|--------|------------|---------------|
| `env_validator.py` | "Create a function that validates environment variables" | 7 lines | 75 lines |
| `health_checker.py` | "Create a tool that checks HTTP health for services" | 14 lines | 166 lines |
| `twilio_sms.py` | "Create a service that sends notifications via Twilio SMS" | 28 lines | 249 lines |

## Methodology

1. Same prompt given to the same AI model (Claude)
2. **Without Gates:** Standard prompting with no constraints
3. **With Gates:** System instructions include XP Gates enforcement

See [`docs/RESEARCH.md`](../docs/RESEARCH.md) for detailed analysis.
