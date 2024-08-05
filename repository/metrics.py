from functools import wraps
import time


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

import socket

from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource(attributes={SERVICE_NAME: socket.gethostname()})
otlp_exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(otlp_exporter)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

meter = metrics.get_meter(__name__)


REQUEST_COUNT = meter.create_counter(
    "http_requests_total", description="Total number of HTTP requests"
)
REQUEST_LATENCY = meter.create_histogram(
    "http_request_duration_seconds", description="Histogram of HTTP request latencies"
)


def measure_latency(endpoint_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Start timing
            start_time = time.time()
            # Call the endpoint function
            response = await func(*args, **kwargs)
            # End timing and record duration
            duration = time.time() - start_time
            REQUEST_LATENCY.record(duration, {"endpoint": endpoint_name})
            return response

        return wrapper

    return decorator
