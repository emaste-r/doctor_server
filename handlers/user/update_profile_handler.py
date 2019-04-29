# coding=utf-8
from common import errcode
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class UpdateProfileHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "uid": None,
            "sex": None,
            "avatar": None,
            "user_name": None,
            "common_param": None,
        }
        need_para = (
            "uid",
            "sex",
            "avatar",
            "user_name",
            "common_param",
        )
        super(UpdateProfileHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        profile_dic = {
            "id": self.para_map["uid"],
            "sex": self.para_map["sex"],
            "avatar": self.para_map["avatar"],
            "user_name": self.para_map["user_name"],
        }

        UserDao.update(profile_dic)

        user = UserDao.get_by_id(self.para_map["uid"])

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "user": user
        }
        return
