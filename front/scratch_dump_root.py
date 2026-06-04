import json
from bs4 import BeautifulSoup

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    data = json.loads(script_inj.string)
    # Vamos a navegar a root[4][1][4][1]
    try:
        node = data["root"][4][1][4][1]["data"]["node"]
        print("Encontrado node en root[4][1][4][1]['data']['node']!")
        print(f"Claves del node: {list(node.keys())}")
        
        # Vamos a ver qué hay en cada subclave principal
        for k in node.keys():
            val = node[k]
            if isinstance(val, dict):
                print(f"  Clave '{k}' (dict) con claves: {list(val.keys())}")
            elif isinstance(val, list):
                print(f"  Clave '{k}' (list) con longitud: {len(val)}")
            else:
                print(f"  Clave '{k}': {val}")
    except Exception as e:
        print(f"Error accediendo a root[4][1][4][1]['data']['node']: {e}")
        
        # Busquemos en todo el data por si la ruta no es exactamente esa
        # Por ejemplo, busquemos dónde está la clave "location"
        def find_key_paths(d, target, path=""):
            paths = []
            if isinstance(d, dict):
                for k, v in d.items():
                    curr = f"{path}.{k}" if path else k
                    if k == target:
                        paths.append((curr, v))
                    paths.extend(find_key_paths(v, target, curr))
            elif isinstance(d, list):
                for i, v in enumerate(d):
                    curr = f"{path}[{i}]"
                    paths.extend(find_key_paths(v, target, curr))
            return paths

        print("\nBuscando rutas para 'location':")
        paths = find_key_paths(data, "location")
        for p, v in paths[:5]:
            print(f"  Path: {p}")
            if isinstance(v, dict):
                print(f"    Keys: {list(v.keys())}")
                if "city" in v:
                    print(f"      city: {v['city']}")
