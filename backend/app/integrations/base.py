"""Base HTTP client for external API integrations."""
from typing import Any, Literal
from httpx import AsyncClient, Response, HTTPStatusError, Timeout
from loguru import logger
from app.core.exceptions import ExternalServiceError


class BaseAPIClient:
    """Base class for external API clients with retry logic and error handling."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize API client.

        Args:
            base_url: Base URL for API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = Timeout(timeout)
        self.max_retries = max_retries
        self.client: AsyncClient | None = None

    async def __aenter__(self) -> "BaseAPIClient":
        """Async context manager entry."""
        self.client = AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    def _get_headers(self, additional_headers: dict[str, str] | None = None) -> dict[str, str]:
        """
        Get request headers with authentication.

        Args:
            additional_headers: Additional headers to include

        Returns:
            Headers dictionary
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        if additional_headers:
            headers.update(additional_headers)

        return headers

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            Response JSON data

        Raises:
            ExternalServiceError: If request fails after retries
        """
        if not self.client:
            raise ExternalServiceError(
                service=self.__class__.__name__,
                message="Client not initialized. Use 'async with' context manager.",
            )

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(kwargs.pop("headers", None))

        for attempt in range(self.max_retries):
            try:
                logger.debug(f"{method} {url} (attempt {attempt + 1}/{self.max_retries})")

                response: Response = await self.client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    **kwargs,
                )

                response.raise_for_status()

                # Return JSON if available
                try:
                    return response.json()
                except Exception:
                    return {"data": response.text}

            except HTTPStatusError as e:
                logger.error(
                    f"HTTP error {e.response.status_code} from {url}: {e.response.text}"
                )

                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    raise ExternalServiceError(
                        service=self.__class__.__name__,
                        message=f"Client error: {e.response.text}",
                        details={
                            "status_code": e.response.status_code,
                            "url": url,
                        },
                    )

                # Retry on server errors (5xx)
                if attempt == self.max_retries - 1:
                    raise ExternalServiceError(
                        service=self.__class__.__name__,
                        message=f"Server error after {self.max_retries} retries",
                        details={
                            "status_code": e.response.status_code,
                            "url": url,
                        },
                    )

            except Exception as e:
                logger.error(f"Request error to {url}: {str(e)}")

                if attempt == self.max_retries - 1:
                    raise ExternalServiceError(
                        service=self.__class__.__name__,
                        message=f"Request failed: {str(e)}",
                        details={"url": url},
                    )

        # This shouldn't be reached, but just in case
        raise ExternalServiceError(
            service=self.__class__.__name__,
            message="Request failed unexpectedly",
        )

    async def get(self, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """GET request."""
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """POST request."""
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """PUT request."""
        return await self._request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """PATCH request."""
        return await self._request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """DELETE request."""
        return await self._request("DELETE", endpoint, **kwargs)


# Example integration: Stripe payment client
class StripeClient(BaseAPIClient):
    """Stripe API client example."""

    def __init__(self, api_key: str) -> None:
        super().__init__(
            base_url="https://api.stripe.com/v1",
            api_key=api_key,
        )

    async def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create Stripe payment intent.

        Args:
            amount: Amount in cents
            currency: Currency code
            metadata: Additional metadata

        Returns:
            Payment intent data
        """
        return await self.post(
            "/payment_intents",
            data={
                "amount": amount,
                "currency": currency,
                "metadata": metadata or {},
            },
        )
