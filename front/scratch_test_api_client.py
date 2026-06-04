from fastapi.testclient import TestClient
from server import app
import json

client = TestClient(app)

def test_analyze_url():
    payload = {
        "url": "https://www.airbnb.es/rooms/1263042088195534687?check_in=2026-07-23&check_out=2026-07-26"
    }
    response = client.post("/api/analyze-url", json=payload)
    print("STATUS CODE:", response.status_code)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_analyze_url()
