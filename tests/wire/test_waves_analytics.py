import datetime

from .conftest import get_client, verify_request_count


def test_waves_analytics_list_streaming_speech_to_text_logs() -> None:
    """Test listStreamingSpeechToTextLogs endpoint with WireMock"""
    test_id = "waves.analytics.list_streaming_speech_to_text_logs.0"
    client = get_client(test_id)
    client.waves.analytics.list_streaming_speech_to_text_logs()
    verify_request_count(test_id, "GET", "/waves/v1/analytics/asr/logs", None, 1)


def test_waves_analytics_delete_streaming_speech_to_text_history() -> None:
    """Test deleteStreamingSpeechToTextHistory endpoint with WireMock"""
    test_id = "waves.analytics.delete_streaming_speech_to_text_history.0"
    client = get_client(test_id)
    client.waves.analytics.delete_streaming_speech_to_text_history(
        request_id="3eea9859-609b-45c5-8a25-0337c9763c96",
    )
    verify_request_count(
        test_id, "DELETE", "/waves/v1/analytics/asr/history/3eea9859-609b-45c5-8a25-0337c9763c96", None, 1
    )


def test_waves_analytics_get_streaming_speech_to_text_usage_timeseries() -> None:
    """Test getStreamingSpeechToTextUsageTimeseries endpoint with WireMock"""
    test_id = "waves.analytics.get_streaming_speech_to_text_usage_timeseries.0"
    client = get_client(test_id)
    client.waves.analytics.get_streaming_speech_to_text_usage_timeseries(
        from_=datetime.datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-08-07T00:00:00+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/waves/v1/analytics/asr/usage/timeseries",
        {"from": "2026-08-01T00:00:00Z", "to": "2026-08-07T00:00:00Z"},
        1,
    )


def test_waves_analytics_list_text_to_speech_logs() -> None:
    """Test listTextToSpeechLogs endpoint with WireMock"""
    test_id = "waves.analytics.list_text_to_speech_logs.0"
    client = get_client(test_id)
    client.waves.analytics.list_text_to_speech_logs()
    verify_request_count(test_id, "GET", "/waves/v1/analytics/tts/logs", None, 1)


def test_waves_analytics_get_text_to_speech_usage_timeseries() -> None:
    """Test getTextToSpeechUsageTimeseries endpoint with WireMock"""
    test_id = "waves.analytics.get_text_to_speech_usage_timeseries.0"
    client = get_client(test_id)
    client.waves.analytics.get_text_to_speech_usage_timeseries(
        from_=datetime.datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-08-07T00:00:00+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/waves/v1/analytics/tts/usage/timeseries",
        {"from": "2026-08-01T00:00:00Z", "to": "2026-08-07T00:00:00Z"},
        1,
    )


def test_waves_analytics_get_text_to_speech_credits_timeseries() -> None:
    """Test getTextToSpeechCreditsTimeseries endpoint with WireMock"""
    test_id = "waves.analytics.get_text_to_speech_credits_timeseries.0"
    client = get_client(test_id)
    client.waves.analytics.get_text_to_speech_credits_timeseries(
        from_=datetime.datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-08-07T00:00:00+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/waves/v1/analytics/tts/usage/credits/timeseries",
        {"from": "2026-08-01T00:00:00Z", "to": "2026-08-07T00:00:00Z"},
        1,
    )


def test_waves_analytics_get_text_to_speech_concurrency_timeseries() -> None:
    """Test getTextToSpeechConcurrencyTimeseries endpoint with WireMock"""
    test_id = "waves.analytics.get_text_to_speech_concurrency_timeseries.0"
    client = get_client(test_id)
    client.waves.analytics.get_text_to_speech_concurrency_timeseries(
        from_=datetime.datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-08-07T00:00:00+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/waves/v1/analytics/tts/concurrency/timeseries",
        {"from": "2026-08-01T00:00:00Z", "to": "2026-08-07T00:00:00Z"},
        1,
    )


def test_waves_analytics_get_text_to_speech_websocket_connections_timeseries() -> None:
    """Test getTextToSpeechWebsocketConnectionsTimeseries endpoint with WireMock"""
    test_id = "waves.analytics.get_text_to_speech_websocket_connections_timeseries.0"
    client = get_client(test_id)
    client.waves.analytics.get_text_to_speech_websocket_connections_timeseries(
        from_=datetime.datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-08-07T00:00:00+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/waves/v1/analytics/tts/ws-connections/timeseries",
        {"from": "2026-08-01T00:00:00Z", "to": "2026-08-07T00:00:00Z"},
        1,
    )


def test_waves_analytics_list_webhook_logs() -> None:
    """Test listWebhookLogs endpoint with WireMock"""
    test_id = "waves.analytics.list_webhook_logs.0"
    client = get_client(test_id)
    client.waves.analytics.list_webhook_logs()
    verify_request_count(test_id, "GET", "/waves/v1/analytics/webhooks/logs", None, 1)
