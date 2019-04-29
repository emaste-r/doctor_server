# coding=utf-8
from common import constant
from common import errcode
from dao.sms.sms_dao import SmsDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler
from myutil.token import app_token_util


class PhoneRegisterHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "phone": None,
            "code": None,
            "common_param": None,
        }
        need_para = (
            "phone",
            "code",
            "common_param",
        )
        super(PhoneRegisterHandler, self).__init__(expect_request_para, need_para)

        # 特殊控制，此接口sid可以为空
        self.sid_control_level = constant.SID_CAN_BE_NULL

    def _process_imp(self):

        # 手机号已经存在
        user = UserDao.get_by_phone(self.para_map["phone"])
        if user:
            self.ret_code = errcode.USER_ALREADY_EXIST
            self.ret_msg = 'phone is already exist'
            return

        # 检查短信验证码
        sms = SmsDao.get_by_phone_and_code(self.para_map["phone"], self.para_map["code"])
        if not sms:
            self.ret_code = errcode.SEND_SMS_ERROR
            self.ret_msg = 'code is error'
            return

        phone = self.para_map["phone"]
        cuid = self.common_param["cuid"]
        device_type = self.common_param["device_type"]
        device_os = self.common_param["device_os"]
        app_version = self.common_param["app_version"]
        channel = self.common_param["channel"]

        user_id = UserDao.insert({
            "phone": phone,
            "cuid": cuid,
            "device_type": device_type,
            "device_os": device_os,
            "app_version": app_version,
            "channel": channel
        }
        )
        user = UserDao.get_by_id(user_id)

        # 生成新的sid，初次注册默认是用户，要上传资料审核才能成为医生
        new_sid = app_token_util.make_sid(constant.USER_SOURCE_LOGIN_USER, user_id, device_type, cuid)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "user": user,
            "sid": new_sid,
        }

        return
