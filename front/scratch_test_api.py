import requests
import json

url = "http://127.0.0.1:8000/api/analyze-url"
payload = {
    "url": "https://www.airbnb.es/rooms/1263042088195534687?check_in=2026-07-23&check_out=2026-07-26&photo_id=2008242867&source_impression_id=p3_1780561714_P3Bo06iMpNVH0CjW&previous_page_section_name=1000"
}

print(f"Enviando POST a {url}...")
try:
    response = requests.post(url, json=payload, timeout=20)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("\n--- RESPUESTA DEL BACKEND ---")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error de conexión: {e}")
