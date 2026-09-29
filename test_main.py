import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_weather_status_code():
    """Valida que el endpoint /weather responda con HTTP 200."""
    response = client.get("/weather")
    assert response.status_code == 200

def test_get_weather_payload_keys():
    """Valida que la respuesta contenga todos los campos requeridos del esquema."""
    response = client.get("/weather")
    data = response.json()
    expected_keys = {"location", "temperature", "status", "wind_speed_kmh"}
    assert expected_keys.issubset(data.keys())

def test_get_weather_data_types():
    """Valida que los tipos de datos devueltos coincidan con la especificación."""
    response = client.get("/weather")
    data = response.json()
    assert isinstance(data["location"], str)
    assert isinstance(data["temperature"], (int, float))
    assert isinstance(data["status"], str)
    assert isinstance(data["wind_speed_kmh"], (int, float))

def test_cors_middleware_headers():
    """Verifica que el middleware CORS permita solicitudes cruzadas."""
    headers = {"Origin": "http://localhost:3000"}
    response = client.get("/weather", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"
