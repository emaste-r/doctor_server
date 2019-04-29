# coding=utf-8
from common import constant
from common import errcode
from dao.user.tourist_dao import TouristDao
from handlers.base.base_handler import BaseHandler


class TouristLoginHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "device_model": None,
            "open_push": None,
            "push_token": None,
            "common_param": None,
        }
        need_para = (
            "device_model",
            "push_token",
            "common_param",
        )
        super(TouristLoginHandler, self).__init__(expect_request_para, need_para)

        # 特殊控制，此接口sid可以为空
        self.sid_control_level = constant.SID_CAN_BE_NULL

    def _process_imp(self):
        cuid = self.para_map["common_param"]["cuid"]
        device_type = self.para_map["common_param"]["device_type"]
        device_os = self.para_map["common_param"]["device_os"]
        device_model = self.para_map["device_model"]
        app_version = self.para_map["common_param"]["app_version"]
        channel = self.para_map["common_param"]["channel"]
        open_push = self.para_map["open_push"]
        push_token = self.para_map["push_token"]

        TouristDao.insert(cuid, device_type, device_os, device_model, app_version, channel, open_push, push_token)

        # 获取tid
        tourist_item = TouristDao.get_by_cuid(self.cuid)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "tid": tourist_item["tid"] if tourist_item else 0
        }
        return
