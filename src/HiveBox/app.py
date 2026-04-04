"""HiveBox API Application"""

from pyctuator.pyctuator import Pyctuator
from flask import Flask
from HiveBox.configs import get_config
from .api import api

__version__ = "0.1.0"


# # ______________________main app _________________________
def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    app.config.from_object(get_config())
    app.register_blueprint(api)
    Pyctuator(
        app=app,
        app_name="HiveBox API",
        app_description="API for retrieving and processing temperature data from HiveBox sensors",
        app_url="http://localhost:5000",
        pyctuator_endpoint_url="/actuator",
        registration_url=None,
        additional_app_info={
            "serviceLinks": {
                "metrics": [
                    "http://xyz/pod/metrics/memory",
                    "http://xyz/pod/metrics/cpu",
                ]
            },
            "podLinks": {
                "metrics": [
                    "http://xyz/pod/metrics/memory",
                    "http://xyz/pod/metrics/cpu",
                ]
            },
        },
    )
    return app
