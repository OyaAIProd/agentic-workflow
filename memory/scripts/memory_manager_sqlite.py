#!/usr/bin/env python3
"""
Agentic Workflow - Memory Manager (SQLite Backend)
Lightweight persistent memory system for AI agents using SQLite.

Author: Julien GELEE
License: MIT

Usage:
    from memory_manager_sqlite import MemoryManager

    mm = MemoryManager()  # Uses ~/.ai_memory/memory.db by default
    mm.log_action("code_review", "Reviewed authentication module")
    mm.log_error("TypeError", "Cannot read property of undefined", "Add null check")

Note: This is a lightweight alternative to the PostgreSQL version.
      Use this for personal projects or when PostgreSQL is not available.
"""

import os
import json
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


class MemoryManager:
    """SQLite-backed memory persistence for AI agents."""

    def __init__(self, db_path: str = None):
        """Initialize with database path.

        Parameters:
            db_path: Path to SQLite database file.
                     Default: ~/.ai_memory/memory.db
        """
        if db_path is None:
            memory_dir = Path.home() / ".ai_memory"
            memory_dir.mkdir(exist_ok=True)
            db_path = str(memory_dir / "memory.db")

        self.db_path = db_path
        self._conn = None
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_schema(self):
        """Initialize database schema if not exists."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                ended_at TEXT,
                summary TEXT,
                metadata TEXT DEFAULT '{}'
            )
        """)

        # Actions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                target_path TEXT,
                status TEXT DEFAULT 'completed',
                metadata TEXT DEFAULT '{}',
                keywords TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)

        # Error solutions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_solutions (
                id TEXT PRIMARY KEY,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                solution TEXT NOT NULL,
                related_files TEXT,
                solution_worked INTEGER,
                occurrences INTEGER DEFAULT 1,
                metadata TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Context table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context (
                id TEXT PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                importance INTEGER DEFAULT 5,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Knowledge base table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                confidence REAL DEFAULT 0.80,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Checkpoints table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                is_milestone INTEGER DEFAULT 0,
                state TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_actions_type ON actions(action_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_actions_created ON actions(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_error_solutions_type ON error_solutions(error_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_key ON context(key)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_category ON context(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkpoints_milestone ON checkpoints(is_milestone)")

        conn.commit()

    def _generate_uuid(self) -> str:
        """Generate a UUID string."""
        return str(uuid.uuid4())

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert sqlite3.Row to dict."""
        if row is None:
            return None
        return dict(row)

    def _rows_to_dicts(self, rows: List[sqlite3.Row]) -> List[Dict]:
        """Convert list of sqlite3.Row to list of dicts."""
        return [self._row_to_dict(row) for row in rows]

    # === Session Management ===

    def start_session(self, summary: str = None) -> str:
        """Start a new session and return its ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        session_id = self._generate_uuid()

        cursor.execute(
            "INSERT INTO sessions (id, summary) VALUES (?, ?)",
            (session_id, summary)
        )
        conn.commit()
        return session_id

    def end_session(self, session_id: str, summary: str = None):
        """End a session with optional summary."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE sessions
               SET ended_at = CURRENT_TIMESTAMP,
                   summary = COALESCE(?, summary)
               WHERE id = ?""",
            (summary, session_id)
        )
        conn.commit()

    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Get recent sessions."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM sessions ORDER BY started_at DESC LIMIT ?",
            (limit,)
        )
        return self._rows_to_dicts(cursor.fetchall())

    # === Action Logging ===

    def log_action(
        self,
        action_type: str,
        description: str,
        target_path: str = None,
        status: str = "completed",
        metadata: Dict = None,
        keywords: List[str] = None,
        session_id: str = None
    ) -> str:
        """Log an action and return its ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        action_id = self._generate_uuid()

        cursor.execute(
            """INSERT INTO actions
               (id, session_id, action_type, description, target_path, status, metadata, keywords)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                action_id,
                session_id,
                action_type,
                description,
                target_path,
                status,
                json.dumps(metadata or {}),
                json.dumps(keywords) if keywords else None
            )
        )
        conn.commit()
        return action_id

    def get_recent_actions(self, limit: int = 20, action_type: str = None) -> List[Dict]:
        """Get recent actions, optionally filtered by type."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if action_type:
            cursor.execute(
                "SELECT * FROM actions WHERE action_type = ? ORDER BY created_at DESC LIMIT ?",
                (action_type, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM actions ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
        return self._rows_to_dicts(cursor.fetchall())

    # === Error Learning ===

    def log_error(
        self,
        error_type: str,
        error_message: str,
        solution: str,
        related_files: List[str] = None,
        metadata: Dict = None
    ) -> str:
        """Log an error and its solution for future reference."""
        conn = self._get_connection()
        cursor = conn.cursor()
        error_id = self._generate_uuid()

        cursor.execute(
            """INSERT INTO error_solutions
               (id, error_type, error_message, solution, related_files, metadata)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                error_id,
                error_type,
                error_message,
                solution,
                json.dumps(related_files) if related_files else None,
                json.dumps(metadata or {})
            )
        )
        conn.commit()
        return error_id

    def find_similar_error(self, error_message: str, limit: int = 5) -> List[Dict]:
        """Find similar errors that have been solved before."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Extract keywords for search
        keywords = [w for w in error_message.split() if len(w) > 3][:5]

        if not keywords:
            return []

        # Build LIKE clauses for each keyword
        conditions = []
        params = []
        for kw in keywords:
            conditions.append("(error_message LIKE ? OR error_type LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])

        query = f"""
            SELECT * FROM error_solutions
            WHERE {" OR ".join(conditions)}
            ORDER BY occurrences DESC, created_at DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, params)
        return self._rows_to_dicts(cursor.fetchall())

    def mark_solution_worked(self, error_id: str, worked: bool = True):
        """Mark whether a solution worked."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE error_solutions
               SET solution_worked = ?,
                   occurrences = occurrences + 1,
                   updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (1 if worked else 0, error_id)
        )
        conn.commit()

    # === Context Management ===

    def set_context(
        self,
        key: str,
        value: str,
        category: str = "general",
        importance: int = 5
    ):
        """Set a context value (upsert)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO context (id, key, value, category, importance)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET
                   value = excluded.value,
                   category = excluded.category,
                   importance = excluded.importance,
                   updated_at = CURRENT_TIMESTAMP""",
            (self._generate_uuid(), key, value, category, importance)
        )
        conn.commit()

    def get_context(self, key: str) -> Optional[str]:
        """Get a context value by key."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM context WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else None

    def get_all_context(self, category: str = None, min_importance: int = 1) -> List[Dict]:
        """Get all context values, optionally filtered."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if category:
            cursor.execute(
                "SELECT * FROM context WHERE category = ? AND importance >= ? ORDER BY importance DESC",
                (category, min_importance)
            )
        else:
            cursor.execute(
                "SELECT * FROM context WHERE importance >= ? ORDER BY importance DESC",
                (min_importance,)
            )
        return self._rows_to_dicts(cursor.fetchall())

    # === Knowledge Base ===

    def add_knowledge(
        self,
        topic: str,
        content: str,
        source: str = None,
        confidence: float = 0.8,
        tags: List[str] = None
    ) -> str:
        """Add knowledge to the base."""
        conn = self._get_connection()
        cursor = conn.cursor()
        knowledge_id = self._generate_uuid()

        cursor.execute(
            """INSERT INTO knowledge_base (id, topic, content, source, confidence, tags)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                knowledge_id,
                topic,
                content,
                source,
                confidence,
                json.dumps(tags) if tags else None
            )
        )
        conn.commit()
        return knowledge_id

    def search_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Search knowledge base using LIKE (SQLite doesn't have full-text by default)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Simple keyword search
        keywords = query.split()
        if not keywords:
            return []

        conditions = []
        params = []
        for kw in keywords:
            conditions.append("(topic LIKE ? OR content LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])

        query_sql = f"""
            SELECT * FROM knowledge_base
            WHERE {" AND ".join(conditions)}
            ORDER BY confidence DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query_sql, params)
        return self._rows_to_dicts(cursor.fetchall())

    # === Checkpoints ===

    def create_checkpoint(
        self,
        name: str,
        description: str = None,
        is_milestone: bool = False,
        state: Dict = None
    ) -> str:
        """Create a checkpoint to save progress."""
        conn = self._get_connection()
        cursor = conn.cursor()
        checkpoint_id = self._generate_uuid()

        cursor.execute(
            """INSERT INTO checkpoints (id, name, description, is_milestone, state)
               VALUES (?, ?, ?, ?, ?)""",
            (
                checkpoint_id,
                name,
                description,
                1 if is_milestone else 0,
                json.dumps(state or {})
            )
        )
        conn.commit()
        return checkpoint_id

    def list_checkpoints(self, limit: int = 20, milestones_only: bool = False) -> List[Dict]:
        """List checkpoints."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if milestones_only:
            cursor.execute(
                "SELECT * FROM checkpoints WHERE is_milestone = 1 ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
        else:
            cursor.execute(
                "SELECT * FROM checkpoints ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
        return self._rows_to_dicts(cursor.fetchall())

    # === Global Search ===

    def global_search(self, query: str, entity_types: List[str] = None) -> Dict[str, List[Dict]]:
        """Search across all tables."""
        results = {}
        types = entity_types or ["actions", "errors", "knowledge", "context"]

        if "actions" in types:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM actions WHERE description LIKE ? ORDER BY created_at DESC LIMIT 10",
                (f"%{query}%",)
            )
            results["actions"] = self._rows_to_dicts(cursor.fetchall())

        if "errors" in types:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM error_solutions WHERE error_message LIKE ? OR solution LIKE ? LIMIT 10",
                (f"%{query}%", f"%{query}%")
            )
            results["errors"] = self._rows_to_dicts(cursor.fetchall())

        if "knowledge" in types:
            results["knowledge"] = self.search_knowledge(query, 10)

        if "context" in types:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM context WHERE key LIKE ? OR value LIKE ? LIMIT 10",
                (f"%{query}%", f"%{query}%")
            )
            results["context"] = self._rows_to_dicts(cursor.fetchall())

        return results

    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


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
        print("SQLite Memory Manager initialized successfully")
        print(f"Database: {mm.db_path}")

        # Quick test
        mm.set_context("test_key", "test_value", importance=5)
        value = mm.get_context("test_key")
        print(f"Test context: {value}")

        mm.close()
    except Exception as e:
        print(f"Error: {e}")
