"""
tool_schema.py
LLM tool-calling schema and function registry for civil engineering AI agents.
"""
from gis_client import get_flood_risk

# OpenAI / Gemini / Claude standard function definition
FLOOD_RISK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "flood_risk",
        "description": (
            "Evaluate river discharge forecast and flood risk level for a specific "
            "geographic site given its latitude and longitude. Returns a structured "
            "risk assessment ('low', 'medium', 'high', 'unknown') along with discharge values."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "Latitude coordinate in decimal degrees between -90.0 and 90.0.",
                },
                "lon": {
                    "type": "number",
                    "description": "Longitude coordinate in decimal degrees between -180.0 and 180.0.",
                },
            },
            "required": ["lat", "lon"],
        },
    },
}

# Registry mapping tool name to the Python callable
REGISTRY = {
    "flood_risk": get_flood_risk,
}
