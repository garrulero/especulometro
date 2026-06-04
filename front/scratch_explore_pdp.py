import json
import re
from bs4 import BeautifulSoup

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    data = json.loads(script_inj.string)
    pdp_key = None
    for k in data.keys():
        if "/rooms/" in k:
            pdp_key = k
            break
            
    if pdp_key:
        print(f"Clave encontrada: '{pdp_key}'")
        pdp_data = data[pdp_key]
        
        # Función para buscar en toda la estructura
        def search_pdp(d, pattern, path=""):
            results = []
            if isinstance(d, dict):
                for k, v in d.items():
                    curr = f"{path}.{k}" if path else k
                    if pattern.search(k):
                        results.append((curr, v))
                    results.extend(search_pdp(v, pattern, curr))
            elif isinstance(d, list):
                for i, v in enumerate(d):
                    curr = f"{path}[{i}]"
                    results.extend(search_pdp(v, pattern, curr))
            return results

        # Buscar claves relacionadas con host o listings
        pattern = re.compile(r'host|listings|count|owner', re.IGNORECASE)
        res = search_pdp(pdp_data, pattern)
        print(f"Total de claves encontradas en PDP data: {len(res)}")
        # Mostrar las primeras 50 claves y sus valores
        for p, v in res[:50]:
            val_str = str(v)[:150]
            print(f"  {p} = {val_str}")
