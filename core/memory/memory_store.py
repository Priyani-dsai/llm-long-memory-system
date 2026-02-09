"""
Memory store module.

Responsible for persisting and retrieving memory objects.
This module contains NO business logic.
"""

import sqlite3
import json
from typing import List, Dict, Optional

DB_PATH = "storage/symbolic_memory.db"


def _get_connection() -> sqlite3.Connection:
    """
    Returns a SQLite connection with row-level access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _initialize_db() -> None:
    """
    Initializes the memory table if it does not exist.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            memory_id TEXT PRIMARY KEY,
            type TEXT,
            domain TEXT,
            status TEXT,
            origin_turn INTEGER,
            last_used_turn INTEGER,
            confidence REAL,
            memory_json TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# Initialize database on import
_initialize_db()


def store_memory(memory: Dict) -> None:
    """
    Persists a new memory object.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO memories (
            memory_id,
            type,
            domain,
            status,
            origin_turn,
            last_used_turn,
            confidence,
            memory_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            memory["memory_id"],
            memory["type"],
            memory["domain"],
            memory["status"],
            memory["origin_turn"],
            memory["last_used_turn"],
            memory["confidence"],
            json.dumps(memory),
        ),
    )

    conn.commit()
    conn.close()


def update_memory(memory_id: str, updates: Dict) -> None:
    """
    Updates fields of an existing memory object.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT memory_json FROM memories WHERE memory_id = ?",
        (memory_id,),
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return

    memory = json.loads(row["memory_json"])
    memory.update(updates)

    cursor.execute(
        """
        UPDATE memories
        SET status = ?,
            last_used_turn = ?,
            confidence = ?,
            memory_json = ?
        WHERE memory_id = ?
        """,
        (
            memory.get("status"),
            memory.get("last_used_turn"),
            memory.get("confidence"),
            json.dumps(memory),
            memory_id,
        ),
    )

    conn.commit()
    conn.close()


def fetch_memories(
    *,
    types: List[str],
    domains: List[str],
    status: str = "active"
) -> List[Dict]:
    """
    Fetches memory objects matching the given filters.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    query = """
        SELECT memory_json FROM memories
        WHERE status = ?
    """
    params: List = [status]

    if types:
        query += " AND type IN ({})".format(",".join("?" * len(types)))
        params.extend(types)

    if domains:
        query += " AND domain IN ({})".format(",".join("?" * len(domains)))
        params.extend(domains)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [json.loads(row["memory_json"]) for row in rows]


def mark_memory_inactive(memory_id: str) -> None:
    """
    Marks a memory object as inactive.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE memories
        SET status = 'inactive'
        WHERE memory_id = ?
        """,
        (memory_id,),
    )

    conn.commit()
    conn.close()
