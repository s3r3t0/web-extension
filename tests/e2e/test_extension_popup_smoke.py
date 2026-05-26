from __future__ import annotations

import json
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Playwright, sync_playwright

from cookie_lab.models import CookieScenario
from cookie_lab.scenarios import SCENARIOS


ROOT_DIR = Path(__file__).resolve().parents[2]
POPUP_URL = (ROOT_DIR / "src" / "popup" / "sereto.html").resolve().as_uri()
BASE_URL = os.environ.get("COOKIE_LAB_BASE_URL", "https://app.localtest.me:8443")


def _selected_browsers() -> list[str]:
    requested = os.environ.get("E2E_BROWSERS", "chromium,firefox")
    items = [item.strip().lower() for item in requested.split(",") if item.strip()]
    allowed = {"chromium", "firefox"}
    selected = [item for item in items if item in allowed]
    if not selected:
        return ["chromium", "firefox"]
    return selected


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
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(0.5)

    raise RuntimeError(f"Cookie Lab health endpoint did not become ready: {health_url}")


def _same_site_for_extension(cookie: dict[str, object]) -> str:
    same_site = str(cookie.get("sameSite", "unspecified")).lower()
    if same_site == "none":
        return "no_restriction"
    if same_site in {"lax", "strict"}:
        return same_site
    return "unspecified"


def _to_extension_cookie(cookie: dict[str, object]) -> dict[str, object]:
    converted: dict[str, object] = {
        "name": cookie["name"],
        "domain": cookie["domain"],
        "secure": cookie["secure"],
        "httpOnly": cookie["httpOnly"],
        "sameSite": _same_site_for_extension(cookie),
    }

    expires = float(cookie.get("expires", -1))
    if expires > 0:
        converted["expirationDate"] = expires

    return converted


def _popup_output_for_mode(
    context: BrowserContext,
    extension_cookies: list[dict[str, object]],
    tab_url: str,
    mode: str,
) -> str:
    page = context.new_page()

    init_payload = json.dumps({"cookies": extension_cookies, "tabUrl": tab_url})
    init_script = """
        (() => {
            const { cookies, tabUrl } = __PAYLOAD__;
            window.__e2eCookies = cookies;
            window.__e2eTabUrl = tabUrl;
            const matchesDomain = (cookieDomain, targetDomain) => {
                const c = cookieDomain.startsWith(".") ? cookieDomain.slice(1) : cookieDomain;
                const t = targetDomain.startsWith(".") ? targetDomain.slice(1) : targetDomain;
                return c === t || c.endsWith(`.${t}`) || t.endsWith(`.${c}`);
            };

            const fakeApi = {
                tabs: {
                    query: () => Promise.resolve([{ title: "Cookie Lab", url: tabUrl }]),
                },
                cookies: {
                    getAll: ({ domain }) => Promise.resolve(cookies.filter((item) => matchesDomain(item.domain, domain))),
                },
            };

            window.browser = fakeApi;
            window.chrome = fakeApi;
        })();
    """.replace("__PAYLOAD__", init_payload)

    page.add_init_script(script=init_script)
    page.goto(POPUP_URL)

    page.evaluate(
        """
        (selectedMode) => {
          const tabUrl = window.__e2eTabUrl;
          const cookies = window.__e2eCookies || [];
          const textarea = document.querySelector("#textarea-cookies");
          if (!textarea) {
            return;
          }

          if (!cookies.length) {
            textarea.value = "No cookies in this tab.";
            return;
          }

          let output = "";
          if (selectedMode === "parent-domain") {
            output = getCookiesParentDomain(cookies);
          } else if (selectedMode === "persistent") {
            output = getCookiesPersistent(cookies);
          } else {
            output = getCookiesFlags(cookies);
          }
          textarea.value = `locators = [{type = \"url\", value = \"${tabUrl}\"}]\\n\\n${output}`;
        }
        """,
        mode,
    )

    page.wait_for_function(
        "document.querySelector('#textarea-cookies').value.length > 0"
    )
    output = page.locator("#textarea-cookies").input_value()
    page.close()
    return output


def _apply_scenario(context: BrowserContext, scenario_id: str) -> None:
    clear_response = context.request.post(f"{BASE_URL}/clear-all")
    assert clear_response.ok, "Failed to clear scenarios before test"

    apply_response = context.request.post(f"{BASE_URL}/apply/{scenario_id}")
    assert apply_response.ok, f"Failed to apply scenario {scenario_id}"


def _collect_extension_cookies(context: BrowserContext) -> list[dict[str, object]]:
    urls = [f"{BASE_URL}/", f"{BASE_URL}/admin"]
    return [_to_extension_cookie(item) for item in context.cookies(urls)]


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


@pytest.fixture(params=_selected_browsers(), ids=lambda browser: browser)
def browser_name(request: pytest.FixtureRequest) -> str:
    return str(request.param)


@pytest.fixture
def browser_context(
    playwright_instance: Playwright,
    browser_name: str,
    cookie_lab_server: None,
) -> BrowserContext:
    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=True)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    context = browser.new_context(ignore_https_errors=True)

    try:
        yield context
    finally:
        context.close()
        browser.close()


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda item: item.scenario_id)
def test_outputs_for_all_scenarios(
    browser_context: BrowserContext,
    scenario: CookieScenario,
) -> None:
    _apply_scenario(browser_context, scenario.scenario_id)
    cookies = _collect_extension_cookies(browser_context)

    flags_output = _popup_output_for_mode(
        browser_context,
        cookies,
        tab_url=f"{BASE_URL}/",
        mode="flags",
    )
    _assert_cookie_presence(
        flags_output,
        scenario.attributes.name,
        scenario.extension_expectation.flags,
        mode="flags",
    )

    parent_domain_output = _popup_output_for_mode(
        browser_context,
        cookies,
        tab_url=f"{BASE_URL}/",
        mode="parent-domain",
    )
    _assert_cookie_presence(
        parent_domain_output,
        scenario.attributes.name,
        scenario.extension_expectation.parent_domain,
        mode="parent-domain",
    )

    persistent_output = _popup_output_for_mode(
        browser_context,
        cookies,
        tab_url=f"{BASE_URL}/",
        mode="persistent",
    )
    _assert_cookie_presence(
        persistent_output,
        scenario.attributes.name,
        scenario.extension_expectation.persistent,
        mode="persistent",
    )
