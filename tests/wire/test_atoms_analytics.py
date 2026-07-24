import datetime

from .conftest import get_client, verify_request_count


def test_atoms_analytics_get_call_counts_log() -> None:
    """Test getCallCountsLog endpoint with WireMock"""
    test_id = "atoms.analytics.get_call_counts_log.0"
    client = get_client(test_id)
    client.atoms.analytics.get_call_counts_log()
    verify_request_count(test_id, "GET", "/analytics/call-counts-log", None, 1)


def test_atoms_analytics_get_call_counts_by_day() -> None:
    """Test getCallCountsByDay endpoint with WireMock"""
    test_id = "atoms.analytics.get_call_counts_by_day.0"
    client = get_client(test_id)
    client.atoms.analytics.get_call_counts_by_day()
    verify_request_count(test_id, "GET", "/analytics/call-counts-by-day", None, 1)


def test_atoms_analytics_get_conversation_details() -> None:
    """Test getConversationDetails endpoint with WireMock"""
    test_id = "atoms.analytics.get_conversation_details.0"
    client = get_client(test_id)
    client.atoms.analytics.get_conversation_details(
        call_id="callId",
    )
    verify_request_count(test_id, "GET", "/analytics/conversation-details/callId", None, 1)


def test_atoms_analytics_get_usage_timeseries() -> None:
    """Test getUsageTimeseries endpoint with WireMock"""
    test_id = "atoms.analytics.get_usage_timeseries.0"
    client = get_client(test_id)
    client.atoms.analytics.get_usage_timeseries()
    verify_request_count(test_id, "GET", "/analytics/usage/timeseries", None, 1)


def test_atoms_analytics_get_dashboard() -> None:
    """Test getDashboard endpoint with WireMock"""
    test_id = "atoms.analytics.get_dashboard.0"
    client = get_client(test_id)
    client.atoms.analytics.get_dashboard()
    verify_request_count(test_id, "GET", "/analytics/dashboard", None, 1)


def test_atoms_analytics_get_analytics_summary() -> None:
    """Test getAnalyticsSummary endpoint with WireMock"""
    test_id = "atoms.analytics.get_analytics_summary.0"
    client = get_client(test_id)
    client.atoms.analytics.get_analytics_summary()
    verify_request_count(test_id, "GET", "/analytics/summary", None, 1)


def test_atoms_analytics_get_call_volume_timeseries() -> None:
    """Test getCallVolumeTimeseries endpoint with WireMock"""
    test_id = "atoms.analytics.get_call_volume_timeseries.0"
    client = get_client(test_id)
    client.atoms.analytics.get_call_volume_timeseries()
    verify_request_count(test_id, "GET", "/analytics/call-volume-timeseries", None, 1)


def test_atoms_analytics_get_pickup_rate_by_number() -> None:
    """Test getPickupRateByNumber endpoint with WireMock"""
    test_id = "atoms.analytics.get_pickup_rate_by_number.0"
    client = get_client(test_id)
    client.atoms.analytics.get_pickup_rate_by_number()
    verify_request_count(test_id, "GET", "/analytics/pickup-rate-by-number", None, 1)


def test_atoms_analytics_get_phone_number_trends() -> None:
    """Test getPhoneNumberTrends endpoint with WireMock"""
    test_id = "atoms.analytics.get_phone_number_trends.0"
    client = get_client(test_id)
    client.atoms.analytics.get_phone_number_trends()
    verify_request_count(test_id, "GET", "/analytics/phone-number-trends", None, 1)


def test_atoms_analytics_get_hourly_performance() -> None:
    """Test getHourlyPerformance endpoint with WireMock"""
    test_id = "atoms.analytics.get_hourly_performance.0"
    client = get_client(test_id)
    client.atoms.analytics.get_hourly_performance()
    verify_request_count(test_id, "GET", "/analytics/hourly-performance", None, 1)


def test_atoms_analytics_get_call_outcomes_timeseries() -> None:
    """Test getCallOutcomesTimeseries endpoint with WireMock"""
    test_id = "atoms.analytics.get_call_outcomes_timeseries.0"
    client = get_client(test_id)
    client.atoms.analytics.get_call_outcomes_timeseries()
    verify_request_count(test_id, "GET", "/analytics/call-outcomes-timeseries", None, 1)


def test_atoms_analytics_get_duration_stats() -> None:
    """Test getDurationStats endpoint with WireMock"""
    test_id = "atoms.analytics.get_duration_stats.0"
    client = get_client(test_id)
    client.atoms.analytics.get_duration_stats()
    verify_request_count(test_id, "GET", "/analytics/duration-stats", None, 1)


def test_atoms_analytics_get_weekly_trends() -> None:
    """Test getWeeklyTrends endpoint with WireMock"""
    test_id = "atoms.analytics.get_weekly_trends.0"
    client = get_client(test_id)
    client.atoms.analytics.get_weekly_trends()
    verify_request_count(test_id, "GET", "/analytics/weekly-trends", None, 1)


def test_atoms_analytics_get_agent_performance() -> None:
    """Test getAgentPerformance endpoint with WireMock"""
    test_id = "atoms.analytics.get_agent_performance.0"
    client = get_client(test_id)
    client.atoms.analytics.get_agent_performance()
    verify_request_count(test_id, "GET", "/analytics/agent-performance", None, 1)


def test_atoms_analytics_get_analytics_concurrency() -> None:
    """Test getAnalyticsConcurrency endpoint with WireMock"""
    test_id = "atoms.analytics.get_analytics_concurrency.0"
    client = get_client(test_id)
    client.atoms.analytics.get_analytics_concurrency(
        date=datetime.date.fromisoformat("2023-01-15"),
    )
    verify_request_count(test_id, "GET", "/analytics/concurrency", {"date": "2023-01-15"}, 1)


def test_atoms_analytics_get_call_start_distribution() -> None:
    """Test getCallStartDistribution endpoint with WireMock"""
    test_id = "atoms.analytics.get_call_start_distribution.0"
    client = get_client(test_id)
    client.atoms.analytics.get_call_start_distribution(
        date=datetime.date.fromisoformat("2023-01-15"),
    )
    verify_request_count(test_id, "GET", "/analytics/call-start-distribution", {"date": "2023-01-15"}, 1)


def test_atoms_analytics_get_daily_call_summary() -> None:
    """Test getDailyCallSummary endpoint with WireMock"""
    test_id = "atoms.analytics.get_daily_call_summary.0"
    client = get_client(test_id)
    client.atoms.analytics.get_daily_call_summary(
        date=datetime.date.fromisoformat("2023-01-15"),
    )
    verify_request_count(test_id, "GET", "/analytics/daily-call-summary", {"date": "2023-01-15"}, 1)


def test_atoms_analytics_get_attempt_cohort() -> None:
    """Test getAttemptCohort endpoint with WireMock"""
    test_id = "atoms.analytics.get_attempt_cohort.0"
    client = get_client(test_id)
    client.atoms.analytics.get_attempt_cohort()
    verify_request_count(test_id, "GET", "/analytics/attempt-cohort", None, 1)
