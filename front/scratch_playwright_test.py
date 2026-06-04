import asyncio
import re
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    url = "https://www.airbnb.es/rooms/1263042088195534687?check_in=2026-07-23&check_out=2026-07-26&photo_id=2008242867&source_impression_id=p3_1780561714_P3Bo06iMpNVH0CjW&previous_page_section_name=1000"
    print("Iniciando Playwright con Stealth...")
    async with Stealth().use_async(async_playwright()) as p:
        # Iniciamos chromium
        browser = await p.chromium.launch(headless=True)
        # Es bueno definir un User-Agent moderno para evitar bloqueos
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES",
            timezone_id="Europe/Madrid"
        )
        page = await context.new_page()
        
        print("Navegando a la URL de Airbnb...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("Navegación completada. Esperando a que se carguen los datos dinámicos (8 segundos)...")
        await page.wait_for_timeout(8000)
        
        # Guardar una captura de pantalla para verificar visualmente qué se ve (muy útil para depurar si hay captcha o si cargó bien)
        await page.screenshot(path="airbnb_screenshot.png")
        print("Captura de pantalla guardada en airbnb_screenshot.png")
        
        html = await page.content()
        with open("airbnb_page_dynamic.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML dinámico guardado en airbnb_page_dynamic.html.")
        
        # Extraer el título
        title = await page.title()
        print(f"Título real de la página: {title}")
        
        # Extraer textos visibles de interés en el DOM
        # 1. Intentar buscar el precio en la página
        # En Airbnb, el precio por noche suele estar en un div o span con clases que cambian pero a menudo tiene un formato como "_1y74zjx" o similar, o se puede buscar por el texto "noche" o "€".
        # Vamos a evaluar un script en la página para extraer textos que parezcan precios.
        prices = await page.evaluate('''() => {
            const results = [];
            // Buscar spans o divs que contengan "€"
            const elements = document.querySelectorAll('span, div');
            for (const el of elements) {
                const text = el.innerText || '';
                if (text.includes('€') && text.length < 30) {
                    results.push(text.trim());
                }
            }
            return [...new Set(results)];
        }''')
        print(f"Textos con '€' encontrados en el DOM: {prices[:20]}")
        
        # 2. Intentar buscar información del host (anfitrión)
        host_texts = await page.evaluate('''() => {
            const results = [];
            const elements = document.querySelectorAll('h1, h2, h3, h4, div, span');
            for (const el of elements) {
                const text = el.innerText || '';
                if ((text.toLowerCase().includes('anfitrión') || text.toLowerCase().includes('host')) && text.length < 100) {
                    results.push(text.trim());
                }
            }
            return [...new Set(results)];
        }''')
        print(f"Textos con 'anfitrión' o 'host' encontrados: {host_texts[:15]}")
        
        # 3. Intentar buscar disponibilidad o rango de fechas
        date_texts = await page.evaluate('''() => {
            const results = [];
            const elements = document.querySelectorAll('div, span');
            for (const el of elements) {
                const text = el.innerText || '';
                if ((text.includes('jul') || text.includes('23') || text.includes('26')) && text.length < 50) {
                    results.push(text.trim());
                }
            }
            return [...new Set(results)];
        }''')
        print(f"Textos con fechas encontrados: {date_texts[:10]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
