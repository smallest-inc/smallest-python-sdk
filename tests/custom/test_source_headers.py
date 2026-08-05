"""Every request must carry SDK source-attribution headers.

The backend attributes traffic by the X-Source header (a ClickHouse channel
dimension, same convention pipecat uses with X-Source: pipecat). We also send
the real installed version in X-Fern-SDK-Version instead of the generator's
hardcoded 0.0.0 so version adoption is trackable. See client_wrapper.py.
"""
import re

from smallestai import __version__
from smallestai.core.client_wrapper import SOURCE, BaseClientWrapper
from smallestai.environment import SmallestAIEnvironment


def _headers():
    return BaseClientWrapper(
        api_key="test-key", environment=SmallestAIEnvironment.PRODUCTION
    ).get_headers()


def test_x_source_present():
    assert _headers()["X-Source"] == SOURCE == "smallest-python-sdk"


def test_sdk_version_is_real_not_placeholder():
    version = _headers()["X-Fern-SDK-Version"]
    assert version == __version__
    assert version != "0.0.0"
    assert re.match(r"^\d+\.\d+\.\d+", version), version


def test_version_importable():
    # Regression: version.py looked up the wrong dist name ("smallest-ai") and
    # broke `import smallestai; smallestai.__version__`.
    assert isinstance(__version__, str) and __version__


def test_user_headers_can_override_source():
    headers = BaseClientWrapper(
        api_key="k",
        environment=SmallestAIEnvironment.PRODUCTION,
        headers={"X-Source": "custom"},
    ).get_headers()
    assert headers["X-Source"] == "custom"
