import httpx, asyncio, backoff

class BaseHTTPClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def _request(self, method: str, url: str, **kwargs):
        r = await self._client.request(method, url, **kwargs)
        r.raise_for_status()
        return r.json()
