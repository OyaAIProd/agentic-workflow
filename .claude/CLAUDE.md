# CLAUDE.md - Agentic Workflow Repository

Configuration for AI-assisted development of this repository.
Configuration pour le développement assisté par IA de ce dépôt.

---

## Project Context / Contexte Projet

```
Project: agentic-workflow
Description: A rigorous methodology for integrating AI assistants without cognitive drift
Repository: https://github.com/Krigsexe/agentic-workflow
Type: Open-source methodology + tools
```

Maintainer: Julien GELEE (GitHub: Krigsexe)

---

## Repository Structure / Structure du Dépôt

```
agentic-workflow/
  templates/          # User-facing templates (CLAUDE.md)
  skills/             # Claude skills (epistemic-guardrails, memory-persistence)
  memory/             # Persistent memory system (PostgreSQL + SQLite)
  docs/               # Documentation (bilingual EN/FR)
  .claude/            # Repository-specific Claude configuration
  init.sh             # Interactive setup script
```

---

## Development Guidelines / Directives de Développement

### Documentation Standards
- All documentation must be bilingual (EN/FR)
- Scholar/scientist style: precision, structure, neutrality
- No emoji in technical documentation
- Signed with author name and date

### Code Standards
- Python: PEP 8, type hints, docstrings
- Bash: shellcheck compliant, portable where possible
- JSON: validated, properly indented

### Version Control
- Semantic versioning (MAJOR.MINOR.PATCH)
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- All components at same version for releases

---

## Current Version / Version Actuelle

All components: **v1.0.0**

- templates/CLAUDE.md: 1.0.0
- skills/epistemic-cognitive-guardrails: 1.0.0
- skills/memory-persistence: 1.0.0
- memory system: 1.0.0
- documentation: 1.0.0

---

## Testing Checklist / Checklist de Tests

Before any release:

1. [ ] Python syntax valid (`python3 -m py_compile`)
2. [ ] Bash syntax valid (`bash -n`)
3. [ ] JSON valid
4. [ ] All internal links working
5. [ ] No credentials in code
6. [ ] Versions synchronized
7. [ ] Documentation up to date

---

## Contributing to This Repository

When contributing:

1. Follow the 7 Epistemic Pillars (see templates/CLAUDE.md)
2. Use TODO/Plan before substantial work
3. Provide checkpoints for complex changes
4. Test both PostgreSQL and SQLite paths
5. Update relevant documentation
6. Sign commits

---

Author: Julien GELEE
Version: 1.0.0
