import logging
import datetime

# Create logger with a specific name
logger = logging.getLogger("wifix_db_logger")

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create and configure a console log handler
console_handler = logging.StreamHandler()  # Log to console
console_handler.setLevel(logging.DEBUG)  # Set handler logging level
console_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)  # Set log message format for console
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Get current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create and configure a file log handler with date in filename
log_filename = f"wifix_db_{current_date}.log"
file_handler = logging.FileHandler(log_filename)  # Log to file
file_handler.setLevel(logging.DEBUG)  # Set handler logging level
file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)  # Set log message format for file
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
