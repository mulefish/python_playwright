import sqlite3

def print_all_pages():
    # Connect to the database
    conn = sqlite3.connect("pages.db")
    cursor = conn.cursor()

    # Query all rows
    cursor.execute("SELECT * FROM pages")
    rows = cursor.fetchall()

    # Print rows
    print("rowId | page | id | tag | cmd | input")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

    # Close connection
    conn.close()

if __name__ == "__main__":
    print_all_pages()
