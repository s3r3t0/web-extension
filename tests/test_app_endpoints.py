from __future__ import annotations

from cookie_lab import create_app


def test_health_endpoint() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/health")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["scenario_count"] == 18


def test_apply_scenario_sets_cookie_header() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/apply/SC16")

    assert response.status_code == 302
    set_cookie_headers = response.headers.getlist("Set-Cookie")
    joined = "\n".join(set_cookie_headers)
    assert "persist_ma=pi" in joined
    assert "Max-Age=86400" in joined


def test_clear_scenario_emits_delete_cookie_header() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/clear/SC11")

    assert response.status_code == 302
    set_cookie_headers = response.headers.getlist("Set-Cookie")
    joined = "\n".join(set_cookie_headers)
    assert "parent_cookie=" in joined
    assert "Expires=" in joined


def test_apply_all_emits_many_cookie_headers() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/apply-all")

    assert response.status_code == 302
    assert len(response.headers.getlist("Set-Cookie")) >= 18
