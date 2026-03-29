"""HiveBox API Application"""

from datetime import datetime, timedelta, timezone

# import datetime for handling date and time operations
# import timedelta for handling time differences
import requests
from pyctuator.pyctuator import Pyctuator
from flask import Flask


# _____________________________data declaration _______________________

app = Flask(__name__)
URL_ALL_BOXES = "https://api.opensensemap.org/boxes"
params = {
    "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "phenomenon": "temperature",
}
e = Exception("Failed to retrieve data")
lesshour = datetime.now(timezone.utc) - timedelta(hours=1)
__version__ = "0.0.1"
pyctuator = Pyctuator(
    app= app,
    app_name="HiveBox API",
    app_description="API for retrieving and processing temperature data from HiveBox sensors",
    app_url="http://localhost:5000",
    pyctuator_endpoint_url="http://localhost:5000/instances",
    registration_url="http://localhost:5000/instances",
)


# ______________________api declaration __________________________
@app.route("/version")
def getversion():
    """Version of the application"""
    return {"version": __version__}


@app.route("/temperature")
def get_temperature_1h():
    """Avergae Temperature in last  hour"""
    current_temperature = avg_temperature()
    return {"Average Temperature": current_temperature}


@app.route("/health")
def health_check():
    '''Health check endpoint'''
    return {"status": "healthy"}

# _______________________________function declaration __________________________
def getallboxesapi():
    """get all  data of boxes"""
    try:
        req = requests.get(URL_ALL_BOXES, params=params, timeout=10)
        response = req.json()
        print(type(response))
        print("is type")
        return response
    except requests.exceptions.HTTPError as ex:
        print("HTTP error occurred: ", ex)
        return ex
    except requests.exceptions.ConnectionError as ex:
        print("Connection error occurred: ", ex)
        return ex
    except requests.exceptions.Timeout as ex:
        print("Request timed out: ", ex)
        return ex
    except requests.exceptions.RequestException as ex:
        print(" failed  to  retreive  data \n")
        return ex


def datatemperaturevalidator():
    """get  temperature from  boxes"""
    data = []
    response = getallboxesapi()
    if not response:
        return data
    for box in response:
        sensors = box.get("sensors", [])
        for sensor in sensors:
            if sensor.get("title", "").lower() in ["temperature", "temperatur"]:
                measurement = sensor.get("lastMeasurement")
                if measurement and "value" in measurement:
                    ts = datetime.fromisoformat(
                        measurement["createdAt"].replace("Z", "+00:00")
                    )
                    if ts >= lesshour:
                        data.append(
                            {
                                "box": box["name"],
                                "temperature": float(measurement["value"]),
                                "time": ts.isoformat(),
                            }
                        )
    print("all  temperture  : ")
    for f in data:
        print(f)
    return data


def avg_temperature():
    """Calculate averge  temp  per Box"""
    grouped = {}
    response = datatemperaturevalidator()
    for i in response:
        box = i["box"]
        temp = i["temperature"]
        if box not in grouped:
            grouped[box] = []
        grouped[box].append(temp)
        data = []
        for b, t in grouped.items():
            avg = sum(t) / len(t)
            print(f"data for {b}")
            data.append({"box": b, "avg_temprature": avg})
            print(f"{data} \n")
    print("average temperature for each box")
    for b in data:
        print(b)

    return data


def return_version():
    """print this  is the version  app"""
    print(f"v {__version__}")
    return __version__

# ______________________main app _________________________

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
