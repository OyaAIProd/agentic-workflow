# Memory Persistence Skill

A skill that enables AI assistants to maintain persistent memory across sessions using PostgreSQL.

---

## Purpose

This skill provides:

1. **Session Continuity** - Remember what happened in previous conversations
2. **Error Learning** - Never solve the same problem twice
3. **Context Preservation** - Project details that survive session boundaries
4. **Progress Tracking** - Checkpoints and milestones

---

## Activation

This skill activates when:

- Starting a new session
- Encountering an error
- Completing significant work
- Needing to recall previous context

---

## Required Setup

Before using this skill, run the auto-build script:

```bash
cd agentic-workflow/memory
chmod +x auto-build.sh
./auto-build.sh
```

---

## Protocols

### Session Start Protocol

At the beginning of every session:

```bash
python3 ~/.ai_memory/session_init.py --quick
```

This provides:
- Recent sessions summary
- Last actions taken
- Known errors and solutions (critical!)
- Important project context
- Recent checkpoints

### Error Handling Protocol

When encountering an error:

1. **FIRST**: Check if it's a known error
   ```python
   from memory_manager import find_similar_error
   known = find_similar_error("your error message here")
   if known:
       print(f"Known solution: {known[0]['solution']}")
   ```

2. **AFTER solving**: Log the solution
   ```python
   from memory_manager import log_error
   log_error(
       error_type="TypeError",
       error_message="Cannot read property 'id' of undefined",
       solution="Add null check before accessing property"
   )
   ```

### Action Logging Protocol

Log significant actions as you work:

```python
from memory_manager import log_action

# After creating something
log_action("create", "Created user authentication module", "src/auth/")

# After fixing something
log_action("fix", "Fixed SQL injection vulnerability in login", "src/auth/login.py")

# After reviewing something
log_action("review", "Reviewed database schema, found normalization issues")
```

### Context Preservation Protocol

Store important information that should persist:

```python
from memory_manager import set_context

# Critical project info
set_context("database_type", "PostgreSQL 15", importance=10)
set_context("api_version", "v2.1.0", importance=8)
set_context("deployment_target", "AWS ECS", importance=7)
```

### Checkpoint Protocol

Create checkpoints at significant moments:

```python
from memory_manager import create_checkpoint

# After completing a feature
create_checkpoint(
    name="User authentication complete",
    description="Login, logout, password reset, 2FA implemented",
    is_milestone=True
)
```

---

## Integration with CLAUDE.md

Add to your project's CLAUDE.md:

```markdown
## Memory Persistence

This project uses persistent memory. At session start:
\`\`\`bash
python3 ~/.ai_memory/session_init.py --quick
\`\`\`

Before debugging errors, always check:
\`\`\`python
from memory_manager import find_similar_error
similar = find_similar_error("error message")
\`\`\`

After solving any error, log it:
\`\`\`python
from memory_manager import log_error
log_error(error_type, error_message, solution)
\`\`\`
```

---

## Available Functions

### Sessions
| Function | Description |
|----------|-------------|
| `start_session(summary)` | Start a new session |
| `end_session(session_id, summary)` | End a session |
| `get_recent_sessions(limit)` | Get recent sessions |

### Actions
| Function | Description |
|----------|-------------|
| `log_action(type, description, target_path)` | Log an action |
| `get_recent_actions(limit, action_type)` | Get recent actions |

### Errors
| Function | Description |
|----------|-------------|
| `log_error(type, message, solution)` | Log error and solution |
| `find_similar_error(message)` | Find known solutions |
| `mark_solution_worked(id, worked)` | Confirm if solution worked |

### Context
| Function | Description |
|----------|-------------|
| `set_context(key, value, category, importance)` | Store context |
| `get_context(key)` | Retrieve context |
| `get_all_context(category, min_importance)` | Get all context |

### Knowledge
| Function | Description |
|----------|-------------|
| `add_knowledge(topic, content, source, confidence, tags)` | Add knowledge |
| `search_knowledge(query)` | Search knowledge base |

### Checkpoints
| Function | Description |
|----------|-------------|
| `create_checkpoint(name, description, is_milestone)` | Create checkpoint |
| `list_checkpoints(limit, milestones_only)` | List checkpoints |

---

## Best Practices

### Do

- Always run session_init at the start
- Log errors immediately after solving them
- Use importance levels (1-10) for context
- Create milestones for significant progress
- Check for known errors before debugging

### Don't

- Skip session initialization
- Forget to log error solutions
- Store sensitive data (passwords, keys) in memory
- Ignore known solutions and re-solve problems

---

## Troubleshooting

### "Database connection failed"

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# If not running
sudo systemctl start postgresql
```

### "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### "Password authentication failed"

Check `~/.ai_memory/.env` has correct password, or re-run:
```bash
./auto-build.sh --password new_password
```

---

## Philosophy

> "An AI that forgets is doomed to repeat its mistakes. Memory is the foundation of learning."

This skill exists because AI assistants have no native memory persistence. By providing external memory, we enable:

- **Accumulated learning** over time
- **Error prevention** through remembered solutions
- **Context continuity** across sessions
- **Progress visibility** through checkpoints

The goal is not to make AI perfect—it's to make it learn from experience.
