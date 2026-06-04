import asyncio
import re
import sys
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    url = "https://www.booking.com/hotel/es/kampion-by-people-rentals.es.html?label=es-es-booking-desktop-onknyt5TBrS8m9RnGd*6fgS652829001115%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9211653%3Ali%3Adec%3Adm&aid=2311236&ucfs=1&arphpl=1&checkin=2026-06-11&checkout=2026-06-14&dest_id=-373608&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=3&hapos=3&sr_order=popularity&nflt=ht_id%3D201&srpvid=73c24ce997630baa&srepoch=1780570732&all_sr_blocks=1231703702_407783969_3_0_0&highlighted_blocks=1231703702_407783969_3_0_0&matching_block_id=1231703702_407783969_3_0_0&sr_pri_blocks=1231703702_407783969_3_0_0__36915&from=searchresults"
    
    print("Iniciando Playwright con Stealth para Booking.com...")
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES",
            timezone_id="Europe/Madrid"
        )
        page = await context.new_page()
        
        print("Navegando...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("Esperando 5 segundos para carga dinámica...")
        await page.wait_for_timeout(5000)
        
        await page.screenshot(path="booking_screenshot.png")
        print("Captura guardada en booking_screenshot.png")
        
        title = await page.title()
        print(f"Título de la página: {title}")
        
        # Intentar extraer info clave (precio, nombre del host/gestor, municipio, etc.)
        dom_data = await page.evaluate('''() => {
            const data = {};
            
            // Buscar ld+json
            const ldScripts = document.querySelectorAll('script[type="application/ld+json"]');
            data.ld_types = [];
            for (const script of ldScripts) {
                try {
                    const json = JSON.parse(script.textContent);
                    data.ld_types.push(json["@type"] || json["@context"]);
                    if (json["@type"] === "Hotel" || json["@type"] === "Accommodation" || json["@type"] === "Product") {
                        data.ld_hotel = json;
                    }
                } catch(e) {}
            }
            
            // Buscar textos de precios
            const priceElements = document.querySelectorAll('.prco-val-color-indicator, .bui-price-display__value, [data-xt-back-price], .js-reservation-total-price');
            data.prices_selectors = [];
            priceElements.forEach(el => data.prices_selectors.push(el.innerText));
            
            // Textos genéricos con €
            const elements = document.querySelectorAll('span, div, td');
            const euroTexts = [];
            for (const el of elements) {
                const text = el.innerText || '';
                if (text.includes('€') && text.length < 40) {
                    euroTexts.push(text.trim());
                }
            }
            data.euro_texts = [...new Set(euroTexts)].slice(0, 30);
            
            // Buscar nombre del host / gestionado por
            const hostElements = [];
            for (const el of elements) {
                const text = el.innerText || '';
                if ((text.toLowerCase().includes('gestionado') || text.toLowerCase().includes('anfitrión') || text.toLowerCase().includes('host') || text.toLowerCase().includes('propietario')) && text.length < 150) {
                    hostElements.push(text.trim());
                }
            }
            data.host_texts = [...new Set(hostElements)].slice(0, 15);
            
            // Municipio/dirección
            const addressEl = document.querySelector('.hp_address_subtitle, #hp_address_subtitle, [data-node_tt_id="location_score_as_link"]');
            if (addressEl) {
                data.address = addressEl.innerText;
            }
            
            // Imagen principal
            const mainImg = document.querySelector('.hp-gallery-top img, #hotel_main_content img, .gallery-side-images-container img');
            if (mainImg) {
                data.image = mainImg.src;
            }
            
            return data;
        }''')
        
        print("Datos del DOM:")
        print(f"Tipos LD+JSON: {dom_data.get('ld_types')}")
        print(f"LD Hotel data: {dom_data.get('ld_hotel') is not None}")
        if dom_data.get('ld_hotel'):
            print(f"LD Hotel Keys: {list(dom_data.get('ld_hotel').keys())}")
            if 'description' in dom_data['ld_hotel']:
                print(f"LD Description: {dom_data['ld_hotel']['description'][:100]}")
            if 'address' in dom_data['ld_hotel']:
                print(f"LD Address: {dom_data['ld_hotel']['address']}")
        print(f"Precios por selectores conocidos: {dom_data.get('prices_selectors')}")
        print(f"Textos con euro encontrados: {dom_data.get('euro_texts')}")
        print(f"Textos de Host/Gestor: {dom_data.get('host_texts')}")
        print(f"Dirección: {dom_data.get('address')}")
        print(f"Imagen: {dom_data.get('image')}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
