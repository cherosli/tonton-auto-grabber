import os
import asyncio
from playwright.async_api import async_playwright

EMAIL = os.getenv("TONTON_EMAIL")
PASSWORD = os.getenv("TONTON_PASSWORD")

async def run():
    print("[INFO] Launching browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context()
            page = await context.new_page()
            print("[INFO] Going to login page...")
            await page.goto("https://www.tonton.com.my/login", timeout=60000)

            print("[INFO] Typing credentials...")
            await page.fill('input[name="email"]', EMAIL)
            await page.fill('input[name="password"]', PASSWORD)
            await page.click("text=Login")
            await page.wait_for_load_state('networkidle', timeout=60000)

            print("[INFO] Navigating to Live TV TV3...")
            await page.goto("https://www.tonton.com.my/live-tv/tv3", timeout=60000)
            await page.wait_for_timeout(5000)

            print("[INFO] Extracting m3u8 link...")
            frame = page.main_frame
            content = await frame.content()
            m3u8_lines = [line for line in content.split('"') if "master_1080.m3u8" in line]

            if m3u8_lines:
                with open("tv3_latest.m3u8.txt", "w") as f:
                    f.write(m3u8_lines[0])
                print("[SUCCESS] Link grabbed:", m3u8_lines[0])
            else:
                print("[FAIL] m3u8 link not found.")

            await browser.close()
    except Exception as e:
        print("[ERROR]", e)

asyncio.run(run())
