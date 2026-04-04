# temperature.py
"""Module for fetching and processing temperature
data from the OpenSenseMap API"""
from datetime import datetime, timedelta, timezone
import requests

# Example: API base URL
URL_ALL_BOXES = "https://api.opensensemap.org/boxes"


# Fetch all boxes
def get_all_boxes(params=None):
    """Fetch all boxes from the API"""
    if params is None:
        params = {
            "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "phenomenon": "temperature",
        }
    try:
        response = requests.get(URL_ALL_BOXES, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch boxes: {e}")
        return []


# Filter temperature measurements from boxes
def get_recent_temperatures(hours=1):
    """Get recent temperature measurements from the last specified hours"""
    data = []
    less_hour = datetime.now(timezone.utc) - timedelta(hours=hours)
    boxes = get_all_boxes()
    for box in boxes:
        for sensor in box.get("sensors", []):
            if sensor.get("title", "").lower() in ["temperature", "temperatur"]:
                measurement = sensor.get("lastMeasurement")
                if measurement:
                    ts = datetime.fromisoformat(
                        measurement["createdAt"].replace("Z", "+00:00")
                    )
                    if ts >= less_hour:
                        data.append(
                            {
                                "box": box["name"],
                                "temperature": float(measurement["value"]),
                                "time": ts.isoformat(),
                            }
                        )
    return data


# Calculate average temperature per box
def avg_temperature():
    """Calculate average temperature per box"""
    temps = get_recent_temperatures()
    grouped = {}
    for t in temps:
        grouped.setdefault(t["box"], []).append(t["temperature"])
    return [
        {"box": b, "avg_temperature": sum(vals) / len(vals)}
        for b, vals in grouped.items()
    ]


def temperature_status():
    """Determine temperature status based on average temperature"""
    avg_temps = avg_temperature()
    for entry in avg_temps:
        temp = entry["avg_temperature"]
        if temp <= 10:
            entry["status"] = "Too Cold"
        elif temp >= 37:
            entry["status"] = "Too Hot"
        else:
            entry["status"] = "Good"

    return avg_temps
