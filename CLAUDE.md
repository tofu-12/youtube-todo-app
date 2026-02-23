# General Guidelines

- Always respond in Japanese.
- Use sub-agents for research and debugging to preserve context.
- Write documentation under `docs/` in Japanese.
- Write CLAUDE.md in English for accuracy.

---

# Coding Conventions

## Python
- Write all code content in English (variable names, comments, logs, docstrings, error messages, etc.).
- Follow PEP8 style guidelines.

### PEP8 style guidelines
| Category | Rule |
|---|---|
| Indentation | 4 spaces |
| Blank lines | 2 lines before/after top-level definitions; 1 line between methods |
| Imports | Order: standard library → third-party → local |
| Variable / function names | `snake_case` |
| Class names | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` |
| Private members | Prefix with `_` (e.g. `_internal`) |
| Docstrings | Required for all public modules, functions, classes, and methods |
| Inline comments | 2 spaces after code, start with `# `. Avoid commenting self-evident code |
| Comparison operators | Use `is` only for `None` and booleans; use `==` otherwise |
| Comprehensions | Prefer list comprehensions and generator expressions |

---

# Slack Notification Rules

Before ending every response, check if notifications are enabled:

```bash
test -f .claude/slack-notify/state/enabled && echo "enabled" || echo "disabled"
```

If **enabled**, write a 2-4 line summary to `.claude/slack-notify/state/pending_message`:

```bash
.claude/slack-notify/scripts/write_pending.sh "<line1>\n<line2>"
```

- Detect language from `state/lang` (default: `en` if missing)
- Follow the message format in `.claude/slack-notify/SKILL.md`
- The Stop hook sends this file automatically — do NOT call notify_slack.py directly
