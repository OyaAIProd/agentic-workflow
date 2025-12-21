# Agentic Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791.svg)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3+-003B57.svg)](https://www.sqlite.org/)

A rigorous methodology for integrating AI assistants into development workflows without cognitive drift.

> "The future of AI collaboration isn't about making AI do more—it's about making AI do better."

---

## The Problem

Working with AI coding assistants often leads to frustrating patterns:

- **Cognitive drift**: The AI gradually loses track of the original objective
- **Hallucinated solutions**: Plausible-sounding but incorrect implementations
- **Documentation chaos**: Duplicated files, inconsistent naming, forgotten context
- **Security leaks**: Credentials accidentally hardcoded, sensitive data exposed
- **Lost context**: After a few exchanges, the AI forgets critical requirements

Sound familiar? You're not alone.

---

## The Solution

This repository provides a **battle-tested methodology** for strict AI integration, developed through extensive real-world usage. It's built on four pillars:

1. **CLAUDE.md** - A universal configuration file for any project
2. **Epistemic Guardrails** - A skill that enforces cognitive discipline
3. **Work Protocols** - Structured approaches that prevent drift
4. **Memory Persistence** - PostgreSQL-backed memory that survives between sessions

---

## Quick Start

### Option 1: Minimal Setup (CLAUDE.md only)

```bash
# Copy CLAUDE.md to your project root
curl -o CLAUDE.md https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main/templates/CLAUDE.md

# Edit the Project Context section
# Start working with your AI assistant
```

### Option 2: Full Setup (CLAUDE.md + Skill)

```bash
# Clone the repository
git clone https://github.com/Krigsexe/agentic-workflow.git

# Copy templates to your project
cp agentic-workflow/templates/CLAUDE.md your-project/
cp -r agentic-workflow/skills/epistemic-cognitive-guardrails your-project/.claude/skills/
```

### Option 3: Memory Persistence (Recommended for long-term projects)

```bash
# Clone and set up persistent memory
git clone https://github.com/Krigsexe/agentic-workflow.git
cd agentic-workflow/memory

# Run the auto-build script (requires PostgreSQL)
chmod +x auto-build.sh
./auto-build.sh

# At the start of each AI session, run:
python3 ~/.ai_memory/session_init.py --quick
```

This gives your AI assistant:
- **Session history** - What happened in previous conversations
- **Error learning** - Solutions to previously solved problems
- **Project context** - Key information that persists
- **Checkpoints** - Progress milestones

See [Memory Persistence Guide](docs/MEMORY_PERSISTENCE.md) for full documentation.

---

## Core Principles

### The 7 Epistemic Pillars

| Pillar | Principle | In Practice |
|--------|-----------|-------------|
| 1 | **Anti-drift** | Never invent to fill gaps—ask instead |
| 2 | **Honesty** | "I don't know" beats plausible fabrication |
| 3 | **Holistic view** | Reread full context before responding |
| 4 | **Integrity** | Quality over speed, always |
| 5 | **Engineer posture** | Pragmatism + methodological rigor |
| 6 | **Questions first** | Doubt = ask, never assume |
| 7 | **Context sync** | Regular checkpoints, perpetual realignment |

### Work Protocols

**Before any work:**
```
## Work Plan

Objective: [clear description]

TODO:
[ ] Step 1 - [description]
[ ] Step 2 - [description]

Vigilance points: [critical elements]
```

**Regular checkpoints:**
```
## Checkpoint

Done:
- [completed elements]

In progress:
- [current work]

TODO:
- [next steps]

Global objective: [vision reminder]
```

---

## What's Included

```
agentic-workflow/
  README.md                    # You are here
  LICENSE                      # MIT License
  CONTRIBUTING.md              # How to contribute
  templates/
    CLAUDE.md                  # Universal project configuration
  skills/
    epistemic-cognitive-guardrails/
      SKILL.md                 # Cognitive discipline skill
      references/
        checkpoint-template.md
    memory-persistence/
      SKILL.md                 # Memory persistence skill
  memory/
    auto-build.sh              # One-command setup script
    schemas/
      001_memory_schema.sql    # PostgreSQL schema
    scripts/
      memory_manager.py        # Python API for memory
      session_init.py          # Session initialization
  docs/
    INTEGRATION_GUIDE.md       # Detailed setup guide
    METHODOLOGY.md             # Deep dive into the approach
    MEMORY_PERSISTENCE.md      # Memory persistence guide
    FAQ.md                     # Common questions
```

---

## Why This Works

Traditional AI assistant usage follows a "fire and forget" pattern: you ask, it answers, you move on. This creates accumulating context loss.

This methodology introduces **structured friction**:

- **Mandatory planning** forces clarity before action
- **Regular checkpoints** prevent context decay
- **Explicit protocols** eliminate ambiguity
- **Documentation standards** ensure consistency

The result? AI that stays aligned with your objectives, produces consistent output, and doesn't drift into hallucination territory.

---

## Real-World Results

This methodology was developed while building:

- **Synapse** - An autonomous research system with 7 specialized AI agents
- **YGGDRASIL** - An ethical AGI architecture project
- **Alixia** - A Swiss SaaS marketing automation platform
- **Multiple production applications** with NestJS, React, and ML components

It emerged from frustration with inconsistent AI outputs and evolved into a rigorous framework through iterative refinement.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Integration Guide](docs/INTEGRATION_GUIDE.md) | Step-by-step setup instructions |
| [Methodology Deep Dive](docs/METHODOLOGY.md) | The thinking behind the approach |
| [Memory Persistence](docs/MEMORY_PERSISTENCE.md) | PostgreSQL-backed AI memory |
| [FAQ](docs/FAQ.md) | Common questions answered |
| [CLAUDE.md Template](templates/CLAUDE.md) | Ready-to-use project configuration |

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas where help is appreciated:
- Translations (FR, DE, ES, etc.)
- Integrations with other AI tools (Cursor, Copilot, etc.)
- Case studies and real-world examples
- Improvements to the methodology

---

## Philosophy

> "Between innovation and rigor lies the path to useful AI."

This project exists because AI assistants are powerful but imperfect. Rather than accepting their limitations, we can work around them with structured discipline.

The goal isn't to constrain AI—it's to channel its capabilities toward consistent, reliable output. Think of it as guardrails on a mountain road: they don't slow you down, they keep you from falling off the cliff.

---

## License

MIT License - Use freely, contribute back if you can.

---

## Author

**Julien GELEE** (GitHub: [@Krigsexe](https://github.com/Krigsexe))

CTO and AI Engineer, building ethical AI systems with Swiss precision.

---

## Support

If this methodology helps your work:
- Star the repository
- Share with colleagues
- Open issues for improvements
- Contribute back

No donations, no premium tiers, no strings attached. Just better AI collaboration for everyone.

---

## Keywords / Topics

For GitHub repository topics:

```
ai-assistant, claude, gpt, llm, developer-tools, productivity,
ai-workflow, cognitive-discipline, memory-persistence, postgresql,
sqlite, python, methodology, best-practices, prompt-engineering,
ai-collaboration, epistemic-guardrails, context-management,
error-learning, checkpoints, documentation, open-source
```

**Primary keywords:**
- `agentic-workflow` - The methodology name
- `ai-assistant-integration` - What it does
- `cognitive-drift-prevention` - The problem it solves
- `persistent-memory-ai` - Key feature

---

*"The best AI assistant is one that knows its limits and works within them."*
