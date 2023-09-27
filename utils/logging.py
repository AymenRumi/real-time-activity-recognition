import logging

from colorlog import ColoredFormatter

TASK_LEVEL = 25
logging.addLevelName(TASK_LEVEL, "TASK")

logger = logging.getLogger(__name__)

stream = logging.StreamHandler()

LogFormat = (
    "%(reset)s%(log_color)s%(asctime)s %(levelname)-8s [%(filename)s] %(message)s"
)
stream.setFormatter(
    ColoredFormatter(
        LogFormat,
        log_colors={
            "TASK": "bold_green",
            "INFO": "cyan",
            "SUCCESS": "green",
            "ADDITIONAL INFO": "green",
            "DEBUG": "yellow",
            "WARNING": "red",
            "ERROR": "red",
            "CRITICAL": "black,bg_red",
        },
    )
)


logging.addLevelName(TASK_LEVEL, "TASK")
logging.Logger.task = lambda self, msg, *args, **kwargs: self.log(
    TASK_LEVEL, msg, *args, **kwargs
)

logger.addHandler(stream)
logger.setLevel(logging.DEBUG)
