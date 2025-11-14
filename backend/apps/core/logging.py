import logging


class RequestIDFilter(logging.Filter):
    """
    Ensures every log record has a request_id attribute so formatters using
    %(request_id)s do not crash. The middleware will normally attach a request_id
    to the LoggerAdapter; this filter provides a safe fallback ('-').
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            # Keep '-' as sentinel for missing request id (easy to grep)
            record.request_id = getattr(record, "request_id", "-")
        return True
