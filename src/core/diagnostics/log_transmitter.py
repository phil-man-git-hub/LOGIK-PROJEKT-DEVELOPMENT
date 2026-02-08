import logging
import json
import socket
import datetime

class LogTransmitterHandler(logging.Handler):
    """
    A custom logging handler that broadcasts log records via UDP.
    This allows external processes (like an MCP server or debug listener)
    to 'listen' to the application in real-time without blocking the main thread.
    """

    def __init__(self, host='127.0.0.1', port=54322):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        try:
            # Format the timestamp
            timestamp = datetime.datetime.fromtimestamp(record.created).isoformat()
            
            # Create a structured log message
            log_entry = {
                "timestamp": timestamp,
                "level": record.levelname,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "message": self.format(record)
            }

            # Serialize to JSON and encode
            payload = json.dumps(log_entry).encode('utf-8')
            
            # Fire and forget (UDP)
            self.sock.sendto(payload, (self.host, self.port))
            
        except Exception:
            self.handleError(record)

    def close(self):
        self.sock.close()
        super().close()
