from functools import wraps
from flask import request, g
from ..logging.trace import set_trace_id, get_trace_id
import logging


def trace_requests(app):
    """Add trace ID to all requests.

    This middleware:
    1. Generates or propagates trace IDs across requests
    2. Adds trace ID to response headers
    """

    @app.before_request
    def before_request():
        trace_id = request.headers.get("X-Trace-ID") or None
        g.trace_id = set_trace_id(trace_id)

    @app.after_request
    def after_request(response):
        response.headers["X-Trace-ID"] = g.trace_id
        return response

    # Add trace ID to log records
    logging.getLogger("werkzeug").addFilter(
        lambda record: setattr(record, "trace_id", get_trace_id()) or True
    )
