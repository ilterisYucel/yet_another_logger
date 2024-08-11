from enum import Enum

__all__: list[str] = [
    "LoggerTypes",
    "LogLevels",
    "ErrorMessages",
]


class LoggerTypes(Enum):
    STREAM: str = "STREAM"
    FILE: str = "FILE"
    ROTATING_FILE: str = "ROTATING_FILE"


class LogLevels(Enum):
    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    WARNING: str = "WARNING"
    ERROR: str = "ERROR"
    CRITICAL: str = "CRITICAL"


class ErrorMessages(Enum):
    NOT_CONFIGURATED: str = "Logger is not yet configurated."
    FACTORY_NOT_CONFIGURED: str = "Factor is not configured."
    INVALID_CONFIGURATION: str = "Configuration is invalid."
    INTERNAL_ERROR: str = "Internal error on library."
    CONFIGURATION_FAILED: str = "Configuration is failed."
    INVALID_CONFIGURATION_FILE: str = "Invalid configuration file."
