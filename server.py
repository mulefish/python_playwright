from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "pages.db"

@app.route('/')
def index():
    # Fetch unique pages from SQLite
    pages = []
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT page FROM pages")
        pages = [row[0] for row in cursor.fetchall()]
        conn.close()

    return render_template("index.html", pages=pages)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    text = data.get("message", "")
    return jsonify({
        "original": text,
        "length": len(text),
        "upper": text.upper()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)
