# coding=utf-8
from common import errcode
from dao.sms.sms_dao import SmsDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler
from myutil.token import app_token_util


class ChangePhoneHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "uid": None,
            "phone": None,
            "code": None,
            "common_param": None,
        }
        need_para = (
            "uid",
            "phone",
            "code",
            "common_param",
        )
        super(ChangePhoneHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # 已经有用户使用该手机，不能被绑定
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
        uid = self.para_map["uid"]
        cuid = self.common_param["cuid"]
        device_type = self.common_param["device_type"]

        UserDao.update({
            "phone": phone,
            "id": uid,
        }
        )
        user_info = UserDao.get_profile_by_phone(phone)

        # 生成新的sid
        new_sid = app_token_util.make_sid(user["source"], uid, device_type, cuid)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "user": user_info,
            "sid": new_sid,
        }

        return
