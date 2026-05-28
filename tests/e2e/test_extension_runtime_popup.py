from __future__ import annotations

import os
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Playwright, sync_playwright

from cookie_lab.models import CookieScenario
from cookie_lab.scenarios import SCENARIOS


ROOT_DIR = Path(__file__).resolve().parents[2]
EXTENSION_DIR = ROOT_DIR / "src"
BASE_URL = os.environ.get("COOKIE_LAB_BASE_URL", "https://app.localtest.me:8443")

BROWSER_EXPECTATION_OVERRIDES: dict[str, dict[str, dict[str, bool]]] = {"chromium": {}}

pytestmark = pytest.mark.skipif(
    os.environ.get("E2E_EXTENSION_RUNTIME") != "1",
    reason="Set E2E_EXTENSION_RUNTIME=1 to run runtime extension popup tests.",
)


def _wait_for_health(base_url: str, timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    health_url = f"{base_url}/health"
    insecure_ssl = ssl._create_unverified_context()

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(
                health_url, timeout=2, context=insecure_ssl
            ) as resp:
                if resp.status == 200:
                    return
        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionError,
        ):  # transient startup/network failure; retry until deadline
            pass
        time.sleep(0.5)

    raise RuntimeError(f"Cookie Lab health endpoint did not become ready: {health_url}")


def _apply_scenario(context: BrowserContext, scenario_id: str) -> None:
    clear_response = _post_with_retry(context, f"{BASE_URL}/clear-all")
    assert clear_response.ok, "Failed to clear scenarios before test"

    apply_response = _post_with_retry(context, f"{BASE_URL}/apply/{scenario_id}")
    assert apply_response.ok, f"Failed to apply scenario {scenario_id}"


def _post_with_retry(
    context: BrowserContext,
    url: str,
    attempts: int = 3,
):
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return context.request.post(url)
        except Exception as error:  # pragma: no cover - flaky network branch
            if "EAI_AGAIN" not in str(error):
                raise
            last_error = error
            time.sleep(0.5)

    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Request failed unexpectedly for URL: {url}")


def _find_extension_id(
    context: BrowserContext,
    user_data_dir: Path,
    timeout_seconds: int = 10,
) -> str | None:
    for worker in context.service_workers:
        if worker.url.startswith("chrome-extension://"):
            return worker.url.split("/")[2]

    try:
        worker = context.wait_for_event("serviceworker", timeout=3_000)
        if worker.url.startswith("chrome-extension://"):
            return worker.url.split("/")[2]
    except Exception:  # service worker event may not fire in some environments; fallback to extension directory probing
        pass

    deadline = time.time() + timeout_seconds
    candidate_roots = [
        user_data_dir / "Default" / "Extensions",
        user_data_dir / "Extensions",
    ]

    while time.time() < deadline:
        for root in candidate_roots:
            if root.exists():
                for child in root.iterdir():
                    if child.is_dir() and len(child.name) == 32:
                        return child.name
        time.sleep(0.25)

    return None


def _open_runtime_popup(
    context: BrowserContext,
    extension_id: str,
    tab_url: str,
    mode: str,
) -> str:
    active_tab = context.new_page()
    active_tab.goto(tab_url)
    active_tab.wait_for_load_state("domcontentloaded")

    popup = context.new_page()
    popup.goto(f"chrome-extension://{extension_id}/popup/sereto.html")

    # In tab-driven automation there is no browser toolbar popup context,
    # so we override only tabs.query while keeping real extension cookie API.
    popup.evaluate(
        """
        (activeUrl) => {
          const patchedQuery = () => Promise.resolve([{ title: "Cookie Lab", url: activeUrl }]);
          if (window.browser?.tabs) {
            window.browser.tabs.query = patchedQuery;
          }
          if (window.chrome?.tabs) {
            window.chrome.tabs.query = patchedQuery;
          }
          if (typeof updateCookieDisplay === "function") {
            updateCookieDisplay();
          }
        }
        """,
        tab_url,
    )

    if mode != "flags":
        popup.evaluate(
            """
            (selectedMode) => {
              const radio = document.querySelector(`input[name="cookie-list"][value="${selectedMode}"]`);
              if (radio) {
                radio.checked = true;
                radio.dispatchEvent(new Event("change", { bubbles: true }));
              }
            }
            """,
            mode,
        )

    popup.evaluate(
        """
        async () => {
          if (typeof updateCookieDisplay === "function") {
            updateCookieDisplay();
            await new Promise((resolve) => setTimeout(resolve, 50));
          }
        }
        """
    )

    popup.wait_for_function(
        "document.querySelector('#textarea-cookies').value.length > 0"
    )
    output = popup.locator("#textarea-cookies").input_value()

    popup.close()
    active_tab.close()
    return output


def _assert_cookie_presence(
    output: str,
    cookie_name: str,
    expected_present: bool,
    mode: str,
) -> None:
    if mode == "parent-domain":
        marker = f'"{cookie_name}"'
    else:
        marker = f'name = "{cookie_name}"'

    if expected_present:
        assert marker in output
    else:
        assert marker not in output


def _expected_presence(scenario: CookieScenario, mode: str) -> bool:
    base_expected = {
        "flags": scenario.extension_expectation.flags,
        "parent-domain": scenario.extension_expectation.parent_domain,
        "persistent": scenario.extension_expectation.persistent,
    }[mode]

    override = (
        BROWSER_EXPECTATION_OVERRIDES.get("chromium", {})
        .get(scenario.scenario_id, {})
        .get(mode)
    )
    if override is None:
        return base_expected
    return override


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def cookie_lab_server() -> None:
    command = [
        sys.executable,
        "-m",
        "flask",
        "--app",
        "cookie_lab.app:create_app",
        "run",
        "--host",
        "0.0.0.0",
        "--port",
        "8443",
        "--cert",
        "adhoc",
    ]

    process = subprocess.Popen(
        command,
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_for_health(BASE_URL)
        yield
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session")
def chromium_runtime_context(
    playwright_instance: Playwright,
    cookie_lab_server: None,
) -> tuple[BrowserContext, str]:
    with tempfile.TemporaryDirectory(prefix="sereto-e2e-") as profile_dir:
        user_data_dir = Path(profile_dir)
        headless = os.environ.get("E2E_HEADLESS", "1") != "0"
        context = playwright_instance.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            ignore_https_errors=True,
            args=[
                f"--disable-extensions-except={EXTENSION_DIR}",
                f"--load-extension={EXTENSION_DIR}",
            ],
        )

        extension_id = _find_extension_id(context, user_data_dir)
        if not extension_id:
            context.close()
            pytest.skip(
                "Runtime extension loading is unavailable in this Chromium environment. "
                "Re-run with a supported local setup (for example E2E_HEADLESS=0)."
            )

        try:
            yield context, extension_id
        finally:
            context.close()


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda item: item.scenario_id)
def test_runtime_popup_outputs_for_all_scenarios(
    chromium_runtime_context: tuple[BrowserContext, str],
    scenario: CookieScenario,
) -> None:
    context, extension_id = chromium_runtime_context
    _apply_scenario(context, scenario.scenario_id)

    flags_output = _open_runtime_popup(
        context=context,
        extension_id=extension_id,
        tab_url=f"{BASE_URL}/",
        mode="flags",
    )
    _assert_cookie_presence(
        flags_output,
        scenario.attributes.name,
        _expected_presence(scenario, "flags"),
        mode="flags",
    )

    parent_domain_output = _open_runtime_popup(
        context=context,
        extension_id=extension_id,
        tab_url=f"{BASE_URL}/",
        mode="parent-domain",
    )
    _assert_cookie_presence(
        parent_domain_output,
        scenario.attributes.name,
        _expected_presence(scenario, "parent-domain"),
        mode="parent-domain",
    )

    persistent_output = _open_runtime_popup(
        context=context,
        extension_id=extension_id,
        tab_url=f"{BASE_URL}/",
        mode="persistent",
    )
    _assert_cookie_presence(
        persistent_output,
        scenario.attributes.name,
        _expected_presence(scenario, "persistent"),
        mode="persistent",
    )
