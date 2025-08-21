import logging
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AppContext:
    start_time: datetime
    logger: logging.Logger


async def startup() -> AppContext:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(name)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return AppContext(start_time=datetime.now(), logger=logger)


async def shutdown():
    logger = logging.getLogger(__name__)
    logger.info("Crawler kit shutting down...")

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
