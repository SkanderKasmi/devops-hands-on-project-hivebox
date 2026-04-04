# utils.py
"""Utility functions for HiveBox application"""
from datetime import datetime


def parse_iso_timestamp(ts):
    """Convert ISO 8601 timestamp to datetime object in UTC"""
    if ts is None:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def format_box_temperature(box, temp):
    """Pretty-print box temperatures"""
    name = box.get("name", "Unknown Box")
    return {"Box": name, " Avg Temp": temp}
