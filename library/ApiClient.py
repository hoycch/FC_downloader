"""
API client — uses headers from builder.build_headers and settings from config.
"""

from __future__ import annotations

import random
import time
from typing import Any, Dict, Mapping, Optional, Union

import requests
import urllib3

from .builder import build_headers   # ← headers come from builder.py
from .config import Config


class ApiClient:
    """
    HTTP client bound to a Config instance.

    Every request builds headers via builder.build_headers(config, ...).
    Timeout, SSL, delays, and endpoints come from config.
    """

    def __init__(
        self,
        config: Config,
        *,
        session: Optional[requests.Session] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
        auto_delay: bool = True,
    ) -> None:
        self.config = config
        self.session = session or requests.Session()
        self.extra_headers = dict(extra_headers) if extra_headers else {}
        self.auto_delay = auto_delay

        if not config.VERIFY_SSL:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _make_headers(
        self, extra_headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, str]:
        """Build headers using builder.py (config values + optional extras)."""
        merged: Dict[str, str] = dict(self.extra_headers)
        if extra_headers:
            merged.update(extra_headers)
        # All base header values come from config via builder.build_headers
        return build_headers(self.config, extra_headers=merged or None)

    def _maybe_delay(self) -> None:
        if self.auto_delay and self.config.MAX_DELAY > 0:
            time.sleep(random.uniform(self.config.MIN_DELAY, self.config.MAX_DELAY))

    def request(
        self,
        method: str,
        url: str,
        *,
        data: Any = None,
        json: Any = None,
        params: Optional[Mapping[str, Any]] = None,
        extra_headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[Union[int, float]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        self._maybe_delay()

        headers = self._make_headers(extra_headers)  # ← from builder.py

        return self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            data=data,
            json=json,
            params=params,
            timeout=timeout if timeout is not None else self.config.REQUEST_TIMEOUT,
            verify=self.config.VERIFY_SSL,
            **kwargs,
        )

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def login(
        self,
        username: str,
        password: str,
    ) -> requests.Response:
        payload: Dict[str, Any] = {
            "username": username,
            "password": password,
        }
        
        cfg = self.config
        payload.update(
        {
            "areaCode": f"+{cfg.area_code}",
            "deviceId": cfg.DEVICE_ID,
            "cId":cfg.DEVICE_ID,
                        
        })
        resp = self.post(
            cfg.LOGIN_URL,
            data=payload,
        )
        
        if resp.json()['info'] != "成功":
            print(resp.json()['info'])
            raise AssertionError(f"{username}: {resp.json()['info']}")
        return resp.json()['row']
    def get_single_json_debug(
        self,
        URL: str,
        token: str,
        data: Any = None,
    ) -> requests.Response:
        method = "POST" if data is not None else "GET"
        return self.post(
            URL,
            data=data,
            # params=params,
            extra_headers={"authorization": f"Bearer {token}"},
        )
    def get_single_json(
        self,
        URL: str,
        token: str,
        data: Any = None,
    ) -> requests.Response:
        method = "POST" if data is not None else "GET"
        return self.post(
            URL,
            data=data,
            # params=params,
            extra_headers={"authorization": f"Bearer {token}"},
        ).json()

    def get_large_json(
        self,
        URL: str,
        token: str,
        data: Any = None,
    ) -> requests.Response:
        extra = {
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }
        if data is not None:
            # JSON body + JSON content-type
            return self.post(URL, json=data, extra_headers=extra)
        # no body
        return self.get(URL, extra_headers=extra)

    
    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()