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
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    try:
        data = json.loads(script_inj.string)
        print("data-injector-instances cargado con éxito.")
        
        # Buscar host / anfitrión
        print("\nBuscando 'host' en data-injector-instances:")
        hosts = search_nested_dict_all(data, "host")
        for p, h in hosts[:10]:
            if isinstance(h, dict):
                print(f"  Path: {p}")
                print(f"  Claves: {list(h.keys())}")
                for k in ["name", "hostName", "id", "thumbnailUrl", "listingsCount"]:
                    if k in h:
                        print(f"    {k}: {h[k]}")
            else:
                print(f"  Path: {p} = {h}")
                
        # Buscar 'primaryHost' o similar
        print("\nBuscando 'primaryHost' en data-injector-instances:")
        p_hosts = search_nested_dict_all(data, "primaryHost")
        for p, h in p_hosts[:10]:
            print(f"  Path: {p}")
            if isinstance(h, dict):
                print(f"    Keys: {list(h.keys())}")
                for k in ["name", "id", "thumbnailUrl", "listingsCount"]:
                    if k in h:
                        print(f"      {k}: {h[k]}")
            else:
                print(f"    Value: {h}")

        # Buscar listingsCount o similar en los hosts
        print("\nBuscando 'listingsCount' / 'totalListings' / 'listings' en data-injector-instances:")
        for key in ["listingsCount", "totalListings", "listings", "hostListingsCount", "listings_count"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {v}")

        # Buscar precios
        print("\nBuscando precios en data-injector-instances:")
        for key in ["price", "priceValue", "amount", "localizedPrice", "amountFormatted", "priceFormatted", "rate"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:10]:
                    print(f"    Path: {p} = {v}")

        # Buscar disponibilidad
        print("\nBuscando disponibilidad / días en data-injector-instances:")
        for key in ["availability", "days", "available", "rate"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada (primeras 5):")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {str(v)[:100]}")
                    
        # Buscar ciudades/municipios
        print("\nBuscando ciudad / municipio en data-injector-instances:")
        for key in ["city", "localizedCity", "town", "neighborhood"]:
            res = search_nested_dict_all(data, key)
            if res:
                print(f"  Key '{key}' encontrada:")
                for p, v in res[:5]:
                    print(f"    Path: {p} = {v}")

    except Exception as e:
        print(f"Error procesando data-injector-instances: {e}")
