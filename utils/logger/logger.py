import logging
from datetime import datetime
from utils.elastic.elastic_service import ElasticConn
from utils.logger.config import INDEX_LOG


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name="teleNews", index=INDEX_LOG, level=logging.DEBUG):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            es = ElasticConn().get_es()

            class ESHandler(logging.Handler):
                def emit(self, record):
                    #logger example: logger.info('sent event', extra={'subject': 'auth', 'user_id': 123})  *The extra is optional*, The key will be the field name and the value will be the value.
                    try:
                        document={
                            "timestamp": datetime.utcnow().isoformat(),

                            "level": record.levelname,
                            "logger": record.name,
                            "message": record.getMessage()

                        }
                        for key, value in record.__dict__.items():
                            if key not in (
                                "name",
                                "msg",
                                "args",
                                "levelname",
                                "levelno",
                                "pathname",
                                "filename",
                                "module",
                                "exc_info",
                                "exc_text",
                                "stack_info",
                                "lineno",
                                "funcName",
                                "created",
                                "msecs",
                                "relativeCreated",
                                "thread",
                                "threadName",
                                "processName",
                                "process",
                            ):
                                document[key] = value
                        es.index(index=index, document=document)
                    except Exception as e:
                        print(f"ES log failed: {e}")

            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger
