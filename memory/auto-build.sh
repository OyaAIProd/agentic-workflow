#!/bin/bash
# Agentic Workflow - Memory Persistence Auto-Build
# Sets up PostgreSQL database and memory persistence for AI agents.
#
# Author: Julien GELEE
# License: MIT
#
# Usage:
#     chmod +x auto-build.sh
#     ./auto-build.sh [--db-only] [--skip-db] [--password <pwd>]
#
# Options:
#     --db-only     Only set up database, skip file configuration
#     --skip-db     Skip database setup, only configure files
#     --password    Set custom database password (default: auto-generated)
#     --help        Show this help

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DB_NAME="ai_memory"
DB_USER="ai_agent"
DB_HOST="localhost"
DB_PORT="5432"
MEMORY_DIR="${HOME}/.ai_memory"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
DB_ONLY=false
SKIP_DB=false
USE_SQLITE=false
DB_PASSWORD=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --db-only)
            DB_ONLY=true
            shift
            ;;
        --skip-db)
            SKIP_DB=true
            shift
            ;;
        --sqlite)
            USE_SQLITE=true
            shift
            ;;
        --password)
            DB_PASSWORD="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./auto-build.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --sqlite      Use SQLite instead of PostgreSQL (lightweight)"
            echo "  --db-only     Only set up database, skip file configuration"
            echo "  --skip-db     Skip database setup, only configure files"
            echo "  --password    Set custom database password (PostgreSQL only)"
            echo "  --help        Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Generate password if not provided
if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD=$(openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 16)
fi

echo -e "${BLUE}=== Agentic Workflow - Memory Persistence Setup ===${NC}"
echo ""

# ============================================================
# STEP 1: Check prerequisites
# ============================================================
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL client not found. Installing...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y postgresql postgresql-contrib
    elif command -v brew &> /dev/null; then
        brew install postgresql
    else
        echo -e "${RED}Error: Cannot install PostgreSQL. Please install manually.${NC}"
        exit 1
    fi
fi

# Check psycopg2
if ! python3 -c "import psycopg2" 2>/dev/null; then
    echo -e "${YELLOW}Installing psycopg2-binary...${NC}"
    pip3 install psycopg2-binary
fi

echo -e "${GREEN}Prerequisites OK${NC}"

# ============================================================
# SQLITE BRANCH - Lightweight alternative
# ============================================================
if [ "$USE_SQLITE" = true ]; then
    echo ""
    echo -e "${BLUE}=== SQLite Mode (Lightweight) ===${NC}"
    echo ""
    
    echo -e "${YELLOW}[1/3] Setting up memory directory...${NC}"
    mkdir -p "${MEMORY_DIR}"
    mkdir -p "${MEMORY_DIR}/checkpoints"
    
    # Copy Python scripts
    cp "${SCRIPT_DIR}/scripts/memory_manager_sqlite.py" "${MEMORY_DIR}/memory_manager.py"
    cp "${SCRIPT_DIR}/scripts/session_init.py" "${MEMORY_DIR}/"
    chmod +x "${MEMORY_DIR}/session_init.py"
    
    echo -e "${GREEN}Memory directory created: ${MEMORY_DIR}${NC}"
    
    echo ""
    echo -e "${YELLOW}[2/3] Creating environment configuration...${NC}"
    
    # Create .env file for SQLite
    cat > "${MEMORY_DIR}/.env" << EOF
# Agentic Workflow - Memory Persistence Configuration (SQLite)
# Generated: $(date -Iseconds)

MEMORY_DB_TYPE=sqlite
MEMORY_DB_PATH=${MEMORY_DIR}/memory.db
EOF
    
    chmod 600 "${MEMORY_DIR}/.env"
    
    # Create shell rc snippet
    cat > "${MEMORY_DIR}/shell_init.sh" << 'EOF'
# Agentic Workflow - Memory Persistence (SQLite)
# Add to your .bashrc or .zshrc:
#   source ~/.ai_memory/shell_init.sh

export MEMORY_DB_TYPE="sqlite"
export MEMORY_DB_PATH="${HOME}/.ai_memory/memory.db"

# Alias for quick session init
alias ai-memory-init="python3 ${HOME}/.ai_memory/session_init.py --quick"
EOF
    
    echo -e "${GREEN}Environment configured${NC}"
    
    echo ""
    echo -e "${YELLOW}[3/3] Initializing SQLite database...${NC}"
    
    # Initialize the database by running the manager
    python3 "${MEMORY_DIR}/memory_manager.py"
    
    echo ""
    echo -e "${BLUE}============================================${NC}"
    echo -e "${GREEN}SQLite Setup complete!${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
    echo "Database: ${MEMORY_DIR}/memory.db"
    echo ""
    echo "Next steps:"
    echo "  1. Add to your shell rc:"
    echo "     source ~/.ai_memory/shell_init.sh"
    echo ""
    echo "  2. Test the connection:"
    echo "     python3 ~/.ai_memory/session_init.py --quick"
    echo ""
    exit 0
fi

# ============================================================
# STEP 2: Set up PostgreSQL database
# ============================================================
if [ "$SKIP_DB" = false ]; then
    echo ""
    echo -e "${YELLOW}[2/5] Setting up PostgreSQL database...${NC}"

    # Check if PostgreSQL is running
    if ! pg_isready -q 2>/dev/null; then
        echo -e "${YELLOW}Starting PostgreSQL...${NC}"
        if command -v systemctl &> /dev/null; then
            sudo systemctl start postgresql
        elif command -v service &> /dev/null; then
            sudo service postgresql start
        else
            echo -e "${RED}Error: Cannot start PostgreSQL. Please start manually.${NC}"
            exit 1
        fi
    fi

    # Create user and database
    echo "Creating database user and database..."
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${DB_NAME};" 2>/dev/null || true
    sudo -u postgres psql -c "DROP USER IF EXISTS ${DB_USER};" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

    # Apply schema
    echo "Applying memory schema..."
    PGPASSWORD="${DB_PASSWORD}" psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} \
        -f "${SCRIPT_DIR}/schemas/001_memory_schema.sql"

    echo -e "${GREEN}Database setup complete${NC}"
else
    echo ""
    echo -e "${YELLOW}[2/5] Skipping database setup (--skip-db)${NC}"
fi

if [ "$DB_ONLY" = true ]; then
    echo ""
    echo -e "${GREEN}Database-only setup complete.${NC}"
    echo ""
    echo "Connection details:"
    echo "  Host: ${DB_HOST}"
    echo "  Port: ${DB_PORT}"
    echo "  Database: ${DB_NAME}"
    echo "  User: ${DB_USER}"
    echo "  Password: ${DB_PASSWORD}"
    exit 0
fi

# ============================================================
# STEP 3: Create memory directory and copy scripts
# ============================================================
echo ""
echo -e "${YELLOW}[3/5] Setting up memory directory...${NC}"

mkdir -p "${MEMORY_DIR}"
mkdir -p "${MEMORY_DIR}/checkpoints"

# Copy Python scripts
cp "${SCRIPT_DIR}/scripts/memory_manager.py" "${MEMORY_DIR}/"
cp "${SCRIPT_DIR}/scripts/session_init.py" "${MEMORY_DIR}/"
chmod +x "${MEMORY_DIR}/session_init.py"

echo -e "${GREEN}Memory directory created: ${MEMORY_DIR}${NC}"

# ============================================================
# STEP 4: Create environment configuration
# ============================================================
echo ""
echo -e "${YELLOW}[4/5] Creating environment configuration...${NC}"

# Create .env file
cat > "${MEMORY_DIR}/.env" << EOF
# Agentic Workflow - Memory Persistence Configuration
# Generated: $(date -Iseconds)

MEMORY_DB_HOST=${DB_HOST}
MEMORY_DB_PORT=${DB_PORT}
MEMORY_DB_NAME=${DB_NAME}
MEMORY_DB_USER=${DB_USER}
MEMORY_DB_PASSWORD=${DB_PASSWORD}
EOF

chmod 600 "${MEMORY_DIR}/.env"

# Create shell rc snippet
cat > "${MEMORY_DIR}/shell_init.sh" << 'EOF'
# Agentic Workflow - Memory Persistence
# Add to your .bashrc or .zshrc:
#   source ~/.ai_memory/shell_init.sh

export MEMORY_DB_HOST="${MEMORY_DB_HOST:-localhost}"
export MEMORY_DB_PORT="${MEMORY_DB_PORT:-5432}"
export MEMORY_DB_NAME="${MEMORY_DB_NAME:-ai_memory}"
export MEMORY_DB_USER="${MEMORY_DB_USER:-ai_agent}"

# Load password from .env if exists
if [ -f "${HOME}/.ai_memory/.env" ]; then
    export $(grep -v '^#' "${HOME}/.ai_memory/.env" | xargs)
fi

# Alias for quick session init
alias ai-memory-init="python3 ${HOME}/.ai_memory/session_init.py --quick"
EOF

echo -e "${GREEN}Environment configured${NC}"

# ============================================================
# STEP 5: Create/Update CLAUDE.md
# ============================================================
echo ""
echo -e "${YELLOW}[5/5] Creating CLAUDE.md instructions...${NC}"

# Check if CLAUDE.md exists in home or project
CLAUDE_MD_PATH=""
if [ -f "${HOME}/CLAUDE.md" ]; then
    CLAUDE_MD_PATH="${HOME}/CLAUDE.md"
elif [ -f "$(pwd)/CLAUDE.md" ]; then
    CLAUDE_MD_PATH="$(pwd)/CLAUDE.md"
fi

# Create memory section
MEMORY_SECTION=$(cat << 'MEMEOF'

## AI Memory Persistence

This project uses PostgreSQL-backed persistent memory for AI agents.

### Quick Start

At the start of each session, run:
```bash
python3 ~/.ai_memory/session_init.py --quick
```

### Available Functions

Import the memory manager:
```python
from memory_manager import MemoryManager
mm = MemoryManager()
```

**Sessions:**
- `start_session(summary)` - Start a new session
- `end_session(session_id, summary)` - End a session
- `get_recent_sessions(limit)` - Get recent sessions

**Actions:**
- `log_action(type, description, target_path)` - Log an action
- `get_recent_actions(limit, action_type)` - Get recent actions

**Errors (Important!):**
- `log_error(type, message, solution)` - Record error with solution
- `find_similar_error(message)` - Find previously solved errors

**Context:**
- `set_context(key, value, category, importance)` - Store context
- `get_context(key)` - Retrieve context

**Knowledge:**
- `add_knowledge(topic, content, source, confidence, tags)` - Add knowledge
- `search_knowledge(query)` - Search knowledge base

**Checkpoints:**
- `create_checkpoint(name, description, is_milestone)` - Save progress
- `list_checkpoints(limit, milestones_only)` - List checkpoints

### Workflow

1. **Start**: Run `session_init.py --quick` to load context
2. **During work**: Use `log_action()` and `log_error()` regularly
3. **End**: Create checkpoint if significant work was done

MEMEOF
)

if [ -n "$CLAUDE_MD_PATH" ]; then
    # Check if memory section already exists
    if grep -q "AI Memory Persistence" "$CLAUDE_MD_PATH"; then
        echo "Memory section already exists in ${CLAUDE_MD_PATH}"
    else
        echo "" >> "$CLAUDE_MD_PATH"
        echo "$MEMORY_SECTION" >> "$CLAUDE_MD_PATH"
        echo -e "${GREEN}Added memory section to ${CLAUDE_MD_PATH}${NC}"
    fi
else
    # Create new CLAUDE.md in home directory
    cat > "${HOME}/CLAUDE.md" << EOF
# Claude AI - Project Configuration

${MEMORY_SECTION}
EOF
    echo -e "${GREEN}Created ${HOME}/CLAUDE.md${NC}"
fi

# ============================================================
# DONE
# ============================================================
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo "Configuration saved to: ${MEMORY_DIR}/.env"
echo ""
echo "Database connection:"
echo "  Host:     ${DB_HOST}"
echo "  Port:     ${DB_PORT}"
echo "  Database: ${DB_NAME}"
echo "  User:     ${DB_USER}"
echo "  Password: ${DB_PASSWORD}"
echo ""
echo "Next steps:"
echo "  1. Add to your shell rc:"
echo "     source ~/.ai_memory/shell_init.sh"
echo ""
echo "  2. Test the connection:"
echo "     python3 ~/.ai_memory/session_init.py --quick"
echo ""
echo "  3. Reference CLAUDE.md when working with AI assistants"
echo ""
echo -e "${YELLOW}Important: Save the password securely!${NC}"
echo ""
