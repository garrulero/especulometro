from bs4 import BeautifulSoup

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
body = soup.body

# Contar caracteres en el body
body_text = body.get_text() if body else ""
print(f"Longitud del texto en body: {len(body_text)}")

# Imprimir las primeras 1000 palabras o caracteres del body_text
print("\n--- TEXTO DEL BODY (primeros 1000 chars) ---")
print(body_text[:1000])

# Buscar si hay alguna palabra en español para entender qué idioma o contenido hay
import re
palabras = re.findall(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]+', body_text)
print(f"\nTotal de palabras en body: {len(palabras)}")
print(f"Primeras 50 palabras: {palabras[:50]}")
