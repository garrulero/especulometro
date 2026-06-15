import asyncio
from playwright.async_api import async_playwright
import re

async def test_profile():
    url = "https://www.airbnb.es/rooms/1633340908045094078?check_in=2026-06-25&check_out=2026-06-28"
    print(f"Testing URL: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        links = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a')).filter(a => a.href && (a.href.includes('/users/show') || a.href.includes('/users/profile'))).map(a => ({href: a.href, text: a.innerText, parentText: a.parentElement.innerText.substring(0, 50)}));
        }''')
        
        print("\n--- PROFILE LINKS ---")
        for link in links:
            print(link)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_profile())
