# todo_app/infrastructure/web/middleware.py
def trace_requests(app):
    """Add trace ID to all requests."""

    @app.before_request
    def before_request():
        trace_id = request.headers.get("X-Trace-ID") or None
        g.trace_id = set_trace_id(trace_id)

    @app.after_request
    def after_request(response):
        response.headers["X-Trace-ID"] = g.trace_id
        return response
