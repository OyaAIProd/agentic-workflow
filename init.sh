#!/bin/bash
# Agentic Workflow - Quick Initialization Script
# Interactive setup for AI-assisted development methodology
#
# Author: Julien GELEE
# License: MIT
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main/init.sh | bash
#   # Or
#   ./init.sh [--minimal|--full|--memory-postgres|--memory-sqlite]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_URL="https://raw.githubusercontent.com/Krigsexe/agentic-workflow/main"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}        ${CYAN}AGENTIC WORKFLOW${NC} - Quick Setup                      ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}        Rigorous AI Integration Methodology               ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Parse arguments
MODE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --minimal)
            MODE="minimal"
            shift
            ;;
        --full)
            MODE="full"
            shift
            ;;
        --memory-postgres)
            MODE="memory-postgres"
            shift
            ;;
        --memory-sqlite)
            MODE="memory-sqlite"
            shift
            ;;
        --help)
            echo "Usage: ./init.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --minimal          Download CLAUDE.md only"
            echo "  --full             Clone full repository"
            echo "  --memory-postgres  Setup with PostgreSQL memory"
            echo "  --memory-sqlite    Setup with SQLite memory (lightweight)"
            echo "  --help             Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Interactive mode if no arguments
if [ -z "$MODE" ]; then
    echo "Choose installation type / Choisir le type d'installation:"
    echo ""
    echo -e "  ${GREEN}1)${NC} Minimal      - CLAUDE.md only (quick start)"
    echo -e "  ${GREEN}2)${NC} Full         - Complete repository with skills"
    echo -e "  ${GREEN}3)${NC} Memory (PG)  - Full + PostgreSQL persistent memory"
    echo -e "  ${GREEN}4)${NC} Memory (SQLite) - Full + SQLite persistent memory (lightweight)"
    echo ""
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) MODE="minimal" ;;
        2) MODE="full" ;;
        3) MODE="memory-postgres" ;;
        4) MODE="memory-sqlite" ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
fi

echo ""
echo -e "${YELLOW}Selected mode: ${MODE}${NC}"
echo ""

# === MINIMAL INSTALLATION ===
if [ "$MODE" = "minimal" ]; then
    echo -e "${CYAN}[1/2]${NC} Downloading CLAUDE.md..."
    
    if [ -f "CLAUDE.md" ]; then
        echo -e "${YELLOW}Warning: CLAUDE.md already exists.${NC}"
        read -p "Overwrite? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
    
    curl -sSL -o CLAUDE.md "${REPO_URL}/templates/CLAUDE.md"
    
    echo -e "${CYAN}[2/2]${NC} Done!"
    echo ""
    echo -e "${GREEN}✓ CLAUDE.md downloaded successfully${NC}"
    echo ""
    echo "Next steps / Prochaines étapes:"
    echo "  1. Edit CLAUDE.md - Fill in Project Context"
    echo "  2. Commit: git add CLAUDE.md && git commit -m 'docs: add CLAUDE.md'"
    echo "  3. Reference it when working with AI assistants"
    echo ""
    exit 0
fi

# === FULL / MEMORY INSTALLATION ===
echo -e "${CYAN}[1/4]${NC} Cloning repository..."

if [ -d "agentic-workflow" ]; then
    echo -e "${YELLOW}Directory 'agentic-workflow' already exists.${NC}"
    read -p "Remove and re-clone? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf agentic-workflow
    else
        echo "Using existing directory."
    fi
fi

if [ ! -d "agentic-workflow" ]; then
    git clone https://github.com/Krigsexe/agentic-workflow.git
fi

cd agentic-workflow

echo -e "${CYAN}[2/4]${NC} Repository cloned."

# Copy CLAUDE.md to parent directory if it doesn't exist
if [ ! -f "../CLAUDE.md" ]; then
    cp templates/CLAUDE.md ../CLAUDE.md
    echo -e "${GREEN}✓ CLAUDE.md copied to project root${NC}"
fi

echo -e "${CYAN}[3/4]${NC} Setting up skills..."

# Create .claude directory in parent
mkdir -p ../.claude/skills
cp -r skills/epistemic-cognitive-guardrails ../.claude/skills/
cp -r skills/memory-persistence ../.claude/skills/
cp .claude/settings.json ../.claude/

echo -e "${GREEN}✓ Skills installed${NC}"

# === MEMORY SETUP ===
if [ "$MODE" = "memory-postgres" ] || [ "$MODE" = "memory-sqlite" ]; then
    echo -e "${CYAN}[4/4]${NC} Setting up persistent memory..."
    
    cd memory
    chmod +x auto-build.sh
    
    if [ "$MODE" = "memory-sqlite" ]; then
        ./auto-build.sh --sqlite
    else
        ./auto-build.sh
    fi
    
    cd ..
else
    echo -e "${CYAN}[4/4]${NC} Skipping memory setup (use --memory-postgres or --memory-sqlite to enable)"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}                    ${GREEN}Setup Complete!${NC}                        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Files created / Fichiers créés:"
echo "  ✓ CLAUDE.md (project configuration)"
echo "  ✓ .claude/skills/ (epistemic guardrails + memory)"
echo "  ✓ .claude/settings.json (hooks configuration)"

if [ "$MODE" = "memory-postgres" ] || [ "$MODE" = "memory-sqlite" ]; then
    echo "  ✓ ~/.ai_memory/ (persistent memory system)"
fi

echo ""
echo "Next steps / Prochaines étapes:"
echo "  1. Edit ../CLAUDE.md - Fill in your Project Context"
echo "  2. git add CLAUDE.md .claude && git commit -m 'docs: add agentic-workflow'"

if [ "$MODE" = "memory-postgres" ] || [ "$MODE" = "memory-sqlite" ]; then
    echo "  3. Add to your shell: source ~/.ai_memory/shell_init.sh"
    echo "  4. Test memory: python3 ~/.ai_memory/session_init.py --quick"
fi

echo ""
echo "Documentation: https://github.com/Krigsexe/agentic-workflow"
echo ""
echo -e "${CYAN}\"The future of AI collaboration isn't about making AI do more—it's about making AI do better.\"${NC}"
echo ""
