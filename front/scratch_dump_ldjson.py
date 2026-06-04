import json
from bs4 import BeautifulSoup

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script", type="application/ld+json")

for i, script in enumerate(scripts):
    print(f"\n--- LD+JSON Script {i} ---")
    try:
        data = json.loads(script.string)
        # Imprimir de forma bonita e ilimitada (dentro de lo razonable, es un script pequeño)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error cargando JSON: {e}")
