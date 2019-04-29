# coding=utf-8
from common import errcode
from dao.ask.answer_img_dao import AskAnswerImgDao
from dao.ask.ask_answer_dao import AskAnswerDao
from handlers.base.base_handler import BaseHandler


class AnswerAskHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "content": None,
            "img_urls": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "content",
            "img_urls",
            "common_param",
        )
        super(AnswerAskHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # 插入答案
        answer_id = AskAnswerDao.insert({
            "user_id": self.uid,
            "ask_id": self.para_map["ask_id"],
            "content": self.para_map["content"],
        })

        # 插入答案的图片
        for img_url in self.para_map["img_urls"]:
            AskAnswerImgDao.insert({
                "ask_id": self.para_map["ask_id"],
                "answer_id": answer_id,
                "img_url": img_url
            })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "answer_id": answer_id
        }
        return
