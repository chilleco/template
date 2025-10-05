from __future__ import annotations

from typing import Any, Callable

import httpx

from app.core.settings import settings


class ExternalServiceError(Exception):
    pass


class BaseAPIClient:
    def __init__(self, base_url: str, *, timeout: float = 10.0, headers: dict[str, str] | None = None) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self._client: httpx.AsyncClient | None = None

    async def _client_instance(self) -> httpx.AsyncClient:
        if not self._client:
            self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout, headers=self.headers)
        return self._client

    async def request(self, method: str, path: str, *, json: Any | None = None, params: dict[str, Any] | None = None) -> Any:
        client = await self._client_instance()
        response = await client.request(method, path, json=json, params=params)
        if response.status_code >= 400:
            raise ExternalServiceError(response.text)
        return response.json()

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None


class PaymentsGateway:
    def __init__(self, client_factory: Callable[[str], BaseAPIClient]) -> None:
        self.client_factory = client_factory

    async def charge(self, provider: str, payload: dict[str, Any]) -> Any:
        client = self.client_factory(provider)
        return await client.request("POST", "/charges", json=payload)


def default_client_factory(provider: str) -> BaseAPIClient:
    base_urls = {
        "stripe": "https://api.stripe.com/v1",
        "yookassa": "https://api.yookassa.ru/v3",
    }
    url = base_urls.get(provider)
    if not url:
        raise ExternalServiceError(f"Unknown provider {provider}")
    return BaseAPIClient(url)
