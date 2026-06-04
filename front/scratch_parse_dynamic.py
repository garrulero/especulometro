import re
import json
from bs4 import BeautifulSoup

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("--- ANALIZANDO HTML DINÁMICO ---")

# 1. Título
title_tag = soup.find("title")
title = title_tag.text if title_tag else ""
print(f"Título: {title}")

# 2. Municipio / Ciudad
# En el título: "... en Bilbao, Euskadi ..." -> Bilbao
# O en el LD+JSON. Vamos a ver si en los LD+JSON del HTML dinámico sigue estando addressLocality
scripts_ld = soup.find_all("script", type="application/ld+json")
municipio = None
for s in scripts_ld:
    try:
        data = json.loads(s.string)
        if isinstance(data, dict):
            if "@type" in data and data["@type"] == "VacationRental":
                if "address" in data and "addressLocality" in data["address"]:
                    municipio = data["address"]["addressLocality"]
    except:
        pass
print(f"Municipio extraído de LD+JSON: {municipio}")

# Si no, de título
if not municipio and " en " in title:
    parts = title.split(" en ")
    if len(parts) > 1:
        # P.ej. "Bilbao, Euskadi, España"
        subparts = parts[1].split(",")
        municipio = subparts[0].strip()
print(f"Municipio final: {municipio}")

# 3. Anfitrión / Host
# Busquemos "Anfitrión: [Nombre]" o "Host: [Nombre]" o similar
host_name = None
host_match = re.search(r'Anfitrión:\s*([A-Z][a-z]+)', html)
if host_match:
    host_name = host_match.group(1)
else:
    # Buscar en el texto plano del body
    text = soup.get_text()
    host_match_text = re.search(r'(?:Anfitrión|Host):\s*([A-Z][a-záéíóúñ]+)', text, re.IGNORECASE)
    if host_match_text:
        host_name = host_match_text.group(1)
print(f"Nombre del anfitrión: {host_name}")

# 4. Listings del anfitrión (listingsCount)
# Busquemos en el texto plano cosas como "[N] evaluaciones" o si hay mención de listings, 
# o busquemos en los JSON dinámicos si se cargó el listingsCount
listings_count = 1
# Busquemos si en el HTML hay referencias al número de anuncios del anfitrión
# Por ejemplo, "anuncios", "alojamientos", "listings", "listingsCount"
listings_matches = re.findall(r'(\d+)\s*(?:anuncio|alojamiento|anuncios|alojamientos|listings)', html, re.IGNORECASE)
print(f"Posibles conteos de anuncios en HTML: {listings_matches}")

# 5. Imagen
# Buscar og:image
og_image = soup.find("meta", property="og:image")
image_url = og_image["content"] if og_image else None
if not image_url:
    # Buscar primer enlace de imagen de muscache
    imgs = soup.find_all("img")
    for img in imgs:
        src = img.get("src", "")
        if "muscache.com/im/pictures" in src:
            image_url = src
            break
print(f"Imagen: {image_url}")

# 6. Precio por noche
# Airbnb suele renderizar el precio por noche en un elemento con estructura especial.
# Busquemos cadenas como "XXX €" o similar en el HTML y tratemos de encontrar el precio.
# En el script de arriba vimos que en el DOM estaba "637 € en total".
# Busquemos también si hay algún patrón tipo "XXX €\xa0noche" o "XXX € por noche"
precios_noche = re.findall(r'(\d+[\.,]?\d*)\s*(?:€|\$|EUR)\xa0*(?:por\s+)?noche', html, re.IGNORECASE)
print(f"Precios por noche por regex 'noche': {precios_noche}")

# Busquemos todos los textos en el html que tengan el símbolo del euro
euro_snippets = []
for m in re.finditer(r'(\d+)\s*[\xa0\s]*€', html):
    start = max(0, m.start() - 30)
    end = min(len(html), m.end() + 30)
    euro_snippets.append(html[start:end].replace('\n', ' '))
print(f"Snippets con € en HTML dinámico (primeros 10): {euro_snippets[:10]}")

# Busquemos si hay "total"
total_snippets = []
for m in re.finditer(r'(\d+)\s*[\xa0\s]*€\s*en\s*total', html, re.IGNORECASE):
    start = max(0, m.start() - 30)
    end = min(len(html), m.end() + 30)
    total_snippets.append(html[start:end].replace('\n', ' '))
print(f"Snippets con '€ en total' (primeros 5): {total_snippets[:5]}")
