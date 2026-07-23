import sys
from loguru import logger
from app.core.config import settings


def setup_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )
    logger.add(
        "logs/jobfinder_{time:YYYY-MM-DD}.log",
        level="WARNING",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        format="{time} | {level: <8} | {name}:{function}:{line} | {message}",
    )
