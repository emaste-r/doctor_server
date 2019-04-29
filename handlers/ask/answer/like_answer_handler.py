# coding=utf-8
from common import errcode
from dao.ask.ask_answer_dao import AskAnswerDao
from dao.ask.ask_answer_like_dao import AskAnswerLikeDao
from handlers.base.base_handler import BaseHandler


class LikeAnswerHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "answer_id": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "answer_id",
            "common_param",
        )
        super(LikeAnswerHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # xxx 给 xxx答案点赞
        ret = AskAnswerLikeDao.insert(self.para_map["ask_id"], self.para_map["answer_id"], self.uid)

        # 答案点赞数 + 1
        if ret:
            AskAnswerDao.update({
                "id": self.para_map["answer_id"],
                "like_num": (1, True),
            })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        return
