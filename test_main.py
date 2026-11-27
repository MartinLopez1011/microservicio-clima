import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.unit
def test_get_weather_status_code():
    """Valida que el endpoint /weather responda con HTTP 200."""
    # Arrange
    endpoint = "/weather"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.contract
def test_get_weather_payload_keys():
    """Valida que la respuesta contenga todos los campos requeridos del esquema."""
    # Arrange
    expected_keys = {"location", "temperature", "status", "wind_speed_kmh"}

    # Act
    response = client.get("/weather")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_keys.issubset(data.keys())


@pytest.mark.contract
def test_get_weather_data_types():
    """Valida que los tipos de datos devueltos coincidan con la especificación."""
    # Arrange
    endpoint = "/weather"

    # Act
    response = client.get(endpoint)
    data = response.json()

    # Assert
    assert isinstance(data["location"], str)
    assert isinstance(data["temperature"], (int, float))
    assert isinstance(data["status"], str)
    assert isinstance(data["wind_speed_kmh"], (int, float))


@pytest.mark.contract
def test_cors_middleware_headers():
    """Verifica que el middleware CORS permita solicitudes cruzadas."""
    # Arrange
    headers = {"Origin": "http://localhost:3000"}

    # Act
    response = client.get("/weather", headers=headers)

    # Assert
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"


@pytest.mark.contract
def test_cors_preflight_options():
    """Verifica que las solicitudes preflight OPTIONS respondan con cabeceras CORS válidas."""
    # Arrange
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
    }

    # Act
    response = client.options("/weather", headers=headers)

    # Assert
    assert response.status_code == 200
    assert "access-control-allow-methods" in response.headers


@pytest.mark.unit
def test_health_endpoint():
    """Valida que el endpoint /health responda HTTP 200 con estado ok."""
    # Arrange
    endpoint = "/health"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.functional
def test_metrics_endpoint():
    """Valida que /metrics exponga métricas Prometheus válidas y registre tráfico previo."""
    # Arrange
    client.get("/weather")
    endpoint = "/metrics"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")
    assert "http_requests_total" in response.text or "python_info" in response.text


@pytest.mark.functional
def test_error_test_endpoint():
    """Valida que el endpoint /error-test retorne HTTP 500 para pruebas de observabilidad."""
    # Arrange
    endpoint = "/error-test"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 500
    assert "detail" in response.json()


@pytest.mark.functional
def test_unknown_route_returns_404():
    """Valida que una ruta inexistente responda HTTP 404 Not Found."""
    # Arrange
    endpoint = "/ruta-inexistente"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 404


@pytest.mark.functional
@pytest.mark.parametrize("endpoint", ["/weather", "/health"])
def test_unsupported_http_method_returns_405(endpoint):
    """Valida que métodos HTTP no permitidos respondan HTTP 405 Method Not Allowed."""
    # Arrange / Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 405
