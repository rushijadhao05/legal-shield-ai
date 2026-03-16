import sqlite3
from datetime import datetime

DB_NAME = "legal_shield.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        incident_text TEXT NOT NULL,
        status TEXT NOT NULL,
        severity TEXT NOT NULL,
        laws TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_complaint(name, contact, incident_text, status, severity, laws):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    laws_text = ", ".join(laws) if laws else ""

    cursor.execute("""
    INSERT INTO complaints (name, contact, incident_text, status, severity, laws, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, contact, incident_text, status, severity, laws_text, created_at))

    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return complaint_id, created_at


def get_all_complaints():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    complaints = []
    for row in rows:
        complaints.append({
            "id": row["id"],
            "name": row["name"],
            "contact": row["contact"],
            "incident_text": row["incident_text"],
            "status": row["status"],
            "severity": row["severity"],
            "laws": row["laws"].split(", ") if row["laws"] else [],
            "created_at": row["created_at"]
        })

    return complaints


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
