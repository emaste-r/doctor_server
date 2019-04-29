# coding=utf-8
import sys

sys.path.append('..')

from celery import Celery, platforms
from celery.utils.log import get_task_logger

from mycelery.config.log import LOG_CONF
from mycelery.config import celery_config

platforms.C_FORCE_ROOT = True  # linux 下要root用户才不报错
app = Celery()
app.config_from_object(celery_config)

# 配置日志
from logging.config import dictConfig

dictConfig(LOG_CONF)
logger = get_task_logger(__name__)
