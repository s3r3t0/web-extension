"""Configuration values for Cookie Lab hostnames and scheme."""

from __future__ import annotations

import os


class AppConfig:
    """Environment-backed application host configuration."""

    BASE_DOMAIN = os.environ.get("COOKIE_LAB_BASE_DOMAIN", "localtest.me")
    APP_HOST = os.environ.get("COOKIE_LAB_APP_HOST", "app.localtest.me")
    API_HOST = os.environ.get("COOKIE_LAB_API_HOST", "api.localtest.me")
    DEFAULT_SCHEME = os.environ.get("COOKIE_LAB_SCHEME", "https")
