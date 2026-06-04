import re
import sys
from bs4 import BeautifulSoup

# Configurar salida de consola a UTF-8
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Buscar todas las etiquetas y su texto que contengan "anuncio" o "alojamiento"
print("--- ANÁLISIS DE ANUNCIOS/ALOJAMIENTOS EN EL DOM ---")
for el in soup.find_all(True):
    # Si la etiqueta no tiene hijos que sean otras etiquetas (es una hoja de texto)
    if el.string or (len(el.contents) == 1 and isinstance(el.contents[0], str)):
        text = el.get_text().strip()
        if any(w in text.lower() for w in ["anuncio", "alojamiento", "listing", "propiedad"]):
            print(f"Tag: {el.name}, Class: {el.get('class')}, Text: {repr(text)}")
            
print("\n--- BÚSQUEDA DE REGEX DE NÚMEROS EN TEXTO PLANO ---")
text_plain = soup.get_text()
matches = re.finditer(r'(\d+)\s*(?:anuncio|alojamiento|propiedad|listing|evaluación|reseña)s?', text_plain, re.IGNORECASE)
for m in matches:
    print(f"Match: {m.group(0)} (Posición {m.start()}) -> Contexto: {repr(text_plain[max(0, m.start()-40):min(len(text_plain), m.end()+40)])}")
