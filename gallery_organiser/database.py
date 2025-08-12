from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple

# Database path can be configured via GALLERY_DB environment variable
DB_PATH = Path(os.environ.get("GALLERY_DB", Path(__file__).resolve().parents[1] / "gallery.db"))


def init_db() -> None:
    """Initialise the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS images (path TEXT PRIMARY KEY, label TEXT)"
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            name TEXT,
            bbox TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def store_label(path: str, label: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("REPLACE INTO images(path, label) VALUES (?, ?)", (path, label))
    conn.commit()
    conn.close()


def add_face_tag(path: str, name: str, bbox: Iterable[int]) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO faces(image_path, name, bbox) VALUES (?, ?, ?)",
        (path, name, json.dumps(list(bbox))),
    )
    conn.commit()
    conn.close()


def search_by_name(name: str) -> List[str]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT image_path FROM faces WHERE name = ?", (name,))
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows
