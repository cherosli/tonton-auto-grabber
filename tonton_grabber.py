import asyncio
from playwright.async_api import async_playwright
import os

EMAIL = os.environ["TONTON_EMAIL"]
PASSWORD = os.environ["TONTON_PASSWORD"]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.tonton.com.my/")
        await page.wait_for_timeout(5000)  # bagi masa loading penuh

        # Cari button login guna selector alternatif
        await page.wait_for_selector("a[href='/login']", timeout=20000)
        await page.click("a[href='/login']")

        await page.wait_for_selector('input[name="email"]', timeout=20000)
        await page.fill('input[name="email"]', EMAIL)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')

        await page.wait_for_timeout(5000)  # tunggu lepas login

        await page.goto("https://www.tonton.com.my/live-tv")
        await page.wait_for_selector('text=TV3', timeout=15000)
        await page.click('text=TV3')

        m3u8_link = None
        async def handle_request(request):
            nonlocal m3u8_link
            if "master_1080.m3u8" in request.url:
                m3u8_link = request.url

        page.on("request", handle_request)
        await page.wait_for_timeout(10000)
        await browser.close()

        if m3u8_link:
            with open("tv3.txt", "w") as f:
                f.write(m3u8_link)

asyncio.run(run())
