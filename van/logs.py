import logging
from logging.config import dictConfig


config = {
    'version': 1,
    'formatters': {
        'f': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        },
    },
    'root': {
        'handlers': ['console'],
        'level': logging.INFO,
    },
    'loggers': {
        'van': {
            'handlers': ['console'],
            'level': logging.DEBUG,
            'propagate': False,
        },
    }
}


def init_logging() -> None:
    """
    Initializes logging configuration using config above.

    Call this at least once when a script/program starts. This is necessary since we're not
    running in Django or some framework that does it for us.
    """
    dictConfig(config)


def get_logger(name: str = None) -> logging.Logger:
    """
    Gets a logger for the name provided.

    :param name: name of the logger
    :return: Logger instance to be used for logging
    """
    return logging.getLogger(name)
