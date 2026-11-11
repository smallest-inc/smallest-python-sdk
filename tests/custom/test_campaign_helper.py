"""Campaign caller-ID payload and legacy compatibility, without network access."""

import warnings
from unittest.mock import Mock

import pytest
import requests

import smallestai.atoms.helpers.campaign as campaign_mod
from smallestai.atoms.helpers import Campaign


@pytest.fixture
def post(monkeypatch):
    post = Mock()
    post.return_value.json.return_value = {"status": True, "data": {"_id": "campaign"}}
    monkeypatch.setattr(campaign_mod.requests, "post", post)
    return post


def test_from_numbers_payload(post):
    campaign = Campaign(base_url="https://api.example/atoms/v1", api_key="sk_test", request_timeout=2)
    numbers = ["+14155552671", "+442079460123"]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = campaign.create("Campaign", "agent", "audience", from_numbers=numbers)
    assert not caught
    post.assert_called_once_with(
        "https://api.example/atoms/v1/campaign",
        headers={"Authorization": "Bearer sk_test", "Content-Type": "application/json"},
        json={
            "name": "Campaign",
            "agentId": "agent",
            "audienceId": "audience",
            "description": "",
            "maxRetries": 3,
            "retryDelay": 15,
            "fromNumbers": numbers,
        },
        timeout=2,
    )
    post.return_value.raise_for_status.assert_called_once_with()
    assert result == {"status": True, "data": {"_id": "campaign"}}


def test_legacy_positional_arguments_warn_and_remain_compatible(post):
    with pytest.warns(DeprecationWarning, match="phone_ids.*from_numbers.*telephony-migration") as caught:
        Campaign().create("Campaign", "agent", "audience", ["product"], "Description", 2, 10)
    assert caught[0].filename == __file__
    payload = post.call_args.kwargs["json"]
    assert payload["phoneNumberIds"] == ["product"]
    assert "fromNumbers" not in payload
    assert (payload["description"], payload["maxRetries"], payload["retryDelay"]) == ("Description", 2, 10)


def test_both_fields_are_sent_for_server_precedence(post):
    with pytest.warns(DeprecationWarning):
        Campaign().create("Campaign", "agent", "audience", phone_ids=["product"], from_numbers=["+123"])
    payload = post.call_args.kwargs["json"]
    assert payload["fromNumbers"] == ["+123"]
    assert payload["phoneNumberIds"] == ["product"]


@pytest.mark.parametrize("numbers", [[""], ["123"], [" +123"], [None], [123], ["+123", "bad"], "+123"])
def test_invalid_numbers_rejected_before_http(post, numbers):
    with pytest.raises(ValueError, match="from_numbers"):
        Campaign().create("Campaign", "agent", "audience", from_numbers=numbers)
    post.assert_not_called()


def test_missing_caller_ids_rejected_before_http(post):
    with pytest.raises(ValueError, match="from_numbers or phone_ids"):
        Campaign().create("Campaign", "agent", "audience")
    post.assert_not_called()


@pytest.mark.parametrize("numbers", [[], ["+"], ["+server-validates-this"]])
def test_number_resolution_and_full_e164_validation_left_to_server(post, numbers):
    post.return_value.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
    with pytest.raises(requests.HTTPError):
        Campaign().create("Campaign", "agent", "audience", from_numbers=numbers)
    assert post.call_args.kwargs["json"]["fromNumbers"] == numbers
    post.return_value.json.assert_not_called()
