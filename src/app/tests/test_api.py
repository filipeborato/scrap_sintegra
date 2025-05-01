from fastapi.testclient import TestClient
from routers.app import app

client = TestClient(app)

def test_home():    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Test": "Technical Challenge"}

def test_scrape_valid_cnpj():    
    body = {"cnpj": "12345678000195"}
    response = client.post("/scrape", json=body)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_scrape_invalid_cnpj():    
    body = {"cnpj": "12345"}
    response = client.post("/scrape", json=body)
    assert response.status_code == 200
    assert "CNPJ must have 14 digits" in response.json().get("content", {}).get("msg", "")

def test_results_task():    
    task_id = "fd0a4f69978a521a_20250501164226"
    response = client.get(f"/results/{task_id}")
    assert response.status_code == 200
    assert "success" in response.json()

