import asyncio
import re
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    url = "https://www.airbnb.es/rooms/1263042088195534687?check_in=2026-07-23&check_out=2026-07-26&photo_id=2008242867"
    print("Iniciando Playwright con Stealth...")
    try:
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            print("Navegando a la URL...")
            await page.goto(url, timeout=25000, wait_until="domcontentloaded")
            
            title = await page.title()
            print(f"Título obtenido: {title}")
            
            # Buscar en el contenido
            html = await page.content()
            
            # Guardar el HTML
            with open("airbnb_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("HTML guardado en airbnb_page.html.")
            
            # Buscar el script data-state
            state_match = re.search(r'<script id="data-state"[^>]*>(.*?)</script>', html, re.DOTALL)
            if state_match:
                print("¡Encontrado script id=data-state!")
                state_json = json.loads(state_match.group(1))
                with open("data_state.json", "w", encoding="utf-8") as f:
                    json.dump(state_json, f, indent=2)
                print("Guardado data_state.json.")
            else:
                print("No se encontró script id=data-state.")
            
            await browser.close()
    except Exception as e:
        print(f"Error en la ejecución: {e}")

if __name__ == "__main__":
    asyncio.run(main())
