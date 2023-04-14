import logging

# Create logger with a specific name
logger = logging.getLogger("wifix_db_logger")

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create and configure a log handler
handler = logging.StreamHandler()  # Log to console
handler.setLevel(logging.DEBUG)  # Set handler logging level
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)  # Set log message format
handler.setFormatter(formatter)
logger.addHandler(handler)
