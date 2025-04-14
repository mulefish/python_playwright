from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import asyncio
from playwright_runner import scrape_page

app = Flask(__name__)
DB_PATH = "pages.db"

@app.route('/api/pages')
def get_pages():
    pages = []
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT page FROM pages")
        pages = [row[0] for row in cursor.fetchall()]
        conn.close()
    return jsonify(pages)

@app.route('/echo', methods=['POST'])
def echo():
    print("LINE 53!!")

    data = request.get_json()
    text = data.get("message", "")
    return jsonify({
        "original": text,
        "length": len(text),
        "upper": text.upper()
    })

@app.route('/doPlaywright', methods=['POST'])
def do_playwright():
    data = request.get_json()
    page_name = data.get("page", "")
    print(f"Running Playwright for page: {page_name}")

    results = asyncio.run(scrape_page(page_name))
    return jsonify({
        "page": page_name,
        "found": results
    })

if __name__ == '__main__':
    print("LINE 65!!")
    app.run(debug=True, port=5050)
