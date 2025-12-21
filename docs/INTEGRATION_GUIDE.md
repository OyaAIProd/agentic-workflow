# Integration Guide / Guide d'Intégration

A comprehensive guide to integrating the Agentic Workflow methodology into your projects.
Un guide complet pour intégrer la méthodologie Agentic Workflow dans vos projets.

---

## Table of Contents / Sommaire

1. [Prerequisites / Prérequis](#prerequisites--prérequis)
2. [Quick Start / Démarrage Rapide](#quick-start--démarrage-rapide)
3. [Full Integration / Intégration Complète](#full-integration--intégration-complète)
4. [Memory Persistence / Mémoire Persistante](#memory-persistence--mémoire-persistante)
5. [Configuration](#configuration)
6. [Usage Patterns / Patterns d'Utilisation](#usage-patterns--patterns-dutilisation)
7. [Tool-Specific Integration / Intégration par Outil](#tool-specific-integration--intégration-par-outil)
8. [Troubleshooting / Dépannage](#troubleshooting--dépannage)

---

## Prerequisites / Prérequis

### Required / Requis

| EN | FR |
|----|-----|
| A project (new or existing) | Un projet (nouveau ou existant) |
| An AI assistant (Claude, GPT, Copilot, etc.) | Un assistant IA (Claude, GPT, Copilot, etc.) |
| Basic familiarity with Markdown | Familiarité basique avec Markdown |

### Recommended / Recommandé

| EN | FR |
|----|-----|
| Version control (Git) | Contrôle de version (Git) |
| Terminal/CLI access | Accès terminal/CLI |
| 15 minutes for initial setup | 15 minutes pour la configuration initiale |

### For Memory Persistence / Pour la Mémoire Persistante

| EN | FR |
|----|-----|
| Python 3.8+ | Python 3.8+ |
| PostgreSQL 12+ OR SQLite 3 | PostgreSQL 12+ OU SQLite 3 |
| pip (Python package manager) | pip (gestionnaire de paquets Python) |

---

## Quick Start / Démarrage Rapide

### Option 1: Minimal (CLAUDE.md only / uniquement)

```bash
# Download / Télécharger
curl -o CLAUDE.md https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main/templates/CLAUDE.md

# Or with wget / Ou avec wget
wget https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main/templates/CLAUDE.md
```

Place in project root / Placer à la racine du projet:
```
your-project/
  src/
  docs/
  CLAUDE.md    <-- Here / Ici
  README.md
```

Edit Project Context / Éditer le contexte projet:
```markdown
## Project Context

Project: MyAwesomeApp
Description: A web application for task management
Repository: https://github.com/username/my-awesome-app

Maintainer: Your Name
```

### Option 2: One-liner Installation

```bash
# Interactive setup / Installation interactive
curl -sSL https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main/init.sh | bash
```

---

## Full Integration / Intégration Complète

### Step 1: Clone / Étape 1 : Cloner

```bash
git clone https://github.com/Krigsexe/agentic-workflow.git
cd agentic-workflow
```

### Step 2: Copy to Your Project / Étape 2 : Copier vers votre projet

```bash
# CLAUDE.md template
cp templates/CLAUDE.md /path/to/your-project/

# Skills (for Claude)
cp -r skills/epistemic-cognitive-guardrails /path/to/your-project/.claude/skills/
cp -r skills/memory-persistence /path/to/your-project/.claude/skills/
```

### Step 3: Configure Stack / Étape 3 : Configurer la stack

Edit CLAUDE.md to match your project / Éditer CLAUDE.md selon votre projet:

**Python Project / Projet Python:**
```markdown
| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Database | PostgreSQL + SQLAlchemy |
| Infrastructure | Docker + AWS |
```

**JavaScript Project / Projet JavaScript:**
```markdown
| Layer | Technology |
|-------|------------|
| Backend | NestJS |
| Frontend | Vite + React |
| Database | PostgreSQL + Prisma |
```

### Step 4: Remove Inapplicable Sections / Étape 4 : Supprimer les sections non applicables

If not using AI/ML / Si pas d'IA/ML:
- Remove "AI/ML Layer" table / Supprimer le tableau "AI/ML Layer"
- Remove "AI/ML Specific" section / Supprimer la section "AI/ML Specific"
- Remove ML-related checklists / Supprimer les checklists ML

### Step 5: Commit / Étape 5 : Commit

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md configuration for AI-assisted development"
```

---

## Memory Persistence / Mémoire Persistante

Memory persistence allows your AI assistant to remember across sessions.
La mémoire persistante permet à votre assistant IA de se souvenir entre les sessions.

### Quick Setup with PostgreSQL / Installation rapide avec PostgreSQL

```bash
cd agentic-workflow/memory
chmod +x auto-build.sh
./auto-build.sh
```

The script handles / Le script gère:
- PostgreSQL database creation / Création de la base PostgreSQL
- Schema application / Application du schéma
- Python dependencies / Dépendances Python
- Environment configuration / Configuration environnement
- Shell aliases / Alias shell

### Alternative: SQLite (Lightweight) / Alternative : SQLite (Léger)

For projects without PostgreSQL / Pour les projets sans PostgreSQL:

```bash
cd agentic-workflow/memory
chmod +x auto-build.sh
./auto-build.sh --sqlite
```

SQLite stores data locally in `~/.ai_memory/memory.db`.
SQLite stocke les données localement dans `~/.ai_memory/memory.db`.

### Usage / Utilisation

At each session start / À chaque début de session:

```bash
python3 ~/.ai_memory/session_init.py --quick
```

Output includes / La sortie inclut:
- Recent sessions / Sessions récentes
- Last actions / Dernières actions
- Known errors and solutions / Erreurs connues et solutions
- Important context / Contexte important
- Recent checkpoints / Checkpoints récents

### Python API

```python
from memory_manager import MemoryManager

mm = MemoryManager()

# Log actions / Journaliser les actions
mm.log_action("code_review", "Reviewed auth module", "src/auth/")

# Log errors with solutions / Journaliser les erreurs avec solutions
mm.log_error(
    error_type="ImportError",
    error_message="No module named 'cryptography'",
    solution="pip install cryptography"
)

# Check for known solutions / Vérifier les solutions connues
similar = mm.find_similar_error("No module named 'cryptography'")
if similar:
    print(f"Known solution: {similar[0]['solution']}")

# Store context / Stocker le contexte
mm.set_context("database_type", "PostgreSQL 15", importance=8)

# Create checkpoint / Créer un checkpoint
mm.create_checkpoint("Auth complete", "Login, logout, 2FA implemented", is_milestone=True)
```

---

## Configuration

### Essential Sections / Sections Essentielles

Always present / Toujours présentes:

1. **Project Context** - Who, what, where / Qui, quoi, où
2. **Fundamental Principles** - The 7 pillars / Les 7 piliers
3. **Work Protocols** - TODO/Plan and Checkpoints
4. **Security Requirements** - Non-negotiable / Non négociable

### Optional Sections / Sections Optionnelles

Adapt to needs / Adapter selon les besoins:

- **Technical Stack** - Customize to your technologies / Personnaliser selon vos technologies
- **AI/ML Specific** - Only if using ML / Seulement si utilisation ML
- **Quick Reference** - Project-specific commands / Commandes spécifiques au projet

### Customization Examples / Exemples de Personnalisation

**Project-specific commands / Commandes spécifiques:**
```markdown
### Commands

```bash
npm run custom:command   # Your description
python manage.py migrate # Django migrations
make deploy-staging      # Deploy to staging
```
```

**Team conventions / Conventions d'équipe:**
```markdown
### Team Conventions

- Branch naming: `feature/TICKET-description`
- Commit format: `type(scope): message`
- PR reviews: minimum 1 approval
```

---

## Usage Patterns / Patterns d'Utilisation

### Pattern 1: Starting Work / Démarrer un travail

```
You: I want to add user authentication.
Vous: Je veux ajouter l'authentification utilisateur.

AI should respond with / L'IA doit répondre avec:
1. Work Plan with TODO / Plan de travail avec TODO
2. Questions for clarification / Questions de clarification
3. Then proceed / Puis procéder
```

### Pattern 2: Requesting Checkpoint / Demander un Checkpoint

```
You: Give me a checkpoint of our progress.
Vous: Donne-moi un checkpoint de notre progression.

AI response / Réponse IA:
## Checkpoint

Done / Fait:
- [completed elements / éléments complétés]

In progress / En cours:
- [current work / travail actuel]

TODO / À faire:
- [next steps / prochaines étapes]
```

### Pattern 3: Enforcing Protocols / Appliquer les Protocoles

If AI drifts / Si l'IA dérive:

```
EN: Remember to follow CLAUDE.md protocols. Reread the initial request and provide a checkpoint.

FR: N'oublie pas de suivre les protocoles CLAUDE.md. Relis la demande initiale et fournis un checkpoint.
```

### Pattern 4: Error Handling with Memory / Gestion d'Erreurs avec Mémoire

```
You: I'm getting "Cannot read property of undefined"
Vous: J'ai l'erreur "Cannot read property of undefined"

AI should / L'IA doit:
1. Check memory for similar errors / Vérifier la mémoire pour erreurs similaires
2. If found, apply known solution / Si trouvée, appliquer la solution connue
3. If new, solve and log for future / Si nouvelle, résoudre et journaliser
```

---

## Tool-Specific Integration / Intégration par Outil

### Claude (Anthropic)

CLAUDE.md is designed for Claude. For best results:
CLAUDE.md est conçu pour Claude. Pour de meilleurs résultats:

- Use epistemic-cognitive-guardrails skill / Utiliser la skill epistemic-cognitive-guardrails
- Use memory-persistence skill / Utiliser la skill memory-persistence
- Reference CLAUDE.md in conversations / Référencer CLAUDE.md dans les conversations
- Enable artifacts for code generation / Activer les artifacts pour la génération de code

**Claude Code Hooks Configuration:**

Create `.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "python3 ~/.ai_memory/session_init.py --quick"
    }]
  },
  "skills": [
    "epistemic-cognitive-guardrails",
    "memory-persistence"
  ]
}
```

### ChatGPT / GPT-4

Copy essential sections into Custom Instructions:
Copier les sections essentielles dans les Instructions Personnalisées:

- The 7 Epistemic Pillars / Les 7 Piliers Épistémiques
- Work Protocols / Protocoles de Travail
- Security Requirements / Exigences de Sécurité

### Cursor IDE

1. Add CLAUDE.md to project root / Ajouter CLAUDE.md à la racine du projet
2. Cursor will include it in context / Cursor l'inclura dans le contexte
3. Reference it in prompts when needed / Le référencer dans les prompts si nécessaire

### GitHub Copilot

Create `.github/copilot-instructions.md`:
```markdown
# Copilot Instructions

Follow these principles when generating code:
[Copy relevant CLAUDE.md sections]

Security requirements:
- Never hardcode credentials
- Use environment variables for secrets
- Validate all inputs
```

### VS Code with Continue

Add to `.continue/config.json`:
```json
{
  "systemMessage": "Read and follow the protocols in CLAUDE.md for this project. Prioritize security, use checkpoints, and never invent information."
}
```

---

## Troubleshooting / Dépannage

### AI Ignores CLAUDE.md / L'IA Ignore CLAUDE.md

**Problem / Problème:** AI doesn't follow protocols / L'IA ne suit pas les protocoles.

**Solution:**
1. Explicitly reference CLAUDE.md at conversation start / Référencer explicitement CLAUDE.md au début
2. Copy relevant sections into your prompt / Copier les sections pertinentes dans votre prompt
3. Remind with / Rappeler avec: "Follow Work Protocols in CLAUDE.md"

### AI Creates Duplicate Files / L'IA Crée des Fichiers Dupliqués

**Problem / Problème:** AI creates `README_v2.md` instead of editing `README.md`.

**Solution:**
1. Quote Documentation Standards section / Citer la section Standards de Documentation
2. State explicitly / Dire explicitement: "Modify existing file, do not create duplicates"
3. Use self-verification checklist / Utiliser la checklist d'auto-vérification

### AI Loses Context / L'IA Perd le Contexte

**Problem / Problème:** After several exchanges, AI forgets requirements.

**Solution:**
1. Request a checkpoint / Demander un checkpoint
2. Ask AI to reread initial request / Demander à l'IA de relire la demande initiale
3. With memory persistence: context is preserved / Avec mémoire persistante: le contexte est préservé

### AI Invents Information / L'IA Invente des Informations

**Problem / Problème:** AI makes up facts or capabilities.

**Solution:**
1. Quote Pillar 2 / Citer le Pilier 2: "Honesty - I don't know beats fabrication"
2. Ask / Demander: "Are you certain? What's your source? / Es-tu certain? Quelle est ta source?"
3. Request verification from official docs / Demander vérification dans la doc officielle

### Memory Database Connection Failed / Échec de Connexion à la Base Mémoire

**Problem / Problème:** "Connection refused" or "Authentication failed"

**Solution:**
```bash
# Check PostgreSQL is running / Vérifier que PostgreSQL tourne
sudo systemctl status postgresql

# If not running / Si pas en cours
sudo systemctl start postgresql

# Reset password if needed / Réinitialiser le mot de passe si nécessaire
sudo -u postgres psql -c "ALTER USER ai_agent WITH PASSWORD 'new_password';"

# Update ~/.ai_memory/.env with new password
```

### Missing Python Module / Module Python Manquant

**Problem / Problème:** `ModuleNotFoundError: No module named 'psycopg2'`

**Solution:**
```bash
pip install psycopg2-binary
# Or for SQLite / Ou pour SQLite (usually included in Python)
```

---

## Next Steps / Prochaines Étapes

1. Read [Methodology Deep Dive](METHODOLOGY.md) / Lire la méthodologie approfondie
2. Check [FAQ](FAQ.md) for common questions / Consulter la FAQ
3. Explore [Memory Persistence](MEMORY_PERSISTENCE.md) / Explorer la mémoire persistante
4. Contribute via Pull Request / Contribuer via Pull Request

---

Author: Julien GELEE
Date: 2025-12-21
Version: 1.0.0
