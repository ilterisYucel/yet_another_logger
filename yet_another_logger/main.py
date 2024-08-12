from yet_another_logger.yet_another_logger import YetAnotherLogger

conf = {"type": "STREAM", "name": "sdasdad"}
conf1 = {"type": "FILE", "name": "sdasdad", "file_path": "../../log.txt"}
lola: list[dict[str, str]] = [conf, conf1]

logger: YetAnotherLogger = YetAnotherLogger.from_dict(lola)
logger.configure()
logger.warning("Test")
