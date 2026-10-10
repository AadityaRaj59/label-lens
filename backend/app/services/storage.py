import json
import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "labellens.sqlite3"
)


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DATABASE_PATH), timeout=10)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            report_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            filename TEXT,
            report_json TEXT NOT NULL
        )
    """)
    return connection


def save_report(report: dict[str, Any]) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO inspections
            (report_id, created_at, filename, report_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                report["report_id"],
                report["created_at"],
                report.get("source", {}).get("filename"),
                json.dumps(report, ensure_ascii=False),
            ),
        )


def get_report(report_id: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT report_json FROM inspections WHERE report_id = ?",
            (report_id,),
        ).fetchone()

    return json.loads(row[0]) if row else None


def list_reports(limit: int = 50) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT report_json FROM inspections
            ORDER BY created_at DESC LIMIT ?
            """,
            (max(1, min(limit, 100)),),
        ).fetchall()

    return [json.loads(row[0]) for row in rows]
