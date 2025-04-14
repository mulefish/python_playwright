import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://localhost:4200/signup")

        async def select_last_option(testid: str):
            # Click the dropdown arrow near the input
            dropdown_control = page.locator(f'[data-testid="{testid}"]').locator('xpath=../../../..')
            await dropdown_control.click()

            # Wait for the dropdown menu to appear
            await page.wait_for_selector('.q-menu .q-item', timeout=2000)

            # Find all q-item options and click the last one
            options = page.locator('.q-menu .q-item')
            count = await options.count()
            if count > 0:
                await options.nth(count - 1).click()
            else:
                print(f"No options found for {testid}")

        await select_last_option("selectedMonth")
        await select_last_option("selectedDay")
        await select_last_option("selectedYear")

        await page.wait_for_timeout(3000)
        await browser.close()

asyncio.run(run())
