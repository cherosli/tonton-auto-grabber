
import os
import asyncio
from playwright.async_api import async_playwright

TONTON_EMAIL = os.getenv("TONTON_EMAIL")
TONTON_PASSWORD = os.getenv("TONTON_PASSWORD")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("🔄 Membuka halaman login Tonton...")
        await page.goto("https://www.tonton.com.my/login")

        await page.fill('input[name="email"]', TONTON_EMAIL)
        await page.fill('input[name="password"]', TONTON_PASSWORD)
        await page.click('button[type="submit"]')

        print("⏳ Tunggu redirect lepas login...")
        await page.wait_for_timeout(5000)

        print("🔄 Pergi ke halaman Live TV (TV3)...")
        await page.goto("https://www.tonton.com.my/live-tv/tv3")

        print("⏳ Tunggu video player load...")
        await page.wait_for_selector("video", timeout=10000)

        m3u8_url = await page.eval_on_selector("video", "el => el.src")

        if m3u8_url:
            print(f"✅ Link berjaya dapat: {m3u8_url}")
        else:
            print("❌ Gagal dapatkan link video.")

        with open("tv3.m3u8.txt", "w") as f:
            f.write(m3u8_url if m3u8_url else "FAILED")

        await browser.close()

asyncio.run(run())
