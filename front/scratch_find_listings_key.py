import json
import re
from bs4 import BeautifulSoup

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    data = json.loads(script_inj.string)
    
    # Buscar claves que contengan palabras interesantes de forma recursiva
    def find_matching_keys(d, search_pattern, path=""):
        results = []
        if isinstance(d, dict):
            for k, v in d.items():
                curr = f"{path}.{k}" if path else k
                if search_pattern.search(k):
                    results.append((curr, v))
                results.extend(find_matching_keys(v, search_pattern, curr))
        elif isinstance(d, list):
            for i, v in enumerate(d):
                curr = f"{path}[{i}]"
                results.extend(find_matching_keys(v, search_pattern, curr))
        return results

    # Buscar 'listings' o 'count'
    pattern = re.compile(r'listings|host|anfitr', re.IGNORECASE)
    res = find_matching_keys(data, pattern)
    print(f"Total de claves encontradas con listings/host/anfitr: {len(res)}")
    for p, v in res[:30]:
        val_str = str(v)[:150]
        print(f"  {p} = {val_str}")
