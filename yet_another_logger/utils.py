from yet_another_logger.enums import LoggerTypes

__all__: list[str] = [
    "validate_logger_type",
]


def validate_logger_type(param: str, logger_type: LoggerTypes) -> bool:
    return param.capitalize() == logger_type
