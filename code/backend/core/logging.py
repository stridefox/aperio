"""
/core/logging.py

Implements the logging functionality needed to track the backend's
functioning. Each logger writes to the console and to a rotating log file
in the backend's logs/ folder.
"""

# Importing the necessary modules
from logging.handlers import RotatingFileHandler
from pathlib import Path
import logging

# Folder for the log files. Resolved from this file's location
# (core/ -> backend/logs) so it doesn't depend on where the app is started from.
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

class Logger:
    """
    Creates and configures a named logger for a part of the backend.

    Attributes:
        logger_name (str): The name of the logger. Also used as the log file's
            name (logs/<logger_name>.log).

    Example:
        logger = Logger("users").initialize_logger()
        logger.info("User created")
    """
    logger_name: str

    def __init__(self, name: str):
        """
        Initializes the Logger.

        Args:
            name (str): The name of the logger.
        """
        self.logger_name = name

    @staticmethod
    def create_console_handler(formatter: logging.Formatter, logger: logging.Logger):
        """
        Adds a handler that prints log messages to the console.

        Args:
            formatter (logging.Formatter): The format of each log message.
            logger (logging.Logger): The logger to add the handler to.
        """

        # Creating a console logger (writes to stderr by default)
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.INFO)
        console_logger.setFormatter(formatter)

        # Adding the handler to the logger
        logger.addHandler(console_logger)

    @staticmethod
    def create_rotating_file_handler(formatter: logging.Formatter, logger: logging.Logger):
        """
        Adds a handler that writes log messages to logs/<logger name>.log.

        When the file reaches 5 MB, it is renamed to <name>.log.1 and a new file
        is started. Only the 2 most recent old files are kept, so each logger
        uses at most about 15 MB of disk space.

        Args:
            formatter (logging.Formatter): The format of each log message.
            logger (logging.Logger): The logger to add the handler to.
        """

        # Creating the logs folder if it doesn't exist yet; otherwise
        # RotatingFileHandler raises FileNotFoundError
        LOG_DIR.mkdir(parents = True, exist_ok = True)

        # Creating a rotating file handler
        rotating_file_handler = RotatingFileHandler(
            filename = LOG_DIR / f"{logger.name}.log",
            backupCount = 2,                # Number of old log files to keep
            encoding = "UTF-8",
            maxBytes = 5 * 1024 * 1024      # Rotate the file once it reaches 5 MB
        )

        # Setting the level and the formatter
        rotating_file_handler.setLevel(logging.INFO)
        rotating_file_handler.setFormatter(formatter)

        # Adding the handler to the logger
        logger.addHandler(rotating_file_handler)

    def initialize_logger(self) -> logging.Logger:
        """
        Creates the logger, or returns it if it was already set up.

        Returns:
            logging.Logger: A logger that writes INFO and higher messages to
                the console and to its log file.
        """

        # Initializing the logger
        logger = logging.getLogger(self.logger_name)

        # getLogger returns the same logger for the same name, so only add the
        # handlers once; otherwise every message would be written multiple times.
        if logger.handlers:
            return logger

        # Setting the level of the logger; messages below INFO (e.g. DEBUG)
        # are ignored
        logger.setLevel(logging.INFO)

        # Setting the formatter for the logger,
        # e.g. "2026-11-27 14:05:31 | users | INFO | User created"
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Creating a console handler
        self.create_console_handler(formatter, logger)

        # Creating a rotating file handler
        self.create_rotating_file_handler(formatter, logger)

        # Returning the logger
        return logger
