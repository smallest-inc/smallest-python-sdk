# Hand-maintained (see .fernignore). Telemetry hook for SDK method calls.
#
# Every generated endpoint method sends its HTTP call through
# client_wrapper.httpx_client (an HttpClient / AsyncHttpClient from the generated
# core/http_client.py). client_wrapper.py (also fernignored) swaps in the subclasses
# below when telemetry is on, so no generated file needs to know about telemetry.
#
# Each subclass passes every argument straight through to the generated client and
# returns its response or re-raises its exception untouched. The only addition is one
# smallestai.telemetry.record_method() call per SDK method call, which queues a tiny
# event and returns immediately. Retries (retries > 0) are recursive calls into the
# same request() and are not counted again. When telemetry is off (env opt-out, pytest,
# CI) each call checks runtime_enabled() first and goes straight to the generated
# client, without walking frames.

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


def _record_response(method: str, response: httpx.Response) -> None:
    try:
        status = response.status_code
        if status < 400:
            telemetry.record_method(method, success=True)
        else:
            telemetry.record_method(method, success=False, error_type="ApiError", http_status=status)
    except Exception:
        pass


def _record_exception(method: str, exc: BaseException) -> None:
    try:
        telemetry.record_method(method, success=False, error_type=type(exc).__name__)
    except Exception:
        pass


def _enabled() -> bool:
    try:
        return telemetry.runtime_enabled()
    except Exception:
        return False


def _is_retry(kwargs: typing.Dict[str, typing.Any]) -> bool:
    try:
        return int(kwargs.get("retries") or 0) > 0
    except Exception:
        return False


class TelemetryHttpClient(HttpClient):
    def request(self, *args: typing.Any, **kwargs: typing.Any) -> httpx.Response:
        if _is_retry(kwargs) or not _enabled():
            return super().request(*args, **kwargs)
        method = _caller_method_name()
        try:
            response = super().request(*args, **kwargs)
        except Exception as exc:
            _record_exception(method, exc)
            raise
        _record_response(method, response)
        return response

    @contextlib.contextmanager
    def stream(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Iterator[httpx.Response]:
        if not _enabled():
            with super().stream(*args, **kwargs) as response:
                yield response
            return
        method = _caller_method_name()
        entered = False
        try:
            with super().stream(*args, **kwargs) as response:
                entered = True
                _record_response(method, response)
                yield response
        except Exception as exc:
            if not entered:
                _record_exception(method, exc)
            raise


class TelemetryAsyncHttpClient(AsyncHttpClient):
    async def request(self, *args: typing.Any, **kwargs: typing.Any) -> httpx.Response:
        if _is_retry(kwargs) or not _enabled():
            return await super().request(*args, **kwargs)
        method = _caller_method_name()
        try:
            response = await super().request(*args, **kwargs)
        except Exception as exc:
            _record_exception(method, exc)
            raise
        _record_response(method, response)
        return response

    @contextlib.asynccontextmanager
    async def stream(self, *args: typing.Any, **kwargs: typing.Any) -> typing.AsyncIterator[httpx.Response]:
        if not _enabled():
            async with super().stream(*args, **kwargs) as response:
                yield response
            return
        method = _caller_method_name()
        entered = False
        try:
            async with super().stream(*args, **kwargs) as response:
                entered = True
                _record_response(method, response)
                yield response
        except Exception as exc:
            if not entered:
                _record_exception(method, exc)
            raise
