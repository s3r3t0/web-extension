from __future__ import annotations

from cookie_lab.scenarios import SCENARIOS


def test_scenario_count_and_ids_are_unique() -> None:
    assert len(SCENARIOS) == 18
    ids = [item.scenario_id for item in SCENARIOS]
    assert len(ids) == len(set(ids))


def test_every_scenario_has_expectation_metadata() -> None:
    for scenario in SCENARIOS:
        assert scenario.browser_expectation.storage in {"stored", "rejected"}
        assert scenario.browser_expectation.scope in {"host-only", "domain"}
        assert scenario.extension_expectation.flags in {True, False}
