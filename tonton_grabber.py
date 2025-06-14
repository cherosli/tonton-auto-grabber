import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    email = os.getenv("TONTON_EMAIL")
    password = os.getenv("TONTON_PASSWORD")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.tonton.com.my/")
        await page.click("text=Login")
        await page.fill('input[type="email"]', email)
        await page.fill('input[type="password"]', password)
        await page.click('button:has-text("Log In")')
        await page.wait_for_url("https://www.tonton.com.my/home")

        await page.goto("https://www.tonton.com.my/live-tv/tv3")
        await page.wait_for_selector("video", timeout=10000)

        m3u8_url = await page.evaluate('''() => {
            const video = document.querySelector("video");
            return video ? video.src : null;
        }''')

        print(f"[TV3] {m3u8_url}")
        await browser.close()

asyncio.run(run())
