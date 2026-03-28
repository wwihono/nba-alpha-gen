"""API contract and behavior tests for the FastAPI backend."""

import pytest
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    assert response.json() == {"status": "ok"}


def test_info_returns_metadata(client: TestClient) -> None:
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "NBA Alpha Gen"
    assert body["version"] == "0.1.0"
    assert body["docs"] == "/docs"


def test_openapi_json_lists_system_routes(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    spec = response.json()
    assert spec["info"]["title"] == "NBA Alpha Gen"
    paths = spec.get("paths", {})
    assert "/health" in paths
    assert "/api/v1/info" in paths
    assert "get" in paths["/health"]


def test_docs_ui_available(client: TestClient) -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_redoc_available(client: TestClient) -> None:
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_unknown_path_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404


def test_health_method_not_allowed_post(client: TestClient) -> None:
    response = client.post("/health")
    assert response.status_code == 405


def test_cors_allows_configured_browser_origin(client: TestClient) -> None:
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
