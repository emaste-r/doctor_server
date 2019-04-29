# coding=utf-8
from logging.config import dictConfig

from mycelery.config.log import LOG_CONF
from myutil.sms.JHSJ_SMSClient import jhsj_client

dictConfig(LOG_CONF)

from mycelery.celery_task import app


@app.task
def send_login_sms(phone, code):
    """
    :param phone:
    :param code:
    :return:
    """
    print "sms: login, phone%s,code=%s" % (phone, code)
    jhsj_client.send_login(phone, "#code#=%s" % code)


@app.task
def send_register_sms(phone, code):
    """
    :param phone:
    :param code:
    :return:
    """
    print "sms: register, phone%s,code=%s" % (phone, code)
    jhsj_client.send_register(phone, "#code#=%s" % code)


@app.task
def send_change_phone_sms(phone, code):
    """
    :param phone:
    :param code:
    :return:
    """
    print "sms: change_phone, phone%s,code=%s" % (phone, code)
    jhsj_client.send_change_phone(phone, "#code#=%s" % code)


@app.task
def send_forget_pass_sms(phone, code):
    """
    :param phone:
    :param code:
    :return:
    """
    print "sms: forget_pass, phone%s,code=%s" % (phone, code)
    jhsj_client.send_forget_pass(phone, "#code#=%s" % code)
