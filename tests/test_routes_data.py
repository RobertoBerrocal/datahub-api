from fastapi.testclient import TestClient

from app.main import app


def test_update_exchange_rates_success(monkeypatch):
    client = TestClient(app)

    monkeypatch.setattr(
        "app.api.routes_data.extract_exchange_rates",
        lambda *args, **kwargs: {"base": "USD", "rates": {"2026-01-01": {"EUR": 0.9}}},
    )

    class DummyDF:
        pass

    monkeypatch.setattr("app.api.routes_data.transform_exchange_rates", lambda *_: DummyDF())
    monkeypatch.setattr("app.api.routes_data.load_exchange_rates", lambda *_: 3)

    response = client.post("/data/update/exchange_rates")

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["rows_inserted"] == 6


def test_update_exchange_rates_error(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(
        "app.api.routes_data.extract_exchange_rates",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    response = client.post("/data/update/exchange_rates")

    assert response.status_code == 500
    assert "Exchange rates update failed" in response.json()["detail"]


def test_update_air_pollution_success(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr("app.api.routes_data.extract_air_pollution", lambda: [{"city": "Berlin"}])

    class DummyDF:
        pass

    monkeypatch.setattr("app.api.routes_data.transform_air_pollution", lambda *_: DummyDF())
    monkeypatch.setattr("app.api.routes_data.load_air_pollution", lambda *_: 10)

    response = client.post("/data/update/air_pollution")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "rows_inserted": 10}


def test_update_air_pollution_error(monkeypatch):
    client = TestClient(app)
    monkeypatch.setattr(
        "app.api.routes_data.extract_air_pollution",
        lambda: (_ for _ in ()).throw(ValueError("missing key")),
    )

    response = client.post("/data/update/air_pollution")

    assert response.status_code == 500
    assert "Air pollution update failed" in response.json()["detail"]
