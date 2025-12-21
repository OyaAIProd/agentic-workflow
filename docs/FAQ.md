# Frequently Asked Questions

Common questions about the Agentic Workflow methodology.

---

## General Questions

### What is Agentic Workflow?

Agentic Workflow is a methodology for working with AI assistants in a disciplined, consistent way. It provides protocols, templates, and guardrails to prevent common problems like cognitive drift, hallucinations, and context loss.

### Who is this for?

- Developers using AI coding assistants
- Teams wanting consistent AI interaction patterns
- Anyone frustrated by inconsistent AI outputs
- People building complex projects with AI assistance

### Is this only for Claude?

No. While the methodology was developed with Claude, the principles apply to any AI assistant:
- ChatGPT / GPT-4
- GitHub Copilot
- Cursor
- Cody
- Other AI tools

The CLAUDE.md file can be adapted for any system.

### Is this free?

Yes, completely. MIT License. No premium tiers, no donations required.

---

## Technical Questions

### Does CLAUDE.md need to be in the project root?

Recommended but not required. The project root is conventional and most AI tools will find it there. You can place it elsewhere if you reference it explicitly.

### How big should CLAUDE.md be?

Aim for 200-400 lines. The template is ~350 lines. If it grows beyond 400 lines, consider splitting into referenced documents.

### Can I modify CLAUDE.md for my needs?

Absolutely. It's designed to be adapted:
- Remove irrelevant sections (e.g., AI/ML if not used)
- Add project-specific conventions
- Customize the technical stack
- Add team agreements

### Do I need the skill file?

The skill file (`epistemic-cognitive-guardrails`) is optional. It's specifically for Claude's skill system. If you're using other AI tools, the CLAUDE.md alone is sufficient.

---

## Usage Questions

### How do I get the AI to follow CLAUDE.md?

At the start of a conversation or when needed:

```
Please read and follow the protocols in CLAUDE.md for this project.
```

If it drifts:

```
Remember the Work Protocols in CLAUDE.md. 
Please provide a checkpoint and reread the initial request.
```

### How often should I request checkpoints?

Recommended frequency:
- After each significant deliverable
- Every 3-5 exchanges on continuous work
- Before major decisions
- When you sense context loss
- When resuming after a break

### The AI ignores my protocols. What do I do?

1. Be more explicit - copy the relevant section into your prompt
2. Remind firmly - "Follow CLAUDE.md protocols. Do not deviate."
3. Reset context - start a new conversation with CLAUDE.md loaded
4. Simplify - focus on one protocol at a time

### Can I use this for non-coding work?

Yes. The principles apply to any AI interaction:
- Writing documentation
- Research and analysis
- Planning and strategy
- Creative work with constraints

Adapt the technical sections to your domain.

---

## Troubleshooting

### The AI still hallucinates despite following protocols

Protocols reduce but don't eliminate hallucinations. When you suspect fabrication:

1. Ask: "Are you certain about this? What's your source?"
2. Request verification: "Please confirm this in official documentation"
3. Cross-check: Verify critical information independently

### The checkpoints are too verbose

Checkpoints should be concise. If they're growing too large:
- Use bullet points, not prose
- Focus on key items only
- Summarize rather than list everything

### The TODO/Plan feels like overhead

It does add upfront time. But it saves time overall by:
- Preventing rework from misunderstandings
- Catching issues before implementation
- Creating alignment on approach

For very small tasks, a mental TODO is fine. For anything taking more than 15 minutes, write it out.

### My team doesn't want to adopt this

Start small:
1. Use it personally first
2. Show concrete improvements
3. Propose it for one project as an experiment
4. Let results speak

Don't force adoption. Demonstrate value.

---

## Philosophy Questions

### Why "epistemic"?

Epistemology is the study of knowledge—what we know and how we know it. The methodology is fundamentally about knowledge discipline:
- When to assert vs. question
- When to know vs. admit uncertainty
- How to maintain accurate understanding

### Isn't this over-engineering?

It might seem that way for simple tasks. But:
- Complex projects benefit enormously
- The overhead becomes second nature
- Prevention is cheaper than repair

Use judgment. Quick questions don't need full protocols. Complex implementations do.

### Why structure instead of flexibility?

Flexibility without structure becomes chaos. The methodology provides:
- A default path that works
- Clear patterns to follow
- Permission to adapt when needed

Structure enables rather than constrains.

### Does this make AI less creative?

No. Creativity happens within constraints. The methodology constrains process, not output:
- You can still explore innovative solutions
- The AI can still suggest creative approaches
- The guardrails prevent drift, not ideation

---

## Contributing Questions

### How can I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). Key areas:
- Translations
- Tool integrations
- Case studies
- Methodology improvements

### I have an idea for improvement. Where do I share it?

Open a GitHub issue. Describe:
- The current limitation
- Your proposed solution
- Why it would help

### Can I create a derivative work?

Yes, under MIT License. Credit is appreciated but not legally required. If you create something valuable, consider contributing it back.

---

## Didn't Find Your Answer?

Open an issue on GitHub. We'll add your question here if it's common enough.

---

Author: Julien GELEE
Date: 2025-12-21
