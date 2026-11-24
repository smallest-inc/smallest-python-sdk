# Hand-maintained (see .fernignore). Telemetry hook for SDK method calls.
#
# Every generated endpoint method sends its HTTP call through
# client_wrapper.httpx_client (an HttpClient / AsyncHttpClient from the generated
# core/http_client.py). client_wrapper.py (also fernignored) swaps in the subclasses
# below when telemetry is on, so no generated file needs to know about telemetry.
#
# Each subclass passes every argument straight through to the generated client and
# returns its response or re-raises its exception untouched. Each SDK method call first
# asks smallestai.telemetry.sampled_rate() whether to record it (telemetry on, and kept
# by the per-event sample, default 10%). If not, the call goes straight to the generated
# client without walking frames. If so, the method name is resolved and one tiny event
# is queued via telemetry.record_sampled(), which returns immediately. Retries
# (retries > 0) are recursive calls into the same request() and are not counted again.

import contextlib
import sys
import typing

import httpx
from .. import telemetry
from .http_client import AsyncHttpClient, HttpClient

_SKIP_NAME_PARTS = {"raw_client", "client"}


def _caller_method_name() -> str:
    """Name of the SDK method that issued this request, e.g. "waves.voices.get_voices".

    Taken from code identifiers only (module path + function name of the nearest
    generated client frame), never from arguments, URLs or data.
    """
    try:
        frame: typing.Any = sys._getframe(2)
        for _ in range(16):
            if frame is None:
                break
            module = frame.f_globals.get("__name__", "")
            if module.startswith("smallestai.") and not module.startswith("smallestai.core"):
                parts = [p for p in module.split(".")[1:] if p not in _SKIP_NAME_PARTS]
                return ".".join(parts + [frame.f_code.co_name])
            frame = frame.f_back
    except Exception:
        pass
    return "unknown"


def _record_response(method: str, rate: float, response: httpx.Response) -> None:
    try:
        status = response.status_code
        if status < 400:
            telemetry.record_sampled(method, sample_rate=rate, success=True)
        else:
            telemetry.record_sampled(method, sample_rate=rate, success=False, error_type="ApiError", http_status=status)
    except Exception:
        pass


def _record_exception(method: str, rate: float, exc: BaseException) -> None:
    try:
        telemetry.record_sampled(method, sample_rate=rate, success=False, error_type=type(exc).__name__)
    except Exception:
        pass


def _sample() -> typing.Optional[float]:
    """The sample rate if this call should be recorded, else None (off or sampled out)."""
    try:
        return telemetry.sampled_rate()
    except Exception:
        return None


def _is_retry(kwargs: typing.Dict[str, typing.Any]) -> bool:
    try:
        return int(kwargs.get("retries") or 0) > 0
    except Exception:
        return False


class TelemetryHttpClient(HttpClient):
    def request(self, *args: typing.Any, **kwargs: typing.Any) -> httpx.Response:
        rate = None if _is_retry(kwargs) else _sample()
        if rate is None:
            return super().request(*args, **kwargs)
        method = _caller_method_name()
        try:
            response = super().request(*args, **kwargs)
        except Exception as exc:
            _record_exception(method, rate, exc)
            raise
        _record_response(method, rate, response)
        return response

    @contextlib.contextmanager
    def stream(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Iterator[httpx.Response]:
        rate = _sample()
        if rate is None:
            with super().stream(*args, **kwargs) as response:
                yield response
            return
        method = _caller_method_name()
        entered = False
        try:
            with super().stream(*args, **kwargs) as response:
                entered = True
                _record_response(method, rate, response)
                yield response
        except Exception as exc:
            if not entered:
                _record_exception(method, rate, exc)
            raise


class TelemetryAsyncHttpClient(AsyncHttpClient):
    async def request(self, *args: typing.Any, **kwargs: typing.Any) -> httpx.Response:
        rate = None if _is_retry(kwargs) else _sample()
        if rate is None:
            return await super().request(*args, **kwargs)
        method = _caller_method_name()
        try:
            response = await super().request(*args, **kwargs)
        except Exception as exc:
            _record_exception(method, rate, exc)
            raise
        _record_response(method, rate, response)
        return response

    @contextlib.asynccontextmanager
    async def stream(self, *args: typing.Any, **kwargs: typing.Any) -> typing.AsyncIterator[httpx.Response]:
        rate = _sample()
        if rate is None:
            async with super().stream(*args, **kwargs) as response:
                yield response
            return
        method = _caller_method_name()
        entered = False
        try:
            async with super().stream(*args, **kwargs) as response:
                entered = True
                _record_response(method, rate, response)
                yield response
        except Exception as exc:
            if not entered:
                _record_exception(method, rate, exc)
            raise
