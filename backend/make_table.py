import sqlite3

conn = sqlite3.connect("pages.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pages (
    rowId INTEGER PRIMARY KEY AUTOINCREMENT,
    page TEXT,
    id TEXT,
    tag TEXT,
    cmd TEXT, 
    input TEXT           
)
""")

conn.commit()
conn.close()

print("SQLite table 'pages' created successfully.")
