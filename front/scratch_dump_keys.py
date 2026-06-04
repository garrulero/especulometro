import json
from bs4 import BeautifulSoup

with open("airbnb_page_dynamic.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
script_inj = soup.find("script", id="data-injector-instances")

if script_inj:
    data = json.loads(script_inj.string)
    print("Claves principales en data-injector-instances:")
    for k in data.keys():
        print(f"  {k} (tipo: {type(data[k])})")
        # Si es un dict o lista, mostrar su tamaño o claves de primer nivel
        if isinstance(data[k], dict):
            print(f"    sub-keys: {list(data[k].keys())[:10]}")
        elif isinstance(data[k], list):
            print(f"    length: {len(data[k])}")
            if len(data[k]) > 0:
                print(f"    first item type: {type(data[k][0])}")
