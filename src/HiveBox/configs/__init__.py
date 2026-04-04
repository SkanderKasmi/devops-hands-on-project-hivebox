"""__init__.py
Initialize the HiveBox package
and import all necessary modules and configurations."""

import os
from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from .promtheus_metrics import (
    collect_metrics,
    handler,
    API_USAGE_GROWTH_COUNTER,
    REQUEST_BY_REGION_COUNTER,
    error_rate_counter,
    INBOUND_REQUESTS_COUNTER,
    OUTBOUND_REQUESTS_COUNTER,
    API_RESPONSE_TIME_HISTOGRAM,
    thread_count_gauge,
    temperature_requests_total,
    request_latency_histogram,
    disk_usage_gauge,
    cpu_usage_gauge,
    memory_usage_gauge,
)


def get_config(env=None):
    """Get the appropriate configuration class based on the environment variable"""
    if env is None:
        env = os.getenv("HIVEBOX_ENV", "development").lower()
    if env == "production":
        return ProductionConfig()
    if env == "testing":
        return TestingConfig()
    return DevelopmentConfig()
