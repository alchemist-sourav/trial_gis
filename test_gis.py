"""
test_gis.py
Pytest suite verifying live requests, input validation, and failure mocks.
"""
from unittest.mock import Mock, patch
import requests
from gis_client import get_flood_risk

TEST_LAT = 29.7604
TEST_LON = -95.3698


def test_live_api_call():
    """Verify a live API call returns standard schema without crashing."""
    result = get_flood_risk(TEST_LAT, TEST_LON)
    assert isinstance(result, dict)
    assert result["risk"] in ["low", "medium", "high", "unknown"]
    assert result["source"] == "Open-Meteo Flood API"
    assert result["error"] is None
    assert isinstance(result["values"], dict)


def test_invalid_coordinates():
    """Verify input validation handles bad numbers and bounds without exceptions."""
    # Out of bounds latitude (> 90)
    out_of_bounds = get_flood_risk(125.0, -95.3698)
    assert out_of_bounds["risk"] == "unknown"
    assert "Out-of-range" in out_of_bounds["error"]

    # Non-numeric coordinate
    bad_type = get_flood_risk("invalid_lat", -95.3698)
    assert bad_type["risk"] == "unknown"
    assert "must be numbers" in bad_type["error"]


@patch("gis_client.requests.get")
def test_mocked_network_timeout(mock_get):
    """Verify timeout is caught gracefully and returns unknown risk."""
    mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
    result = get_flood_risk(TEST_LAT, TEST_LON)
    assert result["risk"] == "unknown"
    assert "timed out" in result["error"].lower()
    assert result["values"] == {}


@patch("gis_client.requests.get")
def test_mocked_server_error(mock_get):
    """Verify HTTP 500 error is caught gracefully."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Internal Server Error", response=mock_response
    )
    mock_get.return_value = mock_response

    result = get_flood_risk(TEST_LAT, TEST_LON)
    assert result["risk"] == "unknown"
    assert "500" in result["error"]
