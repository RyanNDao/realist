import logging
import sys

class CommonLogger:
    LOGGER = None

    @classmethod
    def setupLogger(cls, level=logging.DEBUG):
        if cls.LOGGER is None:
            logger = logging.getLogger('CommonLogger')
            logger.setLevel(level)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '[ %(asctime)s | PROCESS_ID:%(process)d | %(levelname)s | %(filename)s:%(lineno)d ] -- %(message)s'
            )
            handler.setFormatter(formatter)
            if not logger.handlers:
                logger.addHandler(handler)
            logger.propagate = False
            cls.LOGGER = logger
            cls.LOGGER.warning(f'Logging level has been set to: {logging.getLevelName(level)}')
