import asyncio
import re
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    url = "https://www.booking.com/hotel/es/kampion-by-people-rentals.es.html?label=es-es-booking-desktop-onknyt5TBrS8m9RnGd*6fgS652829001115%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9211653%3Ali%3Adec%3Adm&aid=2311236&ucfs=1&arphpl=1&checkin=2026-06-11&checkout=2026-06-14"
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES",
            timezone_id="Europe/Madrid"
        )
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        
        html = await page.content()
        
        print("--- COINCIDENCIAS DE GESTIONADO / ANFITRION ---")
        for line in html.splitlines():
            if any(term in line.lower() for term in ["gestionado", "anfitrión", "anfitriona", "host info", "anfitrión-nombre", "host-name", "people rentals"]):
                # Truncar línea para no inundar el output
                print(line.strip()[:150])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
