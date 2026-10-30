"""
run_demo.py
Demonstration script testing get_flood_risk and tool-calling execution.
"""
import os
from dotenv import load_dotenv
from gis_client import get_flood_risk
from tool_schema import REGISTRY

load_dotenv()

TEST_LAT = float(os.getenv("TEST_LAT", "29.7604"))
TEST_LON = float(os.getenv("TEST_LON", "-95.3698"))


def main():
    print("=" * 65)
    print("      GIS FLOOD RISK CLIENT DEMO (Civil Engineering AI Tool)     ")
    print("=" * 65)
    print(f"Target Site: Latitude {TEST_LAT}, Longitude {TEST_LON}")
    print("Executing API request with 10s timeout...\n")

    # 1. Direct function call
    result = get_flood_risk(TEST_LAT, TEST_LON)
    print("[1] Direct Call: get_flood_risk(lat, lon)")
    print("-" * 45)
    print(f"  Risk Assessment : {result['risk'].upper()}")
    print(f"  Data Source     : {result['source']}")
    print(f"  Error Status    : {result['error']}")
    print("  Forecast Metrics:")
    for key, val in result["values"].items():
        print(f"    - {key}: {val}")

    # 2. Execution via LLM Tool Registry
    print("\n[2] LLM Tool Registry Call: REGISTRY['flood_risk'](lat, lon)")
    print("-" * 45)
    tool_func = REGISTRY.get("flood_risk")
    llm_sim_result = tool_func(lat=TEST_LAT, lon=TEST_LON)
    print(f"  Dispatched Tool  : flood_risk")
    print(f"  Returned Risk    : {llm_sim_result['risk'].upper()}")

    # 3. Graceful handling of invalid coordinates
    print("\n[3] Safety Check: Invalid Coordinates (lat=999, lon=0)")
    print("-" * 45)
    safety_result = get_flood_risk(999, 0)
    print(f"  Returned Risk    : {safety_result['risk']}")
    print(f"  Captured Error   : {safety_result['error']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
