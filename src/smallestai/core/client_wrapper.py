# Hand-maintained (see .fernignore). Kept out of regeneration to preserve two
# observability customizations in get_headers():
#   1. X-Source: attributes SDK-originated traffic in the backend (ClickHouse
#      channel dimension), matching the convention other clients use
#      (e.g. pipecat sends X-Source: pipecat).
#   2. X-Fern-SDK-Version: sourced from the installed package version instead of
#      the generator's hardcoded "0.0.0", so version adoption is trackable.
#   3. telemetry: Sync/AsyncClientWrapper take a `telemetry` flag (default True) and,
#      when it is on, build the request client from core/_telemetry_http_client.py,
#      which records one anonymous sdk_method_called event per SDK call
#      (see smallestai/telemetry.py). False keeps the plain generated client.
# When re-syncing after a regen, re-apply all three edits below.

import typing

import httpx
from ..environment import SmallestAIEnvironment
from ..version import __version__
from ._telemetry_http_client import TelemetryAsyncHttpClient, TelemetryHttpClient
from .http_client import AsyncHttpClient, HttpClient
from .logging import LogConfig, Logger

# Identifies this SDK as the request source for backend attribution. Language-
# tagged so python/ts/go SDKs are distinguishable.
SOURCE = "smallest-python-sdk"


class BaseClientWrapper:
    def __init__(
        self,
        *,
        api_key: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        environment: SmallestAIEnvironment,
        timeout: typing.Optional[float] = None,
        max_retries: int = 2,
        logging: typing.Optional[typing.Union[LogConfig, Logger]] = None,
    ):
        self._api_key = api_key
        self._headers = headers
        self._environment = environment
        self._timeout = timeout
        self._max_retries = max_retries
        self._logging = logging

    def get_headers(self) -> typing.Dict[str, str]:
        import platform

        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-Runtime": f"python/{platform.python_version()}",
            "X-Fern-Platform": f"{platform.system().lower()}/{platform.release()}",
            "X-Fern-SDK-Name": "smallest-ai",
            "X-Fern-SDK-Version": __version__,
            "X-Source": SOURCE,
            **(self.get_custom_headers() or {}),
        }
        headers["Authorization"] = f"Bearer {self._get_api_key()}"
        return headers

    def _get_api_key(self) -> str:
        if isinstance(self._api_key, str):
            return self._api_key
        else:
            return self._api_key()

    def get_custom_headers(self) -> typing.Optional[typing.Dict[str, str]]:
        return self._headers

    def get_environment(self) -> SmallestAIEnvironment:
        return self._environment

    def get_timeout(self) -> typing.Optional[float]:
        return self._timeout

    def get_max_retries(self) -> int:
        return self._max_retries


class SyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        environment: SmallestAIEnvironment,
        timeout: typing.Optional[float] = None,
        max_retries: int = 2,
        logging: typing.Optional[typing.Union[LogConfig, Logger]] = None,
        httpx_client: httpx.Client,
        telemetry: bool = True,
    ):
        super().__init__(
            api_key=api_key,
            headers=headers,
            environment=environment,
            timeout=timeout,
            max_retries=max_retries,
            logging=logging,
        )
        http_client_cls = TelemetryHttpClient if telemetry else HttpClient
        self.httpx_client = http_client_cls(
            httpx_client=httpx_client,
            base_headers=self.get_headers,
            base_timeout=self.get_timeout,
            base_max_retries=self.get_max_retries(),
            logging_config=self._logging,
        )


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        environment: SmallestAIEnvironment,
        timeout: typing.Optional[float] = None,
        max_retries: int = 2,
        logging: typing.Optional[typing.Union[LogConfig, Logger]] = None,
        async_token: typing.Optional[typing.Callable[[], typing.Awaitable[str]]] = None,
        httpx_client: httpx.AsyncClient,
        telemetry: bool = True,
    ):
        super().__init__(
            api_key=api_key,
            headers=headers,
            environment=environment,
            timeout=timeout,
            max_retries=max_retries,
            logging=logging,
        )
        self._async_token = async_token
        async_http_client_cls = TelemetryAsyncHttpClient if telemetry else AsyncHttpClient
        self.httpx_client = async_http_client_cls(
            httpx_client=httpx_client,
            base_headers=self.get_headers,
            base_timeout=self.get_timeout,
            base_max_retries=self.get_max_retries(),
            async_base_headers=self.async_get_headers,
            logging_config=self._logging,
        )

    async def async_get_headers(self) -> typing.Dict[str, str]:
        headers = self.get_headers()
        if self._async_token is not None:
            token = await self._async_token()
            headers["Authorization"] = f"Bearer {token}"
        return headers
