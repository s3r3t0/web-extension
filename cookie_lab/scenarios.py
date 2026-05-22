from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .config import AppConfig
from .models import (
    BrowserExpectation,
    CookieAttributes,
    CookieScenario,
    ExtensionExpectation,
    RequestContext,
)


def _future_date(days: int) -> str:
    target = datetime.now(timezone.utc) + timedelta(days=days)
    return target.strftime("%a, %d %b %Y %H:%M:%S GMT")


def _past_date() -> str:
    target = datetime.now(timezone.utc) - timedelta(days=1)
    return target.strftime("%a, %d %b %Y %H:%M:%S GMT")


SCENARIOS: list[CookieScenario] = [
    CookieScenario(
        scenario_id="SC01",
        title="Valid __Host- cookie",
        category="prefixes",
        attributes=CookieAttributes(
            name="__Host-session",
            value="alpha",
            path="/",
            secure=True,
            httponly=True,
            samesite="Lax",
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Valid host prefix contract: secure + path slash + no domain.",
    ),
    CookieScenario(
        scenario_id="SC02",
        title="Invalid __Host- with Domain",
        category="prefixes",
        attributes=CookieAttributes(
            name="__Host-session-domain",
            value="beta",
            domain=AppConfig.BASE_DOMAIN,
            path="/",
            secure=True,
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="rejected", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=False, parent_domain=False, persistent=False
        ),
        notes="Browsers should reject __Host- cookies if Domain is present.",
    ),
    CookieScenario(
        scenario_id="SC03",
        title="Invalid __Host- with non-root path",
        category="prefixes",
        attributes=CookieAttributes(
            name="__Host-session-path",
            value="gamma",
            path="/app",
            secure=True,
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/app"
        ),
        browser_expectation=BrowserExpectation(
            storage="rejected",
            scope="host-only",
            persistence="session",
            path_scope="/app",
        ),
        extension_expectation=ExtensionExpectation(
            flags=False, parent_domain=False, persistent=False
        ),
        notes="Browsers should reject __Host- cookies when path is not slash.",
    ),
    CookieScenario(
        scenario_id="SC04",
        title="Valid __Secure- cookie",
        category="prefixes",
        attributes=CookieAttributes(
            name="__Secure-id", value="delta", secure=True, samesite="Lax"
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Valid secure prefix cookie over HTTPS.",
    ),
    CookieScenario(
        scenario_id="SC05",
        title="Invalid __Secure- without Secure",
        category="prefixes",
        attributes=CookieAttributes(name="__Secure-no-sec", value="epsilon"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="rejected", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=False, parent_domain=False, persistent=False
        ),
        notes="Browsers should reject secure-prefix cookies lacking Secure.",
    ),
    CookieScenario(
        scenario_id="SC06",
        title="SameSite None with Secure",
        category="samesite",
        attributes=CookieAttributes(
            name="sid_none_ok", value="zeta", secure=True, samesite="None"
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Modern browsers require Secure for SameSite=None.",
    ),
    CookieScenario(
        scenario_id="SC07",
        title="SameSite None without Secure",
        category="samesite",
        attributes=CookieAttributes(name="sid_none_bad", value="eta", samesite="None"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="rejected", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=False, parent_domain=False, persistent=False
        ),
        notes="Should be rejected in current browser engines.",
    ),
    CookieScenario(
        scenario_id="SC08",
        title="SameSite Lax explicit",
        category="samesite",
        attributes=CookieAttributes(name="sid_lax", value="theta", samesite="Lax"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Explicit Lax case.",
    ),
    CookieScenario(
        scenario_id="SC09",
        title="SameSite Strict explicit",
        category="samesite",
        attributes=CookieAttributes(name="sid_strict", value="iota", samesite="Strict"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Explicit Strict case.",
    ),
    CookieScenario(
        scenario_id="SC10",
        title="SameSite omitted",
        category="samesite",
        attributes=CookieAttributes(name="sid_default", value="kappa"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Effective behavior should default to Lax in modern browsers.",
    ),
    CookieScenario(
        scenario_id="SC11",
        title="Parent-domain cookie",
        category="domain-scope",
        attributes=CookieAttributes(
            name="parent_cookie",
            value="lambda",
            domain=AppConfig.BASE_DOMAIN,
            path="/",
            secure=True,
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="domain", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=True, persistent=False
        ),
        notes="Expected on both app and api subdomains.",
    ),
    CookieScenario(
        scenario_id="SC12",
        title="Host-only cookie",
        category="domain-scope",
        attributes=CookieAttributes(name="host_cookie", value="mu", path="/"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Should not be sent to sibling subdomains.",
    ),
    CookieScenario(
        scenario_id="SC13",
        title="Path root cookie",
        category="path-scope",
        attributes=CookieAttributes(name="path_root", value="nu", path="/"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Expected to match most routes.",
    ),
    CookieScenario(
        scenario_id="SC14",
        title="Path nested cookie",
        category="path-scope",
        attributes=CookieAttributes(name="path_admin", value="xi", path="/admin"),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/admin"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored",
            scope="host-only",
            persistence="session",
            path_scope="/admin",
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="Expected only on /admin subtree.",
    ),
    CookieScenario(
        scenario_id="SC15",
        title="Session cookie",
        category="persistence",
        attributes=CookieAttributes(name="session_only", value="omicron", secure=True),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=False
        ),
        notes="No Max-Age or Expires.",
    ),
    CookieScenario(
        scenario_id="SC16",
        title="Persistent cookie via Max-Age",
        category="persistence",
        attributes=CookieAttributes(
            name="persist_ma", value="pi", max_age=86400, secure=True
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored",
            scope="host-only",
            persistence="persistent",
            path_scope="/",
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=True
        ),
        notes="Lifetime around one day.",
    ),
    CookieScenario(
        scenario_id="SC17",
        title="Persistent cookie via Expires",
        category="persistence",
        attributes=CookieAttributes(
            name="persist_exp", value="rho", expires=_future_date(7), secure=True
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="stored",
            scope="host-only",
            persistence="persistent",
            path_scope="/",
        ),
        extension_expectation=ExtensionExpectation(
            flags=True, parent_domain=False, persistent=True
        ),
        notes="Absolute expiration date in UTC.",
    ),
    CookieScenario(
        scenario_id="SC18",
        title="Immediate expiry delete",
        category="persistence",
        attributes=CookieAttributes(
            name="delete_me", value="sigma", expires=_past_date(), max_age=0
        ),
        request_context=RequestContext(
            scheme="https", host=AppConfig.APP_HOST, path="/"
        ),
        browser_expectation=BrowserExpectation(
            storage="rejected", scope="host-only", persistence="session", path_scope="/"
        ),
        extension_expectation=ExtensionExpectation(
            flags=False, parent_domain=False, persistent=False
        ),
        notes="Set-and-expire immediately should remove or skip storage.",
    ),
]


def get_scenario_map() -> dict[str, CookieScenario]:
    return {scenario.scenario_id: scenario for scenario in SCENARIOS}
