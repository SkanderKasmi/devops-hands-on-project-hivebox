# sensors.py
'''Module for processing sensor data from HiveBox API'''

def filter_sensors(box, titles=None):
    """
    Return sensors in a box matching the given titles.
    titles: list of sensor names (case-insensitive)
    """
    if titles is None:
        titles = ["temperature"]

    return [
        sensor
        for sensor in box.get("sensors", [])
        if sensor.get("title", "").lower() in [t.lower() for t in titles]
    ]


def get_last_measurement(sensor):
    """Return the last measurement of a sensor or None"""
    measurement = sensor.get("lastMeasurement")
    if measurement:
        return measurement.get("value"), measurement.get("createdAt")
    return None, None
