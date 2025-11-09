# apps/core/logging.py
import logging

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(record, "request_id", "-")
        return True
