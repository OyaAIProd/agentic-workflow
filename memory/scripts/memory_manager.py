#!/usr/bin/env python3
"""
Agentic Workflow - Memory Manager
Persistent memory system for AI agents with PostgreSQL backend.

Author: Julien GELEE
License: MIT

Usage:
    from memory_manager import MemoryManager

    mm = MemoryManager()
    mm.log_action("code_review", "Reviewed authentication module")
    mm.log_error("TypeError", "Cannot read property of undefined", "Add null check")
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("Warning: psycopg2 not installed. Run: pip install psycopg2-binary")
    psycopg2 = None


class MemoryManager:
    """PostgreSQL-backed memory persistence for AI agents."""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        database: str = None,
        user: str = None,
        password: str = None
    ):
        """Initialize with database connection parameters.

        Parameters can be passed directly or via environment variables:
        - MEMORY_DB_HOST (default: localhost)
        - MEMORY_DB_PORT (default: 5432)
        - MEMORY_DB_NAME (default: ai_memory)
        - MEMORY_DB_USER (default: ai_agent)
        - MEMORY_DB_PASSWORD (required)
        """
        self.config = {
            "host": host or os.getenv("MEMORY_DB_HOST", "localhost"),
            "port": port or int(os.getenv("MEMORY_DB_PORT", "5432")),
            "database": database or os.getenv("MEMORY_DB_NAME", "ai_memory"),
            "user": user or os.getenv("MEMORY_DB_USER", "ai_agent"),
            "password": password or os.getenv("MEMORY_DB_PASSWORD"),
        }

        if not self.config["password"]:
            raise ValueError("Database password required. Set MEMORY_DB_PASSWORD environment variable.")

        self._conn = None

    def _get_connection(self):
        """Get or create database connection."""
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(**self.config)
        return self._conn

    def _execute(self, query: str, params: tuple = None, fetch: bool = True) -> Any:
        """Execute a query and return results."""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
                return cur.rowcount
        except Exception as e:
            conn.rollback()
            raise e

    # === Session Management ===

    def start_session(self, summary: str = None) -> UUID:
        """Start a new session and return its ID."""
        result = self._execute(
            "INSERT INTO sessions (summary) VALUES (%s) RETURNING id",
            (summary,)
        )
        return result[0]["id"] if result else None

    def end_session(self, session_id: UUID, summary: str = None):
        """End a session with optional summary."""
        self._execute(
            "UPDATE sessions SET ended_at = NOW(), summary = COALESCE(%s, summary) WHERE id = %s",
            (summary, str(session_id)),
            fetch=False
        )

    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Get recent sessions."""
        return self._execute(
            "SELECT * FROM sessions ORDER BY started_at DESC LIMIT %s",
            (limit,)
        )

    # === Action Logging ===

    def log_action(
        self,
        action_type: str,
        description: str,
        target_path: str = None,
        status: str = "completed",
        metadata: Dict = None,
        keywords: List[str] = None,
        session_id: UUID = None
    ) -> UUID:
        """Log an action and return its ID."""
        result = self._execute(
            """INSERT INTO actions
               (session_id, action_type, description, target_path, status, metadata, keywords)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                str(session_id) if session_id else None,
                action_type,
                description,
                target_path,
                status,
                json.dumps(metadata or {}),
                keywords
            )
        )
        return result[0]["id"] if result else None

    def get_recent_actions(self, limit: int = 20, action_type: str = None) -> List[Dict]:
        """Get recent actions, optionally filtered by type."""
        if action_type:
            return self._execute(
                "SELECT * FROM actions WHERE action_type = %s ORDER BY created_at DESC LIMIT %s",
                (action_type, limit)
            )
        return self._execute(
            "SELECT * FROM actions ORDER BY created_at DESC LIMIT %s",
            (limit,)
        )

    # === Error Learning ===

    def log_error(
        self,
        error_type: str,
        error_message: str,
        solution: str,
        related_files: List[str] = None,
        metadata: Dict = None
    ) -> UUID:
        """Log an error and its solution for future reference."""
        result = self._execute(
            """INSERT INTO error_solutions
               (error_type, error_message, solution, related_files, metadata)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING id""",
            (
                error_type,
                error_message,
                solution,
                related_files,
                json.dumps(metadata or {})
            )
        )
        return result[0]["id"] if result else None

    def find_similar_error(self, error_message: str, limit: int = 5) -> List[Dict]:
        """Find similar errors that have been solved before."""
        # Search by keywords in the error message
        keywords = [w for w in error_message.split() if len(w) > 3][:5]

        if not keywords:
            return []

        # Build search pattern
        pattern = "%".join(keywords)

        return self._execute(
            """SELECT * FROM error_solutions
               WHERE error_message ILIKE %s OR error_type ILIKE %s
               ORDER BY occurrences DESC, created_at DESC
               LIMIT %s""",
            (f"%{pattern}%", f"%{pattern}%", limit)
        )

    def mark_solution_worked(self, error_id: UUID, worked: bool = True):
        """Mark whether a solution worked."""
        self._execute(
            """UPDATE error_solutions
               SET solution_worked = %s,
                   occurrences = occurrences + 1,
                   updated_at = NOW()
               WHERE id = %s""",
            (worked, str(error_id)),
            fetch=False
        )

    # === Context Management ===

    def set_context(
        self,
        key: str,
        value: str,
        category: str = "general",
        importance: int = 5
    ):
        """Set a context value (upsert)."""
        self._execute(
            """INSERT INTO context (key, value, category, importance)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (key) DO UPDATE
               SET value = EXCLUDED.value,
                   category = EXCLUDED.category,
                   importance = EXCLUDED.importance,
                   updated_at = NOW()""",
            (key, value, category, importance),
            fetch=False
        )

    def get_context(self, key: str) -> Optional[str]:
        """Get a context value by key."""
        result = self._execute(
            "SELECT value FROM context WHERE key = %s",
            (key,)
        )
        return result[0]["value"] if result else None

    def get_all_context(self, category: str = None, min_importance: int = 1) -> List[Dict]:
        """Get all context values, optionally filtered."""
        if category:
            return self._execute(
                "SELECT * FROM context WHERE category = %s AND importance >= %s ORDER BY importance DESC",
                (category, min_importance)
            )
        return self._execute(
            "SELECT * FROM context WHERE importance >= %s ORDER BY importance DESC",
            (min_importance,)
        )

    # === Knowledge Base ===

    def add_knowledge(
        self,
        topic: str,
        content: str,
        source: str = None,
        confidence: float = 0.8,
        tags: List[str] = None
    ) -> UUID:
        """Add knowledge to the base."""
        result = self._execute(
            """INSERT INTO knowledge_base (topic, content, source, confidence, tags)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING id""",
            (topic, content, source, confidence, tags)
        )
        return result[0]["id"] if result else None

    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Search knowledge base using full text search."""
        return self._execute(
            """SELECT *,
                      ts_rank(to_tsvector('english', topic || ' ' || content),
                              plainto_tsquery('english', %s)) as rank
               FROM knowledge_base
               WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery('english', %s)
               ORDER BY rank DESC, confidence DESC
               LIMIT %s""",
            (query, query, limit)
        )

    # === Checkpoints ===

    def create_checkpoint(
        self,
        name: str,
        description: str = None,
        is_milestone: bool = False,
        state: Dict = None
    ) -> UUID:
        """Create a checkpoint to save progress."""
        result = self._execute(
            """INSERT INTO checkpoints (name, description, is_milestone, state)
               VALUES (%s, %s, %s, %s)
               RETURNING id""",
            (name, description, is_milestone, json.dumps(state or {}))
        )
        return result[0]["id"] if result else None

    def list_checkpoints(self, limit: int = 20, milestones_only: bool = False) -> List[Dict]:
        """List checkpoints."""
        if milestones_only:
            return self._execute(
                "SELECT * FROM checkpoints WHERE is_milestone = TRUE ORDER BY created_at DESC LIMIT %s",
                (limit,)
            )
        return self._execute(
            "SELECT * FROM checkpoints ORDER BY created_at DESC LIMIT %s",
            (limit,)
        )

    # === Global Search ===

    def global_search(self, query: str, entity_types: List[str] = None) -> Dict[str, List[Dict]]:
        """Search across all tables."""
        results = {}

        types = entity_types or ["actions", "errors", "knowledge", "context"]

        if "actions" in types:
            results["actions"] = self._execute(
                "SELECT * FROM actions WHERE description ILIKE %s ORDER BY created_at DESC LIMIT 10",
                (f"%{query}%",)
            )

        if "errors" in types:
            results["errors"] = self._execute(
                "SELECT * FROM error_solutions WHERE error_message ILIKE %s OR solution ILIKE %s LIMIT 10",
                (f"%{query}%", f"%{query}%")
            )

        if "knowledge" in types:
            results["knowledge"] = self.search_knowledge(query, 10)

        if "context" in types:
            results["context"] = self._execute(
                "SELECT * FROM context WHERE key ILIKE %s OR value ILIKE %s LIMIT 10",
                (f"%{query}%", f"%{query}%")
            )

        return results

    def close(self):
        """Close database connection."""
        if self._conn and not self._conn.closed:
            self._conn.close()


# Convenience functions for direct use
_default_manager = None

def get_manager() -> MemoryManager:
    """Get or create the default memory manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = MemoryManager()
    return _default_manager

def log_action(action_type: str, description: str, **kwargs):
    """Log an action using the default manager."""
    return get_manager().log_action(action_type, description, **kwargs)

def log_error(error_type: str, error_message: str, solution: str, **kwargs):
    """Log an error using the default manager."""
    return get_manager().log_error(error_type, error_message, solution, **kwargs)

def find_similar_error(error_message: str):
    """Find similar errors using the default manager."""
    return get_manager().find_similar_error(error_message)

def set_context(key: str, value: str, **kwargs):
    """Set context using the default manager."""
    return get_manager().set_context(key, value, **kwargs)

def get_context(key: str):
    """Get context using the default manager."""
    return get_manager().get_context(key)

def create_checkpoint(name: str, **kwargs):
    """Create checkpoint using the default manager."""
    return get_manager().create_checkpoint(name, **kwargs)


if __name__ == "__main__":
    # Test connection
    try:
        mm = MemoryManager()
        print("Memory Manager initialized successfully")
        print(f"Connected to: {mm.config['host']}:{mm.config['port']}/{mm.config['database']}")
    except Exception as e:
        print(f"Error: {e}")
