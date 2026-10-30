# GIS Flood Risk Tool for Civil Engineering AI

A lightweight, robust Python client designed to test GIS flood risk API integration locally before connecting to LLM tool-calling systems.

## Project Structure

- `gis_client.py`: Core client with `get_flood_risk(lat, lon)`. Validates coordinates, calls API with 10s timeout, safely parses response, and guarantees no crashes.
- `tool_schema.py`: LLM tool definition (JSON schema) and `REGISTRY` mapping the function name `flood_risk` to `get_flood_risk`.
- `run_demo.py`: Interactive script testing direct calls, LLM tool dispatch, and invalid inputs.
- `test_gis.py`: Pytest suite covering live API calls, coordinate validation, and mocked network/HTTP failures.
- `requirements.txt`: Minimal dependencies (`requests`, `python-dotenv`, `pytest`).
- `.env.example` / `.env`: Configurable API base URL, optional API key, and test coordinates.

## Setup Instructions

### 1. Create Virtual Environment
- **Windows (PowerShell / Command Prompt)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration (.env)
Copy `.env.example` to `.env`:
- **Windows**: `copy .env.example .env`
- **macOS / Linux**: `cp .env.example .env`

*(Uses Open-Meteo Flood API by default - no API key required)*

## Running the Demo

Execute the demo script:
```bash
python run_demo.py
```

## Running the Tests

Execute pytest with verbose output:
```bash
pytest -v
```

## LLM Integration Example

```python
from tool_schema import REGISTRY, FLOOD_RISK_TOOL_SCHEMA

# Pass FLOOD_RISK_TOOL_SCHEMA to your model (OpenAI / Gemini / Anthropic)
# When the model invokes "flood_risk" with arguments:
result = REGISTRY["flood_risk"](lat=29.7604, lon=-95.3698)
print(result)
```
