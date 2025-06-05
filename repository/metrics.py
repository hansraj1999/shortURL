from functools import wraps
import time


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)
from starlette.middleware.base import BaseHTTPMiddleware

import socket
from fastapi import Request

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


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        latency = time.time() - start_time
        print(str(request.url.path), "fiofnoo")
        REQUEST_LATENCY.record(latency, {"endpoint": str(request.url.path)})
        REQUEST_COUNT.add(
            1, {"method": str(request.method), "endpoint": str(request.url.path)}
        )

        return response
