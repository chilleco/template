"""Base HTTP client used for third-party integrations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from app.core.config import settings


class BaseServiceClient:
    """Reusable HTTP client with unified request/response hooks."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 10.0,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.base_url = base_url
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={"User-Agent": f"{settings.project_name}/backend"} | (dict(headers) if headers else {}),
            http2=True,
        )

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        resp = await self._client.request(method, url, **kwargs)
        if resp.is_error:
            await self.handle_error(resp)
        return resp

    async def handle_error(self, response: httpx.Response) -> None:
        raise httpx.HTTPStatusError("External service returned error", request=response.request, response=response)

    async def close(self) -> None:
        await self._client.aclose()


class PaymentsGateway(BaseServiceClient):
    """Example domain wrapper for payment providers sharing normalized interface."""

    async def create_payment(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self.request("POST", "/payments", json=payload)
        return response.json()

    async def refund(self, payment_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self.request("POST", f"/payments/{payment_id}/refund", json=payload)
        return response.json()


__all__ = ["BaseServiceClient", "PaymentsGateway"]
