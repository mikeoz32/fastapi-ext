from typing import TYPE_CHECKING
from loguru import logger
import sys
import json
import logging

if TYPE_CHECKING:
    from loguru import Record

LOG_LEVEL = logging.INFO


def stdout_format(record: "Record") -> str:
    record["extra"]["extra_json"] = json.dumps(record["extra"])
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> - "
        "{extra[extra_json]}"
        "\n{exception}"
    )


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init_logger():
    logger.remove()

    logger.add(sys.stdout, level=LOG_LEVEL, format=stdout_format)

    logging.basicConfig(handlers=[InterceptHandler()], level=LOG_LEVEL, force=True)
    for uvicorn_logger_name in ["uvicorn", "uvicorn.error"]:
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.setLevel(LOG_LEVEL)
        uvicorn_logger.handlers = []
    for uvicorn_logger_name in ["uvicorn.access", "alembic.runtime.migration"]:
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.setLevel(LOG_LEVEL)
        uvicorn_logger.handlers = [InterceptHandler()]


__all__ = ["init_logger", "logger"]
