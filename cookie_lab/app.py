from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, url_for

from .scenarios import SCENARIOS, get_scenario_map

SCENARIO_MAP = get_scenario_map()


def _set_cookie_from_scenario(response: Any, scenario_id: str) -> None:
    scenario = SCENARIO_MAP[scenario_id]
    attrs = scenario.attributes
    response.set_cookie(
        key=attrs.name,
        value=attrs.value,
        domain=attrs.domain,
        path=attrs.path,
        secure=attrs.secure,
        httponly=attrs.httponly,
        samesite=attrs.samesite,
        max_age=attrs.max_age,
        expires=attrs.expires,
    )


def _clear_cookie_from_scenario(response: Any, scenario_id: str) -> None:
    scenario = SCENARIO_MAP[scenario_id]
    attrs = scenario.attributes

    response.delete_cookie(key=attrs.name, path=attrs.path)

    if attrs.domain:
        response.delete_cookie(key=attrs.name, path=attrs.path, domain=attrs.domain)


def _grouped_scenarios() -> dict[str, list[Any]]:
    groups: dict[str, list[Any]] = defaultdict(list)
    for scenario in SCENARIOS:
        groups[scenario.category].append(scenario)
    return dict(groups)


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.get("/")
    def index() -> str:
        return render_template("index.html", groups=_grouped_scenarios())

    @app.get("/health")
    def health() -> Any:
        return jsonify({"status": "ok", "scenario_count": len(SCENARIOS)})

    @app.get("/api/scenarios")
    def api_scenarios() -> Any:
        payload = []
        for scenario in SCENARIOS:
            item = asdict(scenario)
            payload.append(item)
        return jsonify(payload)

    @app.post("/apply/<scenario_id>")
    def apply_scenario(scenario_id: str) -> Any:
        if scenario_id not in SCENARIO_MAP:
            return jsonify({"error": "unknown scenario"}), 404

        response = redirect(url_for("index"))
        _set_cookie_from_scenario(response, scenario_id)
        return response

    @app.post("/clear/<scenario_id>")
    def clear_scenario(scenario_id: str) -> Any:
        if scenario_id not in SCENARIO_MAP:
            return jsonify({"error": "unknown scenario"}), 404

        response = redirect(url_for("index"))
        _clear_cookie_from_scenario(response, scenario_id)
        return response

    @app.post("/apply-all")
    def apply_all() -> Any:
        response = redirect(url_for("index"))
        for scenario in SCENARIOS:
            _set_cookie_from_scenario(response, scenario.scenario_id)
        return response

    @app.post("/clear-all")
    def clear_all() -> Any:
        response = redirect(url_for("index"))
        for scenario in SCENARIOS:
            _clear_cookie_from_scenario(response, scenario.scenario_id)
        return response

    @app.get("/admin")
    def admin_route() -> Any:
        return jsonify(
            {
                "path": request.path,
                "message": "Use this route to inspect /admin path-scoped cookie behavior.",
            }
        )

    return app
