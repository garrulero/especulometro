import json
import re
from bs4 import BeautifulSoup

def search_nested_dict(d, search_key, path=""):
    results = []
    if isinstance(d, dict):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if k == search_key:
                results.append((current_path, v))
            else:
                results.extend(search_nested_dict(v, search_key, current_path))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            current_path = f"{path}[{i}]"
            results.extend(search_nested_dict(item, search_key, current_path))
    return results

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script")
print(f"Total de scripts: {len(scripts)}")

for i, script in enumerate(scripts):
    sid = script.get("id")
    stype = script.get("type")
    sclass = script.get("class")
    content_len = len(script.string) if script.string else 0
    if content_len > 100:
        print(f"Script {i}: id={sid}, type={stype}, class={sclass}, len={content_len}")

# Intentemos cargar los JSON de los scripts que parezcan JSON
for i, script in enumerate(scripts):
    if script.string and script.string.strip().startswith("{") and script.string.strip().endswith("}"):
        sid = script.get("id", f"unnamed_{i}")
        try:
            data = json.loads(script.string)
            print(f"\n--- Script {sid} (JSON cargado con éxito) ---")
            
            # Buscar precio
            for key in ["price", "priceValue", "amount", "localizedPrice", "host", "hostName", "listingsCount", "title", "name", "city", "localizedCity", "price_string", "rate"]:
                res = search_nested_dict(data, key)
                if res:
                    print(f"  Clave '{key}' encontrada {len(res)} veces:")
                    for path, val in res[:3]:
                        val_str = str(val)[:100]
                        print(f"    Path: {path} = {val_str}")
        except Exception as e:
            pass
