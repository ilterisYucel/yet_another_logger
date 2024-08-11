from pydantic import BaseModel, ConfigDict, FilePath, field_serializer

from .enums import LoggerTypes, LogLevels

__all__ = [
    "BaseConfiguration",
    "StreamLoggerConfiguration",
    "FileLoggerConfiguration",
    "RotatingFileLoggerConfiguration",
]


class BaseConfiguration(BaseModel):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)

    name: str = "Root"
    type: LoggerTypes = LoggerTypes.STREAM
    format: str | None = None
    log_level: LogLevels = LogLevels.DEBUG
    date_format: str | None = None


class StreamLoggerConfiguration(BaseConfiguration):
    pass


class FileLoggerConfiguration(BaseConfiguration):
    file_path: FilePath

    @field_serializer("file_path")
    def serialize_dt(self, file_path) -> str:
        return str(object=file_path)


class RotatingFileLoggerConfiguration(FileLoggerConfiguration):
    max_bytes: int = 10000
    backup_count: int = 3
