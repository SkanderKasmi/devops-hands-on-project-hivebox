# routes.py
"""Define API routes for the HiveBox application"""

from flask import Blueprint, jsonify, request, render_template, current_app, Response
from HiveBox.modules import temperature_status
from HiveBox.configs.promtheus_metrics import (
    temperature_requests_total,
    collect_metrics,
    handler,
    REQUEST_BY_REGION_COUNTER,
)
from prometheus_client import CONTENT_TYPE_LATEST

# Create a blueprint
api = Blueprint("api", __name__, url_prefix="/api/v1")
actuator_api = Blueprint("actuator_api", __name__, url_prefix="/instances")


@api.before_request
def before_request():
    """Log incoming requests"""
    ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)
    try:
        details = handler.getDetails(ip_addr)
        region = details.region
    except Exception as e:
        print(f"Error fetching IP details: {e}")
        region = "unknown"
    REQUEST_BY_REGION_COUNTER.labels(endpoint=request.path, region=region).inc()

    print(f"Received request: {request.method} {request.path}")


@api.after_request
def after_request(response):
    """Log outgoing responses"""
    print(f"Responding with status: {response.status}")
    return response


@api.errorhandler(404)
def not_found(_error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


@api.errorhandler(500)
def internal_error(_error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


@api.errorhandler(Exception)
def handle_exception(error):
    """Handle unexpected exceptions"""
    print(f"Unexpected error: {error}")
    return jsonify({"error": "An unexpected error occurred"}), 500


@api.route("/")
def index():
    """API index endpoint"""
    endpoints = []
    for i in current_app.url_map.iter_rules():
        if i.rule.startswith(api.url_prefix):
            endpoints.append(
                {"endpoint": i.endpoint, "methods": list(i.methods), "rule": i.rule}
            )

    return render_template("index.html", endpoints=endpoints)


# Version endpoint
@api.route("/version", methods=["GET"])
def version():
    """Return the version of the application"""
    return jsonify({"version": "0.1.0"})


# Temperature endpoint
@api.route("/temperature", methods=["GET"])
def temperature():
    """Return average temperature data from HiveBox sensors"""
    temperature_requests_total.inc()
    data = temperature_status()
    return jsonify(data)


# Health check
@api.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})


@api.route("/metrics", methods=["GET"])
def metrics():
    """Metrics endpoint"""
    res = Response(collect_metrics(), mimetype=CONTENT_TYPE_LATEST)
    print (res)
    return res
