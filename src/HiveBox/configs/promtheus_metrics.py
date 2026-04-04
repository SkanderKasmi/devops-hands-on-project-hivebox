from prometheus_client import (
    Gauge,
    Counter,
    generate_latest,
    Histogram,
)
import psutil
import time
import os
import ipinfo

handler = ipinfo.getHandler("143d90fcb1955c")

process = psutil.Process(os.getpid())
# Create Prometheus metrics
memory_usage_gauge = Gauge("hivebox_memory_usage_bytes", "Memory usage in bytes")
cpu_usage_gauge = Gauge("hivebox_cpu_usage_percent", "CPU usage in percent")
disk_usage_gauge = Gauge("hivebox_disk_usage_percent", "Disk usage in percent")
request_latency_histogram = Histogram(
    "hivebox_request_latency_seconds", "Request latency in seconds"
)
temperature_requests_total = Counter(
    "hivebox_temperature_requests_total", "Total number of temperature requests"
)
thread_count_gauge = Gauge(
    "hivebox_thread_count", "Number of threads in the application"
)
INBOUND_REQUESTS_COUNTER = Counter(
    "hivebox_inbound_requests_total", "Total number of inbound requests"
)
OUTBOUND_REQUESTS_COUNTER = Counter(
    "hivebox_outbound_requests_total", "Total number of outbound requests"
)
error_rate_counter = Counter("hivebox_error_rate_total", "Total number of errors")
API_RESPONSE_TIME_HISTOGRAM = Histogram(
    "hivebox_api_response_time_seconds", "API response time in seconds"
)
API_USAGE_GROWTH_COUNTER = Counter(
    "hivebox_api_usage_growth_total", "Total growth in API usage over time"
)
REQUEST_BY_REGION_COUNTER = Counter(
    "api_requests_by_region_total",
    "Total API requests by region",
    ["endpoint", "region"],
)


def collect_metrics():
    """Collect system metrics and update Prometheus gauges"""
    memory_usage_gauge.set(process.memory_info().rss)
    cpu_usage_gauge.set(process.cpu_percent(interval=1))
    disk_usage_gauge.set(psutil.disk_usage("/").percent)
    request_latency_histogram.observe(0.1)  # Simulate request latency
    temperature_requests_total.inc()  # Increment the counter for temperature requests
    thread_count_gauge.set(process.num_threads())
    INBOUND_REQUESTS_COUNTER.inc()  # Increment the counter for inbound requests
    OUTBOUND_REQUESTS_COUNTER.inc()  # Increment the counter for outbound requests
    error_rate_counter.inc()  # Increment the counter for errors
    API_RESPONSE_TIME_HISTOGRAM.observe(0.2)  # Simulate API response time
    API_USAGE_GROWTH_COUNTER.inc()  # Increment the counter for API usage growth
    REQUEST_BY_REGION_COUNTER.labels(endpoint="temperature", region="us-west").inc()
    return generate_latest()
