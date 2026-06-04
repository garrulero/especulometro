import json
from bs4 import BeautifulSoup

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script")

# 1. Buscar ofertas en application/ld+json
print("--- BUSCANDO EN LD+JSON ---")
for i, script in enumerate(scripts):
    if script.get("type") == "application/ld+json":
        try:
            data = json.loads(script.string)
            # Busquemos recursivamente cualquier clave que contenga 'price' o 'offers'
            def find_offers_prices(d):
                res = []
                if isinstance(d, dict):
                    if "offers" in d:
                        res.append(("offers", d["offers"]))
                    if "price" in d:
                        res.append(("price", d["price"]))
                    for k, v in d.items():
                        res.extend(find_offers_prices(v))
                elif isinstance(d, list):
                    for item in d:
                        res.extend(find_offers_prices(item))
                return res

            op = find_offers_prices(data)
            if op:
                print(f"Encontrados en Script {i}:")
                for k, v in op:
                    print(f"  {k} = {v}")
        except Exception as e:
            pass

# 2. Buscar expresiones regulares en el HTML para precios como por ejemplo "XX €" o "€XX" o "XX €/noche" o similar
import re
print("\n--- BUSCANDO EXPRESIONES REGULARES EN EL HTML ---")
# Buscamos patrones de precio en español "120 €" o "120€"
precios_es = re.findall(r'(\d+[\.,]?\d*)\s*€', html)
print(f"Precios encontrados con '€': {list(set(precios_es))[:20]}")

# Buscamos patrones de precio en inglés / general como "$120"
precios_en = re.findall(r'\$\s*(\d+[\.,]?\d*)', html)
print(f"Precios encontrados con '$': {list(set(precios_en))[:20]}")

# Busquemos también textos del tipo "noche" o "por noche"
noches = re.findall(r'(\d+[\.,]?\d*)\s*[^<]{0,15}noche', html, re.IGNORECASE)
print(f"Números seguidos de 'noche': {list(set(noches))[:20]}")
