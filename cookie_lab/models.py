from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ScopeType = Literal["host-only", "domain"]
PersistenceType = Literal["session", "persistent"]
StorageResult = Literal["stored", "rejected"]


@dataclass(frozen=True)
class RequestContext:
    scheme: Literal["http", "https"]
    host: str
    path: str


@dataclass(frozen=True)
class BrowserExpectation:
    storage: StorageResult
    scope: ScopeType
    persistence: PersistenceType
    path_scope: str


@dataclass(frozen=True)
class ExtensionExpectation:
    flags: bool
    parent_domain: bool
    persistent: bool


@dataclass(frozen=True)
class CookieAttributes:
    name: str
    value: str
    domain: str | None = None
    path: str = "/"
    secure: bool = False
    httponly: bool = False
    samesite: Literal["Lax", "Strict", "None"] | None = None
    max_age: int | None = None
    expires: str | None = None


@dataclass(frozen=True)
class CookieScenario:
    scenario_id: str
    title: str
    category: str
    attributes: CookieAttributes
    request_context: RequestContext
    browser_expectation: BrowserExpectation
    extension_expectation: ExtensionExpectation
    notes: str
