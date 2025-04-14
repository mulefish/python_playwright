import asyncio
import sqlite3
from playwright.async_api import async_playwright

async def run():
    # Setup database connection
    conn = sqlite3.connect("pages.db")
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            rowId INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT,
            id TEXT,
            tag TEXT,
            cmd TEXT
        )
    """)

    # name = "signup"
    # name = "eligibility"
    # name = "legalname"
    name = "namematch"

    # Delete existing rows for this page name
    cursor.execute("DELETE FROM pages WHERE page = ?", (name,))
    print(f"Deleted existing rows for page: {name}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        url = "http://localhost:4200/" + name
        await page.goto(url)
        await page.wait_for_timeout(3000)

        elements = await page.query_selector_all("[data-test-id], [data-testid]")
        ignore = ['DIV', 'P', 'HEADER', 'LABEL', 'H2', 'I', 'FORM']

        for el in elements:
            testid = await el.get_attribute("data-test-id") or await el.get_attribute("data-testid")
            tag = await el.evaluate("(node) => node.tagName")
            if tag not in ignore:
                print(f"{name}, {testid}, {tag}")
                # Insert into database
                cursor.execute(
                    "INSERT INTO pages (page, id, tag, cmd) VALUES (?, ?, ?, ?)",
                    (name, testid, tag, "")
                )

        await browser.close()

    # Save and close database
    conn.commit()
    conn.close()

asyncio.run(run())
