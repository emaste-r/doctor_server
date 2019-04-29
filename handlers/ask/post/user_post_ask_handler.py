# coding=utf-8
from common import constant
from common import errcode
from dao.ask.ask_dao import AskDao
from dao.ask.ask_img_dao import AskImgDao
from handlers.base.base_handler import BaseHandler


class UserPostAskHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "title": None,
            "content": None,
            "img_urls": None,
            "common_param": {},
        }
        need_para = (
            "title",
            "content",
            "img_urls",
            "common_param",
        )
        super(UserPostAskHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # 插入问题
        ask_id = AskDao.insert({
            "author_id": self.uid,
            "user_type": constant.USER_SOURCE_TOURIST,
            "title": self.para_map["title"],
            "content": self.para_map["content"],
        })

        # 插入问题的图片
        for img_url in self.para_map["img_urls"]:
            AskImgDao.insert({
                "ask_id": ask_id,
                "img_url": img_url
            })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "ask_id": ask_id
        }
        return
