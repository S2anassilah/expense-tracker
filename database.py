import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "expenses.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL
                    CHECK(kind IN ('Income', 'Expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT DEFAULT ''
            )
        """)


def add_transaction(kind, amount, category, date, description):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO transactions
            (kind, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (kind, amount, category, date, description))


def get_transactions():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM transactions
            ORDER BY date DESC, id DESC
        """).fetchall()

    return [dict(row) for row in rows]


def delete_transaction(transaction_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )