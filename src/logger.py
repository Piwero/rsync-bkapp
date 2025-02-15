import logging
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator


class LoggerConfig(BaseModel):
    log_level: str = Field(default="INFO", description="Logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s",
                            description="Log message format")
    log_file: Optional[str] = Field(default=None, description="Path to the log file (if logging to a file)")
    console_log: bool = Field(default=True, description="Whether to log to the console")

    @model_validator(mode='before')
    @classmethod
    def validate_log_level(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        log_level = values.get("log_level")
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_levels:
            raise ValueError(f"Invalid log level: {log_level}. Must be one of {valid_levels}")
        return values


def setup_logger(config: LoggerConfig) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(config.log_level)
    formatter = logging.Formatter(config.log_format)
    if config.console_log:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if config.log_file:
        file_handler = logging.FileHandler(config.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


logger_config = LoggerConfig(
    log_level="INFO",
    log_file="app.log",
    console_log=True
)

logger = setup_logger(logger_config)
