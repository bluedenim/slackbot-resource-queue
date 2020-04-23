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


def init_logging():
    dictConfig(config)


def get_logger(name=None):
    return logging.getLogger(name)
