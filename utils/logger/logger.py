import logging
# from utils.elastic import ...

"""
תכניס אלסטיק
"""
from utils.logger.config import *
from datetime import datetime
import os


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name=NAME,
                   index=INDEX, level=logging.DEBUG):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:

            """
            תכניס פה את המופע של אלסטיק
            """


            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={
                            "timestamp": datetime.utcnow().isoformat(),

                            "level": record.levelname,
                            "logger": record.name,
                            "message": record.getMessage()

                        })
                    except Exception as e:
                        print(f"ES log failed: {e}")

            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger
