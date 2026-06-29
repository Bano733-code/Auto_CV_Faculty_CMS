import sqlite3
import json

conn = sqlite3.connect("faculty.db", check_same_thread=False)
cur = conn.cursor()

def create_tables():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        university TEXT,
        slug TEXT UNIQUE,
        data TEXT
    )
    """)
    conn.commit()


def save_or_update_teacher(name, university, slug, data):

    cur.execute("SELECT id FROM teachers WHERE slug=?", (slug,))
    exists = cur.fetchone()

    if exists:
        cur.execute("""
        UPDATE teachers
        SET name=?, university=?, data=?
        WHERE slug=?
        """, (name, university, json.dumps(data), slug))
    else:
        cur.execute("""
        INSERT INTO teachers (name, university, slug, data)
        VALUES (?, ?, ?, ?)
        """, (name, university, slug, json.dumps(data)))

    conn.commit()


def get_teacher_by_slug(slug):

    cur.execute("SELECT * FROM teachers WHERE slug=?", (slug,))
    row = cur.fetchone()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "university": row[2],
            "slug": row[3],
            "data": json.loads(row[4])
        }
    return None


def get_universities():

    cur.execute("SELECT DISTINCT university FROM teachers")
    rows = cur.fetchall()

    return [r[0] for r in rows]
