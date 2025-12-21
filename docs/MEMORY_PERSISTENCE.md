# Memory Persistence for AI Agents

A PostgreSQL-backed persistent memory system that allows AI assistants to learn from past sessions, remember solutions to errors, and maintain project context across conversations.

---

## Why Memory Persistence?

AI assistants have a fundamental limitation: they forget everything between sessions. This leads to:

- **Repeated mistakes**: Solving the same error multiple times
- **Lost context**: Re-explaining project structure every session
- **No learning curve**: Each session starts from zero

Memory persistence solves this by storing:

1. **Sessions** - Track conversation history
2. **Actions** - Log what was done
3. **Errors & Solutions** - Learn from mistakes
4. **Context** - Remember project details
5. **Knowledge** - Accumulate insights
6. **Checkpoints** - Mark progress milestones

---

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Krigsexe/agentic-workflow.git
cd agentic-workflow/memory

# Run the auto-build script
chmod +x auto-build.sh
./auto-build.sh
```

The script will:
1. Install dependencies (psycopg2)
2. Create PostgreSQL database and user
3. Apply the schema
4. Set up `~/.ai_memory/` directory
5. Configure environment variables
6. Update your CLAUDE.md

### Manual Setup

If you prefer manual installation:

```bash
# 1. Create database
sudo -u postgres psql << EOF
CREATE USER ai_agent WITH PASSWORD 'your_password';
CREATE DATABASE ai_memory OWNER ai_agent;
GRANT ALL PRIVILEGES ON DATABASE ai_memory TO ai_agent;
EOF

# 2. Apply schema
PGPASSWORD='your_password' psql -h localhost -U ai_agent -d ai_memory \
    -f memory/schemas/001_memory_schema.sql

# 3. Set environment variables
export MEMORY_DB_HOST=localhost
export MEMORY_DB_PORT=5432
export MEMORY_DB_NAME=ai_memory
export MEMORY_DB_USER=ai_agent
export MEMORY_DB_PASSWORD=your_password

# 4. Copy scripts
mkdir -p ~/.ai_memory
cp memory/scripts/*.py ~/.ai_memory/
```

---

## Usage

### Session Initialization

At the start of each AI session, run:

```bash
python3 ~/.ai_memory/session_init.py --quick
```

This outputs:
- Recent sessions
- Last actions taken
- Known errors and solutions
- Important context
- Recent checkpoints

### Python API

```python
from memory_manager import MemoryManager

mm = MemoryManager()

# Start a session
session_id = mm.start_session("Working on authentication module")

# Log actions
mm.log_action(
    action_type="code_review",
    description="Reviewed auth flow, found XSS vulnerability",
    target_path="src/auth/login.py"
)

# Log errors with solutions (critical for learning!)
mm.log_error(
    error_type="ImportError",
    error_message="No module named 'cryptography'",
    solution="pip install cryptography",
    related_files=["requirements.txt", "src/auth/crypto.py"]
)

# Check for known solutions before debugging
similar = mm.find_similar_error("No module named 'cryptography'")
if similar:
    print(f"Known solution: {similar[0]['solution']}")

# Store context
mm.set_context(
    key="database_type",
    value="PostgreSQL 15",
    category="infrastructure",
    importance=8  # 1-10 scale
)

# Create checkpoint
mm.create_checkpoint(
    name="Auth module complete",
    description="Login, logout, password reset implemented",
    is_milestone=True
)

# End session
mm.end_session(session_id, "Completed authentication module")
mm.close()
```

### Convenience Functions

For quick operations without instantiating:

```python
from memory_manager import log_action, log_error, set_context

log_action("fix", "Fixed null pointer in user service")
log_error("TypeError", "undefined is not a function", "Check variable scope")
set_context("api_version", "v2.1.0")
```

---

## Database Schema

### Tables

| Table | Purpose |
|-------|---------|
| `sessions` | Track conversation sessions |
| `actions` | Log significant actions |
| `error_solutions` | Store errors and their solutions |
| `context` | Key-value store for project info |
| `knowledge_base` | Accumulated knowledge with full-text search |
| `checkpoints` | Progress milestones |

### Error Solutions Table (The Most Important One)

```sql
CREATE TABLE error_solutions (
    id UUID PRIMARY KEY,
    error_type VARCHAR(200) NOT NULL,      -- e.g., "ImportError"
    error_message TEXT NOT NULL,            -- Full error message
    solution TEXT NOT NULL,                 -- How to fix it
    related_files TEXT[],                   -- Files involved
    solution_worked BOOLEAN,                -- Did it actually work?
    occurrences INTEGER DEFAULT 1,          -- How often seen
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

When you encounter an error:

1. **First**: Check if it's known
   ```python
   known = mm.find_similar_error(error_message)
   if known:
       print(f"Try: {known[0]['solution']}")
   ```

2. **After solving**: Log the solution
   ```python
   mm.log_error(error_type, error_message, solution)
   ```

3. **Confirm it worked**:
   ```python
   mm.mark_solution_worked(error_id, worked=True)
   ```

---

## Best Practices

### 1. Always Initialize Sessions

```python
# Good - loads previous context
context = init_session(quick=True)
print(f"Recent errors to avoid: {context['known_errors']}")

# Bad - starts blind
mm = MemoryManager()
# ... no idea what happened before
```

### 2. Log Actions Immediately

```python
# Good - logged right after doing
mm.log_action("create", "Created user model", "models/user.py")
# ... continue working

# Bad - trying to remember later
# ... did lots of work
# What did I even do?
```

### 3. Error Learning is Critical

The most valuable data is error → solution mappings. Always log:

```python
# Every time you fix an error
mm.log_error(
    error_type="TypeError",
    error_message="Cannot read property 'id' of undefined",
    solution="Add null check: if (user && user.id) { ... }",
    related_files=["src/services/user.js"]
)
```

### 4. Use Importance Levels for Context

```python
# Critical - always show (importance 10)
mm.set_context("production_db", "db.prod.example.com", importance=10)

# Important (7-9)
mm.set_context("api_key_location", "~/.config/api.key", importance=8)

# Normal (4-6)
mm.set_context("preferred_editor", "vim", importance=5)

# Low (1-3) - only show when specifically needed
mm.set_context("last_coffee_break", "14:30", importance=1)
```

### 5. Create Checkpoints at Milestones

```python
# After completing significant work
mm.create_checkpoint(
    name="v1.0 Release Ready",
    description="All tests passing, documentation complete",
    is_milestone=True,
    state={"tests": "passing", "coverage": "87%"}
)
```

---

## Integration with Claude Code

### CLAUDE.md Configuration

Add to your project's CLAUDE.md:

```markdown
## Memory Persistence

At session start, run:
\`\`\`bash
python3 ~/.ai_memory/session_init.py --quick
\`\`\`

Before debugging any error, check:
\`\`\`python
from memory_manager import find_similar_error
known = find_similar_error("your error message")
\`\`\`
```

### Hooks (When Available)

Claude Code hooks can automate memory operations:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.ai_memory/session_init.py --quick"
      }]
    }]
  }
}
```

> Note: Hooks may have limitations depending on Claude Code version.

---

## Troubleshooting

### Connection Refused

```
Error: connection to server at "localhost" refused
```

**Solution**: Start PostgreSQL
```bash
sudo systemctl start postgresql
# or
sudo service postgresql start
```

### Authentication Failed

```
Error: password authentication failed for user "ai_agent"
```

**Solution**: Reset password
```bash
sudo -u postgres psql -c "ALTER USER ai_agent WITH PASSWORD 'new_password';"
# Update ~/.ai_memory/.env with new password
```

### Missing psycopg2

```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solution**: Install the module
```bash
pip install psycopg2-binary
```

### Database Not Found

```
Error: database "ai_memory" does not exist
```

**Solution**: Run auto-build or create manually
```bash
./auto-build.sh
# or
sudo -u postgres psql -c "CREATE DATABASE ai_memory OWNER ai_agent;"
```

---

## Security Notes

1. **Password storage**: The `.env` file is chmod 600 (owner-only read/write)
2. **Network**: Default config uses localhost only
3. **Credentials**: Never commit `.env` files to version control
4. **Backup**: Regular pg_dump for important memory data

---

## Contributing

Improvements welcome! Key areas:

- Additional database backends (SQLite, MySQL)
- Cloud sync options
- Memory compression for old sessions
- Better error matching algorithms

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## License

MIT License - Use freely, contribute back if you can.
