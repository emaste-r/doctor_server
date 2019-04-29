# coding=utf-8
import random

from common import constant
from common import errcode
from dao.sms.sms_dao import SmsDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler
from mycelery.tasks import send_sms_task


class SmsForgetPassHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "phone": None,
            "common_param": None,
        }
        need_para = (
            "phone",
            "common_param",
        )
        super(SmsForgetPassHandler, self).__init__(expect_request_para, need_para)

        # 特殊控制，此接口sid可以为空
        self.sid_control_level = constant.SID_CAN_BE_NULL

    def _process_imp(self):
        # 用户必须存在
        user = UserDao.get_by_phone(self.para_map["phone"])
        if not user:
            self.ret_code = errcode.SEND_SMS_ERROR
            self.ret_msg = 'user not exist'
            return

        # 保存到数据库
        code = random.randint(1000, 9999)
        SmsDao.insert(self.para_map["phone"], code, constant.SMS_FORGET_PASS)

        # 发送短信
        send_sms_task.send_forget_pass_sms.delay(self.para_map["phone"], code)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'

        return
