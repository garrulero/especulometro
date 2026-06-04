import re

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

# Busquemos todas las apariciones de "€" o "\u20ac"
matches_euro = [m.start() for m in re.finditer(r'[\u20ac€]', html)]
print(f"Número de símbolos € encontrados: {len(matches_euro)}")

# Imprimir fragmentos alrededor de los primeros 10 símbolos de euro encontrados
for idx, pos in enumerate(matches_euro[:10]):
    start = max(0, pos - 50)
    end = min(len(html), pos + 50)
    snippet = html[start:end].replace('\n', ' ')
    print(f"Euro {idx}: ... {snippet} ...")

# Busquemos también si hay palabras como "noche" o "noches"
matches_noche = [m.start() for m in re.finditer(r'noche', html, re.IGNORECASE)]
print(f"\nNúmero de palabras 'noche' encontradas: {len(matches_noche)}")
for idx, pos in enumerate(matches_noche[:10]):
    start = max(0, pos - 50)
    end = min(len(html), pos + 50)
    snippet = html[start:end].replace('\n', ' ')
    print(f"Noche {idx}: ... {snippet} ...")
