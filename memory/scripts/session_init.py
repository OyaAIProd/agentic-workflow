#!/usr/bin/env python3
"""
Agentic Workflow - Session Initialization
Run at the start of each AI session to load context.

Author: Julien GELEE
License: MIT

Usage:
    python session_init.py [--quick] [--json]

Options:
    --quick     Quick summary only
    --json      Output as JSON
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from memory_manager import MemoryManager
except ImportError:
    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from memory_manager import MemoryManager


def init_session(quick: bool = False, as_json: bool = False) -> dict:
    """Initialize session and return context."""

    try:
        mm = MemoryManager()
    except Exception as e:
        if as_json:
            return {"error": str(e)}
        print(f"Error connecting to memory database: {e}")
        return {}

    context = {
        "timestamp": datetime.now().isoformat(),
        "sessions": [],
        "recent_actions": [],
        "known_errors": [],
        "project_context": {},
        "checkpoints": []
    }

    # Get recent sessions
    try:
        sessions = mm.get_recent_sessions(limit=5)
        context["sessions"] = [
            {
                "id": str(s["id"])[:8],
                "started": str(s["started_at"]),
                "summary": s["summary"]
            }
            for s in sessions
        ]
    except Exception:
        pass

    # Get recent actions
    try:
        actions = mm.get_recent_actions(limit=10 if quick else 20)
        context["recent_actions"] = [
            {
                "type": a["action_type"],
                "description": a["description"][:80] if quick else a["description"],
                "created": str(a["created_at"])
            }
            for a in actions
        ]
    except Exception:
        pass

    # Get known errors (important for avoiding repeat mistakes)
    try:
        from psycopg2.extras import RealDictCursor
        conn = mm._get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT error_type, error_message, solution, occurrences
                FROM error_solutions
                ORDER BY occurrences DESC, created_at DESC
                LIMIT 5
            """)
            errors = cur.fetchall()

        context["known_errors"] = [
            {
                "type": e["error_type"],
                "message": e["error_message"][:60],
                "solution": e["solution"][:100] if quick else e["solution"],
                "occurrences": e["occurrences"]
            }
            for e in errors
        ]
    except Exception:
        pass

    # Get project context
    try:
        ctx = mm.get_all_context(min_importance=5)
        context["project_context"] = {
            c["key"]: c["value"][:100] if quick else c["value"]
            for c in ctx
        }
    except Exception:
        pass

    # Get recent checkpoints
    try:
        checkpoints = mm.list_checkpoints(limit=5, milestones_only=True)
        context["checkpoints"] = [
            {
                "name": cp["name"],
                "description": cp["description"][:60] if cp["description"] else None,
                "created": str(cp["created_at"])
            }
            for cp in checkpoints
        ]
    except Exception:
        pass

    mm.close()
    return context


def print_context(context: dict, as_json: bool = False):
    """Print context in human or JSON format."""

    if as_json:
        print(json.dumps(context, indent=2, default=str))
        return

    print("=" * 60)
    print("AGENTIC WORKFLOW - SESSION INIT")
    print(f"Timestamp: {context.get('timestamp', 'N/A')}")
    print("=" * 60)

    # Sessions
    if context.get("sessions"):
        print("\n--- RECENT SESSIONS ---")
        for s in context["sessions"]:
            summary = s.get("summary", "No summary")[:50]
            print(f"  [{s['id']}] {summary}")

    # Actions
    if context.get("recent_actions"):
        print("\n--- RECENT ACTIONS ---")
        for a in context["recent_actions"][:10]:
            print(f"  [{a['type']}] {a['description'][:60]}")

    # Known errors (critical!)
    if context.get("known_errors"):
        print("\n--- KNOWN ERRORS (Avoid repeating!) ---")
        for e in context["known_errors"]:
            print(f"  [{e['type']}] {e['message']}")
            print(f"    -> Solution: {e['solution']}")

    # Project context
    if context.get("project_context"):
        print("\n--- PROJECT CONTEXT ---")
        for key, value in list(context["project_context"].items())[:10]:
            val_preview = str(value)[:50]
            print(f"  {key}: {val_preview}")

    # Checkpoints
    if context.get("checkpoints"):
        print("\n--- MILESTONES ---")
        for cp in context["checkpoints"]:
            print(f"  [{cp['created'][:10]}] {cp['name']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Initialize AI session with memory context")
    parser.add_argument("--quick", action="store_true", help="Quick summary only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    context = init_session(quick=args.quick, as_json=args.json)
    print_context(context, as_json=args.json)


if __name__ == "__main__":
    main()
