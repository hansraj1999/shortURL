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

NON_REQ_DATA = ["thread", "args", "name", "threadName", "processName",
                "process", "relativeCreated", "msecs", "stack_info", "exc_text"]
resource = Resource(attributes={
    "service.name": "short-link-service",
    "environment": "dev",
    "host": socket.gethostname()
})
logger = logging.getLogger(__name__)
trace.set_tracer_provider(TracerProvider(resource=resource))

# span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317"))
# trace.get_tracer_provider().add_span_processor(
#     span_processor
# )


class LogFormatter(logging.Formatter):
    """LogFormatter."""
    resource_attributes = {
        "service.name": "short-link-service",
        "host": socket.gethostname(),
    }

    def __init__(self, **kwargs):
        super().__init__()

    def format(self, record):
        """format."""
        span_context = get_current_span().get_span_context()
        trace_id, span_id, trace_flags = span_context.trace_id, span_context.span_id, span_context.trace_flags
        trace_id = format_trace_id(trace_id if trace_id else 0)
        span_id = format_span_id(span_id if span_id else 0)

        body = record.getMessage()
        raw_attributes = vars(record)
        if type(record.msg) == dict:
            raw_attributes.update(record.msg)
        exc_info = raw_attributes.get("exc_info")
        custom_attributes = raw_attributes
        for non_req_data in NON_REQ_DATA:
            if non_req_data in custom_attributes:
                del custom_attributes[non_req_data]
        record_dict = {
            "body": f"{body}",
            "severity_number": record.levelno,
            "severity_text": record.levelname,
            "attributes": custom_attributes,
            "exc_info": exc_info,
            "timestamp": datetime.datetime.utcfromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "trace_id": trace_id,
            "span_id": span_id,
            "trace_flags": trace_flags,
            "resource": {
                # "pathname": record.pathname,
                "lineno": record.lineno,
                **self.resource_attributes
            }
        }
        try:
            message_string = ujson.dumps(
                record_dict)
        except Exception as e:
            logger.exception(e)
            message_string = json.dumps(
                record_dict, indent=None, default=str)
        return message_string
