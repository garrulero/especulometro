import json
import re
from bs4 import BeautifulSoup

def search_nested_dict(d, search_key):
    results = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k == search_key:
                results.append(v)
            else:
                results.extend(search_nested_dict(v, search_key))
    elif isinstance(d, list):
        for item in d:
            results.extend(search_nested_dict(item, search_key))
    return results

def analyze_json():
    with open("airbnb_page.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Inspect data-deferred-state-0
    script_deferred = soup.find("script", id="data-deferred-state-0")
    if script_deferred:
        print("data-deferred-state-0 encontrado!")
        try:
            data = json.loads(script_deferred.string)
            print("data-deferred-state-0 JSON cargado correctamente!")
            
            # Print top-level keys
            print(f"Claves principales: {list(data.keys())}")
            
            # Busquemos algunas claves clave
            for key in ["price", "priceValue", "amount", "localizedPrice", "host", "hostName", "listingsCount", "title", "name", "city", "localizedCity"]:
                res = search_nested_dict(data, key)
                if res:
                    print(f"Clave '{key}' encontrada {len(res)} veces. Primeros valores:")
                    for r in res[:5]:
                        # Si es un dict grande, resumir
                        if isinstance(r, dict):
                            print(f"  dict keys: {list(r.keys())}")
                        else:
                            print(f"  {r}")
        except Exception as e:
            print(f"Error al decodificar data-deferred-state-0: {e}")
            
    # 2. Inspect data-injector-instances
    script_injector = soup.find("script", id="data-injector-instances")
    if script_injector:
        print("\ndata-injector-instances encontrado!")
        try:
            # data-injector-instances is often a list of scripts or custom format
            # Let's see if it's JSON
            data = json.loads(script_injector.string)
            print("data-injector-instances JSON cargado!")
            print(f"Claves principales: {list(data.keys())}")
            
            for key in ["price", "amount", "host", "name", "city"]:
                res = search_nested_dict(data, key)
                if res:
                    print(f"Clave '{key}' encontrada {len(res)} veces.")
        except Exception as e:
            print(f"Error al decodificar data-injector-instances: {e}")

if __name__ == "__main__":
    analyze_json()
