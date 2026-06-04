import json
import re
from bs4 import BeautifulSoup

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    data = json.loads(script_inj.string)
    try:
        node = data["root"][4][1][4][1]["data"]["node"]
        
        # Buscar en el nodo recursivamente cualquier clave con 'host' o 'listings' o similar
        def search_node(d, pattern, path=""):
            results = []
            if isinstance(d, dict):
                for k, v in d.items():
                    curr = f"{path}.{k}" if path else k
                    if pattern.search(k):
                        results.append((curr, v))
                    results.extend(search_node(v, pattern, curr))
            elif isinstance(d, list):
                for i, v in enumerate(d):
                    curr = f"{path}[{i}]"
                    results.extend(search_node(v, pattern, curr))
            return results

        pattern = re.compile(r'host|listings|count|owner', re.IGNORECASE)
        res = search_node(node, pattern)
        print(f"Claves encontradas en node: {len(res)}")
        for p, v in res[:30]:
            val_str = str(v)[:150]
            print(f"  {p} = {val_str}")
            
    except Exception as e:
        print(f"Error: {e}")
