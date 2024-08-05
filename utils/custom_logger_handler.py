import logging
import ujson
import json
import datetime
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation import asgi

from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import (
    format_span_id,
    format_trace_id,
    get_current_span
)
import socket

resource = Resource(attributes={
    "service.name": "short-link-service",
    "environment": "dev",
    "host": socket.gethostname()
})
logger = logging.getLogger(__name__)
trace.set_tracer_provider(TracerProvider(resource=resource))



class LogFormatter(logging.Formatter):
    def format(self, record):
        span_context = get_current_span().get_span_context()
        trace_id = format_trace_id(span_context.trace_id if span_context.trace_id else 0)
        span_id = format_span_id(span_context.span_id if span_context.span_id else 0)
        record.trace_id = trace_id
        record.span_id = span_id
        record.trace_flags = span_context.trace_flags if span_context.trace_flags else 0
        record.service_name = "short-link-service"
        record.host = socket.gethostname()
        return super().format(record)
