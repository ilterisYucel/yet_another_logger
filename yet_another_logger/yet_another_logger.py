from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import toml
from enums import ErrorMessages, LoggerTypes
from errors import BaseYALError
from pydantic import ValidationError
from schemas import (
    BaseConfiguration,
    FileLoggerConfiguration,
    RotatingFileLoggerConfiguration,
    StreamLoggerConfiguration,
)

# from yet_another_logger.utils import validate_logger_type

__all__: list[str] = [
    "StreamLogger",
    "FileLogger",
    "RotatingFileLogger",
    "YetAnotherLogger",
    "LoggerFactory",
]


class BaseLogger(ABC):
    def __init__(self, configuration: BaseConfiguration) -> None:
        self.__configuration: BaseConfiguration = configuration
        self.__logger: logging.Logger = None

    @property
    def logger(self) -> logging.Logger:
        if not self.configured():
            raise BaseYALError(
                message=ErrorMessages.NOT_CONFIGURATED,
                class_name=self.__class__.__name__,
                function_name=self.logger.__name__,
            )
        return self.__logger

    @abstractmethod
    @classmethod
    def validate_configuration(
        cls, configuration: BaseConfiguration | None = None
    ) -> bool:
        pass

    @abstractmethod
    @classmethod
    def from_dict(cls, configuration_dict: dict) -> BaseLogger:
        pass

    @abstractmethod
    def configure(self) -> None:
        pass

    def configured(self) -> bool:
        return self.__logger is not None

    def log(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.log(level=self.__configuration.log_level, msg=message)

    def debug(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.debug(msg=message)

    def info(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.info(msg=message)

    def warning(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.warning(msg=message)

    def error(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.error(msg=message)

    def critical(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        self.__logger.critical(msg=message)


class StreamLogger(BaseLogger):
    def __init__(self, configuration: StreamLoggerConfiguration) -> None:
        super().__init__(configuration=configuration)

    def configure(self) -> None:
        try:
            self.__logger = logging.getLogger(self.__configuration.name)
            logger_format = logging.Formatter(
                self.__configuration.format, datefmt=self.__configuration.date_format
            )
            logger_handler = logging.StreamHandler()
            logger_handler.setLevel(level=self.__configuration.log_level)
            logger_handler.setFormatter(fmt=logger_format)
            self.__logger.addHandler(hdlr=logger_handler)
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.CONFIGURATION_FAILED,
                class_name=self.__class__.__name__,
                function_name=self.logger.__name__,
            ) from exc

    @classmethod
    def from_config(cls, configuration_dict: dict) -> StreamLogger:
        try:
            configuration: StreamLoggerConfiguration = StreamLoggerConfiguration(
                **configuration_dict
            )
            return cls(configuration)
        except ValidationError as exc:
            raise BaseYALError(
                message=ErrorMessages.INVALID_CONFIGURATION,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc


class FileLogger(BaseLogger):
    def __init__(self, configuration: FileLoggerConfiguration) -> None:
        super().__init__(configuration=configuration)

    def configure(self) -> None:
        try:
            self.__logger = logging.getLogger(self.__configuration.name)
            logger_format = logging.Formatter(
                self.__configuration.format, datefmt=self.__configuration.date_format
            )
            logger_handler = logging.FileHandler(
                filename=self.__configuration.file_path
            )
            logger_handler.setLevel(level=self.__configuration.log_level)
            logger_handler.setFormatter(fmt=logger_format)
            self.__logger.addHandler(hdlr=logger_handler)
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.CONFIGURATION_FAILED,
                class_name=self.__class__.__name__,
                function_name=self.logger.__name__,
            ) from exc

    @classmethod
    def from_config(cls, configuration_dict: dict) -> StreamLogger:
        try:
            configuration: FileLoggerConfiguration = FileLoggerConfiguration(
                **configuration_dict
            )
            return cls(configuration)
        except ValidationError as exc:
            raise BaseYALError(
                message=ErrorMessages.INVALID_CONFIGURATION,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc


class RotatingFileLogger(BaseLogger):
    def __init__(self, configuration: RotatingFileLoggerConfiguration) -> None:
        super().__init__(configuration=configuration)

    def configure(self) -> None:
        try:
            self.__logger = logging.getLogger(self.__configuration.name)
            logger_format = logging.Formatter(
                self.__configuration.format, datefmt=self.__configuration.date_format
            )
            logger_handler = RotatingFileHandler(
                filename=self.__configuration.file_path,
                maxBytes=self.__configuration.max_bytes,
                backupCount=self.__configuration.backup_count,
            )
            logger_handler.setLevel(level=self.__configuration.log_level)
            logger_handler.setFormatter(fmt=logger_format)
            self.__logger.addHandler(hdlr=logger_handler)
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.CONFIGURATION_FAILED,
                class_name=self.__class__.__name__,
                function_name=self.logger.__name__,
            ) from exc

    @classmethod
    def from_config(cls, configuration_dict: dict) -> StreamLogger:
        try:
            configuration: FileLoggerConfiguration = FileLoggerConfiguration(
                **configuration_dict
            )
            return cls(configuration)
        except ValidationError as exc:
            raise BaseYALError(
                message=ErrorMessages.INVALID_CONFIGURATION,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.logger.__name__,
            ) from exc


class LoggerFactory:
    def __init__(self, configuration_list: list[BaseConfiguration]) -> None:
        self.__configuration_list: list[BaseConfiguration] = configuration_list
        self.__loggers: list[BaseLogger] = []

    def configured(self) -> bool:
        return len(self.__loggers) > 0

    @property
    def loggers(self) -> list[BaseLogger]:
        if not self.configured():
            raise BaseYALError(
                message=ErrorMessages.FACTORY_NOT_CONFIGURED,
                class_name=self.__class__.__name__,
                function_name=self.loggers.__name__,
            )
        return self.__loggers

    @classmethod
    def from_file(
        cls,
        config_file: str | Path,
    ) -> LoggerFactory:
        try:
            content: dict[str, Any] = toml.load(config_file)
            configuration_list: list[BaseConfiguration] = []
            for v in content.values():
                match v["type"].capitalize():
                    case LoggerTypes.STREAM:
                        configuration_list.append(StreamLoggerConfiguration(**v))
                    case LoggerTypes.FILE:
                        configuration_list.append(FileLoggerConfiguration(**v))
                    case LoggerTypes.ROTATING_FILE:
                        configuration_list.append(RotatingFileLoggerConfiguration(**v))
            return cls(configuration_list)
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INVALID_CONFIGURATION_FILE,
                class_name=cls.__name__,
                function_name=cls.from_file.__name__,
            ) from exc

    @classmethod
    def from_dict(cls, dict_list: list[dict]) -> LoggerFactory:
        try:
            configuration_list: list[BaseConfiguration] = []
            for d in dict_list:
                match d["type"].capitalize():
                    case LoggerTypes.STREAM:
                        configuration_list.append(StreamLoggerConfiguration(**d))
                    case LoggerTypes.FILE:
                        configuration_list.append(FileLoggerConfiguration(**d))
                    case LoggerTypes.ROTATING_FILE:
                        configuration_list.append(RotatingFileLoggerConfiguration(**d))
            return cls(configuration_list)
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INVALID_CONFIGURATION_FILE,
                class_name=cls.__name__,
                function_name=cls.from_dict.__name__,
            ) from exc

    def configure(self) -> None:
        try:
            for conf in self.__configuration_list:
                match conf.type:
                    case LoggerTypes.STREAM:
                        self.__loggers.append(StreamLogger(conf))
                    case LoggerTypes.FILE:
                        self.__loggers.append(FileLogger(conf))
                    case LoggerTypes.ROTATING_FILE:
                        self.__loggers.append(RotatingFileLogger(conf))

            # map(self.__loggers, lambda logger: logger.configure())
        except BaseYALError as exc:
            raise exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=self.__class__.__name__,
                function_name=self.configure.__name__,
            ) from exc


class YetAnotherLogger:
    def __init__(self, logger_factory: LoggerFactory) -> None:
        self.__logger_factory: LoggerFactory = logger_factory
        self.__logger_factory.configure()
        self.__loggers: list[BaseLogger] = self.__logger_factory.loggers

    @classmethod
    def from_dict(cls, dict_list: list[dict]) -> YetAnotherLogger:
        try:
            factory: LoggerFactory = LoggerFactory.from_dict(dict_list=dict_list)
            return cls(factory)
        except BaseYALError as exc:
            raise exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.from_dict.__name__,
            ) from exc

    @classmethod
    def from_file(cls, config_file: str | Path) -> YetAnotherLogger:
        try:
            factory: LoggerFactory = LoggerFactory.from_file(config_file)
            return cls(factory)
        except BaseYALError as exc:
            raise exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.from_file.__name__,
            ) from exc

    @classmethod
    def from_schema(cls, schema_list: list[BaseConfiguration]) -> YetAnotherLogger:
        try:
            factory: LoggerFactory = LoggerFactory(configuration_list=schema_list)
            return cls(factory)
        except BaseYALError as exc:
            raise exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=cls.__name__,
                function_name=cls.from_schema.__name__,
            ) from exc

    def configure(self) -> None:
        try:
            map(self.__loggers, lambda logger: logger.configure())
        except BaseYALError as exc:
            raise exc
        except Exception as exc:
            raise BaseYALError(
                message=ErrorMessages.INTERNAL_ERROR,
                class_name=self.__class__.__name__,
                function_name=self.from_schema.__name__,
            ) from exc

    def configured(self) -> None:
        return all([logger.configured() for logger in self.__loggers])

    def log(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.log(message))

    def debug(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.debug(message))

    def info(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.info(message))

    def warning(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.warning(message))

    def error(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.error(message))

    def critical(self, message: str) -> None:
        if not self.configured():
            raise BaseYALError(message=ErrorMessages.NOT_CONFIGURATED)
        map(self.__loggers, lambda logger: logger.cricital(message))
