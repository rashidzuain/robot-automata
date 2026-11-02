import time
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from server.app import create_app
from server.config import Settings


@pytest.fixture
def config(tmp_path):
    return Settings(database_path=tmp_path / "test.sqlite3", demo_interval_seconds=0.01, demo_max_seconds=2)


@pytest.fixture
def client(config):
    with TestClient(create_app(config)) as client:
        yield client


def wait_for(predicate, timeout=2):
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        value = predicate()
        if value:
            return value
        time.sleep(0.01)
    raise AssertionError("El resultado esperado no llegó dentro del tiempo de prueba")


def test_empty_server_has_no_fabricated_readings(client):
    assert client.get("/healthz").json() == {"status": "ok", "version": "0.1.0"}
    state = client.get("/api/v1/status").json()
    assert state["sample_count"] == 0
    assert state["device"]["connected"] is False
    assert state["device"]["last_seen_at"] is None
    assert state["demo_running"] is False
    assert client.get("/api/v1/telemetry").json() == {"items": [], "total": 0}
    assert client.get("/api/v1/telemetry?source=demo").json()["items"] == []


def test_telemetry_survives_restart_and_keeps_unknowns(config):
    sample = {"battery_v": 6.03, "ir_left": False, "pwm_left": 0}
    with TestClient(create_app(config)) as first:
        response = first.post("/api/v1/telemetry", json=sample)
        assert response.status_code == 201
        record = response.json()
        assert record["battery_v"] == 6.03
        assert record["ir_left"] is False
        assert record["pwm_left"] == 0
        assert record["distance_cm"] is None
        assert record["source"] == "device"
        assert datetime.fromisoformat(record["received_at"]).utcoffset() == timedelta(0)
    with TestClient(create_app(config)) as second:
        assert second.get("/api/v1/telemetry").json() == {"items": [record], "total": 1}
        assert second.get("/api/v1/status").json()["demo_running"] is False


@pytest.mark.parametrize("sample", [
    {}, {"battery_v": None}, {"battery_v": -1}, {"battery_v": 21},
    {"distance_cm": -1}, {"distance_cm": 1001}, {"battery_v": "6.03"},
    {"pwm_left": 256}, {"pwm_right": -256}, {"pwm_left": True},
    {"ir_left": "false"}, {"ir_right": 1},
    {"battery_v": 6, "source": "demo"}, {"battery_v": 6, "robot_id": "sim-01"},
    {"battery_v": 6, "unexpected": "value"},
])
def test_invalid_sample_is_rejected_without_writing(client, sample):
    response = client.post("/api/v1/telemetry", json=sample)
    assert response.status_code == 422
    assert response.json()["detail"]
    assert client.get("/api/v1/telemetry").json()["total"] == 0


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
def test_nonfinite_values_return_a_valid_error(client, value):
    response = client.post("/api/v1/telemetry", content='{"battery_v": ' + value + '}', headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert client.get("/api/v1/telemetry").json()["total"] == 0


def test_history_is_bounded_sorted_and_source_specific(client):
    ids = []
    for value in [0, 42.5, 1000]:
        response = client.post("/api/v1/telemetry", json={"distance_cm": value})
        assert response.status_code == 201
        ids.append(response.json()["id"])
    result = client.get("/api/v1/telemetry?source=device&limit=2").json()
    assert result["total"] == 3
    assert [item["id"] for item in result["items"]] == list(reversed(ids[-2:]))
    assert client.get("/api/v1/telemetry?source=demo").json()["total"] == 0


@pytest.mark.parametrize("query", ["limit=0", "limit=501", "limit=-2", "limit=wrong", "source=unknown"])
def test_history_rejects_invalid_queries(client, query):
    assert client.get(f"/api/v1/telemetry?{query}").status_code == 422


def test_device_becomes_stale_without_losing_history(client):
    assert client.post("/api/v1/telemetry", json={"battery_v": 6}).status_code == 201
    assert client.get("/api/v1/status").json()["device"]["connected"] is True
    old = (datetime.now(timezone.utc) - timedelta(seconds=20)).isoformat()
    with client.app.state.store.connection() as db:
        db.execute("UPDATE telemetry SET received_at=?", (old,))
    state = client.get("/api/v1/status").json()
    assert state["device"]["connected"] is False
    assert state["device"]["last_seen_at"] == old
    assert client.get("/api/v1/telemetry").json()["total"] == 1


def test_demo_start_is_idempotent_and_does_not_connect_real_robot(client):
    assert client.post("/api/v1/demo/start", json={}).json() == {"running": True}
    task = client.app.state.demo._task
    assert client.post("/api/v1/demo/start", json={}).json() == {"running": True}
    assert client.app.state.demo._task is task
    wait_for(lambda: client.get("/api/v1/telemetry?source=demo").json()["total"] >= 2)
    sample = client.get("/api/v1/telemetry?source=demo&limit=1").json()["items"][0]
    assert sample["robot_id"] == "sim-01"
    assert sample["source"] == "demo"
    assert client.get("/api/v1/telemetry").json()["total"] == 0
    assert client.get("/api/v1/status").json()["device"]["connected"] is False
    assert client.post("/api/v1/demo/stop", json={}).json() == {"running": False}
    count = client.get("/api/v1/telemetry?source=demo").json()["total"]
    time.sleep(0.06)
    assert client.get("/api/v1/telemetry?source=demo").json()["total"] == count
    assert client.post("/api/v1/demo/stop", json={}).json() == {"running": False}
    messages = [item["message"] for item in client.get("/api/v1/events").json()["items"]]
    assert sum(message.startswith("Simulación iniciada") for message in messages) == 1


def test_demo_stops_when_lifespan_closes(config):
    app = create_app(config)
    with TestClient(app) as client:
        client.post("/api/v1/demo/start", json={})
        wait_for(lambda: client.get("/api/v1/telemetry?source=demo").json()["total"] > 0)
    assert app.state.demo.running is False
    count = app.state.store.history("demo", 1)["total"]
    time.sleep(0.03)
    assert app.state.store.history("demo", 1)["total"] == count


def test_demo_expires_without_an_explicit_stop(tmp_path):
    settings = Settings(database_path=tmp_path / "expiry.sqlite3", demo_interval_seconds=0.01, demo_max_seconds=0.08)
    with TestClient(create_app(settings)) as client:
        client.post("/api/v1/demo/start", json={})
        wait_for(lambda: client.get("/api/v1/status").json()["demo_running"] is False)
        assert client.get("/api/v1/telemetry?source=demo").json()["total"] > 0


def test_other_sites_cannot_change_the_local_server(client):
    assert client.post("/api/v1/demo/start", json={}, headers={"Origin": "https://other.example"}).status_code == 403
    assert client.post("/api/v1/demo/start", json={}, headers={"Sec-Fetch-Site": "cross-site"}).status_code == 403
    assert client.get("/healthz", headers={"Host": "other.example"}).status_code == 400
    assert client.get("/api/v1/demo/start").status_code == 405
    assert client.post("/api/v1/demo/start", json={}, headers={"Origin": "http://testserver"}).status_code == 200
    assert client.post("/api/v1/demo/stop", json={}).status_code == 200


def test_dashboard_assets_and_contract_are_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert 'lang="es"' in response.text
    assert client.get("/static/styles.css").status_code == 200
    assert client.get("/static/app.js").status_code == 200
    schema = client.get("/openapi.json").json()
    assert "post" in schema["paths"]["/api/v1/telemetry"]
    assert client.get("/api/v1/status").headers["cache-control"] == "no-store"
