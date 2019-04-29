# coding=utf-8
from common import config

LOG_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(filename)s-%(lineno)d [%(levelname)s] %(message)s',
            'datefmt': '%m-%d-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'celery_logger': {
            'level': 'INFO',
            'filters': None,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': config.LOG_CELERY_PATH,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
        },
    },
    'loggers': {
        'celery_task': {
            'handlers': ['celery_logger'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
