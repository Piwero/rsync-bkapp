import logging
from io import StringIO

import pytest
from pydantic import ValidationError

from src.logger import LoggerConfig, setup_logger


def test_logger_config_valid_log_level():
    config = LoggerConfig(log_level="DEBUG")
    assert config.log_level == "DEBUG"


def test_logger_config_invalid_log_level():
    with pytest.raises(ValidationError):
        LoggerConfig(log_level="INVALID_LEVEL")


def test_setup_logger_console_logging():
    config = LoggerConfig(log_level="DEBUG", console_log=True)
    logger = setup_logger(config)

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger.addHandler(handler)

    logger.debug("This is a debug message")

    handler.flush()
    log_contents = log_stream.getvalue()

    assert "This is a debug message" in log_contents
    logger.removeHandler(handler)  # Clean up


def test_setup_logger_file_logging(tmp_path):
    log_file = tmp_path / "test.log"
    config = LoggerConfig(log_level="DEBUG", log_file=str(log_file), console_log=False)
    logger = setup_logger(config)

    logger.debug("This is a debug message written to a file")

    with open(log_file, "r") as f:
        log_contents = f.read()

    assert "This is a debug message written to a file" in log_contents
