"""
Configuration module.

Selects BASE_URL (and derived URLs) based on area_code and exposes
all settings used by the rest of the application, including the
base HTTP header values.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Union
from urllib.parse import urlparse


# Mapping of area_code → CloudFront base URL
_AREA_CODE_BASE_URLS = {
    "852": "https://dhzx6onj3zqr3.cloudfront.net",
    "853": "https://dhzx6onj3zqr3.cloudfront.net",
    "65": "https://d1vqujo8itcqpm.cloudfront.net",
    "82": "https://d29m8ihcfwtow5.cloudfront.net",
    "84": "https://d1icj6ewkl9j2u.cloudfront.net",
}


@dataclass(frozen=True)
class Config:
    """Immutable configuration for a given area_code."""

    area_code: str
    BASE_URL: str
    LOGIN_URL: str
    AUTH_CHECK_URL: str
    USER_INFO_URL: str
    TEAM_INFO_URL: str
    TEAM_MEMBERS_URL: str
    INPUT_FILE: str
    OUTPUT_DIR: Path
    DEVICE_ID: str
    REQUEST_TIMEOUT: int
    MIN_DELAY: float
    MAX_DELAY: float
    VERIFY_SSL: bool

    # ── Base HTTP header values (all header data lives here) ──
    HOST: str
    CONTENT_TYPE: str
    COOKIE: str
    CHECK_IP_REALIP: str
    CONNECTION: str
    ACCEPT: str
    USER_AGENT: str
    ACCEPT_LANGUAGE: str
    ACCEPT_ENCODING: str
    BUSINESSLANG: str

    @property
    def host(self) -> str:
        """Alias for HOST (hostname for the Host header)."""
        return self.HOST


def get_config(area_code: Union[int, str]) -> Config:
    """
    Return a Config instance for the given area_code.

    Supported area codes:
        852, 853 → https://dhzx6onj3zqr3.cloudfront.net
        65       → https://d1vqujo8itcqpm.cloudfront.net
        82       → https://d29m8ihcfwtow5.cloudfront.net
        84       → https://d1icj6ewkl9j2u.cloudfront.net

    Raises:
        ValueError: if the area_code is not supported.
    """
    code = str(area_code).strip()
    base_url = _AREA_CODE_BASE_URLS.get(code)
    if base_url is None:
        supported = ", ".join(sorted(_AREA_CODE_BASE_URLS.keys()))
        raise ValueError(
            f"Unsupported area_code '{area_code}'. "
            f"Supported values: {supported}"
        )

    host = urlparse(base_url).netloc

    return Config(
        area_code=code,
        BASE_URL=base_url,
        LOGIN_URL=f"{base_url}/api/user/login",
        AUTH_CHECK_URL=f"{base_url}/api/invest/auth/check",
        USER_INFO_URL=f"{base_url}/api/user/getUserInfo",
        TEAM_INFO_URL=f"{base_url}/api/user/team/getTeamInfo",
        TEAM_MEMBERS_URL=f"{base_url}/api/user/team/getTeamMemberList",
        INPUT_FILE="successful.csv",
        OUTPUT_DIR=Path("results"),
        DEVICE_ID="5f3fbd80c94874e6789e781ad0dd9efe",
        REQUEST_TIMEOUT=30,
        MIN_DELAY=2.0,
        MAX_DELAY=5.0,
        VERIFY_SSL=False,
        # Header values
        HOST=host,
        CONTENT_TYPE="application/x-www-form-urlencoded",
        COOKIE="SITE_TOTAL_ID=4d913556bb7defb4af2006d9732e48e6",
        CHECK_IP_REALIP="221.127.137.240",
        CONNECTION="keep-alive",
        ACCEPT="*/*",
        USER_AGENT=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
            "Html5Plus/1.0 (Immersed/20) uni-app"
        ),
        ACCEPT_LANGUAGE="zh_HANT",
        ACCEPT_ENCODING="gzip, deflate, br",
        BUSINESSLANG="zh_HANT",
    )


def generate_config_snippet(area_code: Union[int, str]) -> str:
    """Return a string that looks like a traditional config.py module."""
    cfg = get_config(area_code)
    return f'''from pathlib import Path


BASE_URL = "{cfg.BASE_URL}"

INPUT_FILE = "successful.csv"

OUTPUT_DIR = Path("results")

DEVICE_ID = "5f3fbd80c94874e6789e781ad0dd9efe"

REQUEST_TIMEOUT = 30

MIN_DELAY = 2.0
MAX_DELAY = 5.0

VERIFY_SSL = False


USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "Html5Plus/1.0 (Immersed/20) uni-app"
)
'''
