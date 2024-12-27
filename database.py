import sqlite3
from typing import Dict


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    complaint TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_complaint(self, data: Dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                INSERT INTO complaints (name, contact, complaint)
                VALUES (?, ?, ?)
            """, (
                data['name'],
                data['contact'],
                data['complaint']
            ))
            conn.commit()
