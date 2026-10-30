"""gis_client.py: Queries flood discharge metrics and evaluates flood risk."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("GIS_API_URL", "https://flood-api.open-meteo.com/v1/flood")
API_KEY = os.getenv("GIS_API_KEY", "")
SOURCE_NAME = os.getenv("GIS_SOURCE_NAME", "Open-Meteo Flood API")


def get_flood_risk(lat: float, lon: float) -> dict:
    """Assess flood risk for given coordinates. Never raises exceptions."""
    try:
        lat, lon = float(lat), float(lon)
    except (TypeError, ValueError):
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME,
                "error": f"Coordinates must be numbers. Received lat={lat}, lon={lon}."}

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME,
                "error": f"Out-of-range: lat ({lat}) in [-90, 90], lon ({lon}) in [-180, 180]."}

    params = {
        "latitude": lat, "longitude": lon,
        "daily": ["river_discharge", "river_discharge_mean", "river_discharge_max"],
        "forecast_days": 7,
    }
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

    try:
        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME, "error": "Request timed out after 10s."}
    except requests.exceptions.HTTPError as err:
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME, "error": f"HTTP error {resp.status_code}: {err}"}
    except requests.exceptions.RequestException as err:
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME, "error": f"Network error: {err}"}
    except ValueError as err:
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME, "error": f"Malformed JSON: {err}"}

    try:
        daily = data.get("daily", {})
        discharge = daily.get("river_discharge", [])
        valid_max = [v for v in daily.get("river_discharge_max", []) if v is not None]
        valid_mean = [v for v in daily.get("river_discharge_mean", []) if v is not None]

        if not valid_max and not valid_mean:
            return {"risk": "low", "values": {"note": "No active river basins near coordinates."},
                    "source": SOURCE_NAME, "error": None}

        peak_max = max(valid_max) if valid_max else 0.0
        avg_mean = (sum(valid_mean) / len(valid_mean)) if valid_mean else 1.0
        ratio = (peak_max / avg_mean) if avg_mean > 0 else 1.0

        if ratio >= 2.5 or peak_max >= 250.0:
            risk = "high"
        elif ratio >= 1.5 or peak_max >= 50.0:
            risk = "medium"
        else:
            risk = "low"

        values = {
            "current_discharge_m3s": discharge[0] if discharge else None,
            "peak_forecast_discharge_m3s": round(peak_max, 2),
            "mean_discharge_m3s": round(avg_mean, 2),
            "discharge_ratio": round(ratio, 2),
            "forecast_days": len(discharge),
        }
        return {"risk": risk, "values": values, "source": SOURCE_NAME, "error": None}
    except Exception as err:
        return {"risk": "unknown", "values": {}, "source": SOURCE_NAME, "error": f"Parsing error: {err}"}
