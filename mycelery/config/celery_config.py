# coding=utf-8
from common import config

BROKER_URL = config.CELERY_REDIS_BROKER_URL
CELERY_RESULT_BACKEND = config.CELERY_REDIS_BACKEND_URL
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERYD_CONCURRENCY = 3  # worker数量
CELERYD_HIJACK_ROOT_LOGGER = False  # 如果True则会移除所有的root logger下的handler。

CELERY_ACKS_LATE = False
CELERYD_PREFETCH_MULTIPLIER = 1  # 每一个worker服务的task数量

# 定时任务
CELERYBEAT_SCHEDULE = {
    # 'foli_push_everyday': {
    #     'task': 'mycelery.task.CeleryFoliPush.foli_auto_push',
    #     'schedule': crontab(hour=9, minute=0),
    #     'args': ()
    # },
    # 'huixiang_push_everymin': {
    #     'task': 'mycelery.task.CeleryHuixiangPush.huixiang_push',
    #     'schedule': crontab(minute='*/1'),
    #     'args': ()
    # },
}

# 队列
CELERY_QUEUES = {
    "quick_queue": {
        "exchange": "quick_queue",
        "binding_key": "quick_queue"},
    "slow_queue": {
        "exchange": "slow_queue",
        "binding_key": "slow_queue",
    },
}

# 路由
CELERY_ROUTES = {
    'mycelery.tasks.send_sms_task.send_login_sms': {'queue': "quick_queue"},
    'mycelery.tasks.send_sms_task.send_register_sms': {'queue': "quick_queue"},
    'mycelery.tasks.send_sms_task.send_change_phone_sms': {'queue': "quick_queue"},
    'mycelery.tasks.send_sms_task.send_forget_pass_sms': {'queue': "quick_queue"},
}

# 配置IMPORT，才能把task注册在celery中
CELERY_IMPORTS = ("mycelery.tasks.send_sms_task",
                  )

"""
通过 celery worker -A celery_task  --loglevel=DEBUG可以看看注册的task：
[tasks]
  . celery.backend_cleanup
  . celery.chain
  . celery.chord
  . celery.chord_unlock
  . celery.chunks
  . celery.group
  . celery.map
  . celery.starmap
  . mycelery.celery_task.custom_message_push
  . mycelery.celery_task.get_rongcloud_token
  . mycelery.task.CeleryFoliPush.foli_auto_push
  . mycelery.task.CeleryFoliPush.foli_manual_push
  . mycelery.task.CeleryHuixiangPush.huixiang_push
  . mycelery.task.CeleryManualPush.manual_push
  . mycelery.task.CeleryOrderFeedbackPush.order_feedback_push
  . mycelery.task.CelerySaveAppRequest.request_save_to_db
  . mycelery.task.CelerySaveThirdUserAvatar.save_thirduser_avatar
  . mycelery.task.ctool.CeleryQiniu.qiniu_delete
  . mycelery.task.ctool.CeleryQiniu.qiniu_upload_file
  . mycelery.task.ctool.CelerySmsClient.send_code_sms
  . mycelery.task.ctool.CelerySmsClient.send_feedback_sms

"""
