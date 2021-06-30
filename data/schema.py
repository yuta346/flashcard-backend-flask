import sqlite3

def schema(dbpath="flashcard.db"):
    with sqlite3.connect(dbpath) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE words(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            word VARCHAR UNIQUE NOT NULL,
            speech VARCHAR(16),
            definition VARCHAR,
            example VARCHAR
        );""")


if __name__ == "__main__":
    schema()