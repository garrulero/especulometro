import json
from bs4 import BeautifulSoup

def search_nested_dict_all(d, search_key, path=""):
    results = []
    if isinstance(d, dict):
        for k, v in d.items():
            current_path = f"{path}.{k}" if path else k
            if k == search_key:
                results.append((current_path, v))
            results.extend(search_nested_dict_all(v, search_key, current_path))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            current_path = f"{path}[{i}]"
            results.extend(search_nested_dict_all(item, search_key, current_path))
    return results

with open("airbnb_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script")

# 1. Mostrar todos los application/ld+json
print("--- APPLICATION/LD+JSON SCRIPTS ---")
for i, script in enumerate(scripts):
    if script.get("type") == "application/ld+json":
        try:
            data = json.loads(script.string)
            print(f"\nScript {i}:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        except Exception as e:
            print(f"Error cargando script {i}: {e}")

# 2. Buscar en data-deferred-state-0 todas las ocurrencias que contengan información útil
print("\n--- BUSCANDO DETALLES EN data-deferred-state-0 ---")
script_def = soup.find("script", id="data-deferred-state-0")
if script_def:
    try:
        data = json.loads(script_def.string)
        
        # Buscar host / anfitrión
        print("\nBuscando 'host':")
        hosts = search_nested_dict_all(data, "host")
        for p, h in hosts[:5]:
            if isinstance(h, dict):
                print(f"  Path: {p}")
                print(f"  Claves del host: {list(h.keys())}")
                if "name" in h:
                    print(f"    name: {h.get('name')}")
                if "hostName" in h:
                    print(f"    hostName: {h.get('hostName')}")
                if "profileRoute" in h:
                    print(f"    profileRoute: {h.get('profileRoute')}")
            else:
                print(f"  Path: {p} = {h}")
                
        # Buscar 'primaryHost' o similar
        print("\nBuscando 'primaryHost':")
        p_hosts = search_nested_dict_all(data, "primaryHost")
        for p, h in p_hosts[:5]:
            print(f"  Path: {p}")
            if isinstance(h, dict):
                print(f"    Keys: {list(h.keys())}")
                for k in ["name", "hostName", "id", "thumbnailUrl", "hostUrl"]:
                    if k in h:
                        print(f"      {k}: {h[k]}")
            else:
                print(f"    Value: {h}")

        # Buscar listingsCount o similar en los hosts
        print("\nBuscando 'listingsCount' / 'totalListings' / 'listings':")
        for key in ["listingsCount", "totalListings", "listings", "hostListingsCount"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {v}")

        # Buscar precios
        print("\nBuscando precios:")
        for key in ["price", "priceValue", "amount", "localizedPrice", "amountFormatted", "priceFormatted"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:10]:
                    print(f"    Path: {p} = {v}")

        # Buscar disponibilidad
        print("\nBuscando disponibilidad / días:")
        for key in ["availability", "days", "available", "rate"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada (primeras 5):")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {str(v)[:100]}")
                    
        # Buscar ciudades/municipios
        print("\nBuscando ciudad / municipio:")
        for key in ["city", "localizedCity", "town", "neighborhood"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {v}")

    except Exception as e:
        print(f"Error procesando data-deferred-state-0: {e}")
