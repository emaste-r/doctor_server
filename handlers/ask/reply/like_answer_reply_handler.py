# coding=utf-8
from common import errcode
from dao.ask.ask_answer_reply_dao import AskAnswerReplyDao
from dao.ask.ask_answer_reply_like_dao import AskAnswerReplyLikeDao
from handlers.base.base_handler import BaseHandler


class LikeAnswerReplyHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "answer_id": None,
            "reply_id": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "answer_id",
            "reply_id",
            "common_param",
        )
        super(LikeAnswerReplyHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # xxx 给 xxx答案的xxx回复点赞
        ret = AskAnswerReplyLikeDao.insert(self.para_map["ask_id"], self.para_map["answer_id"],
                                           self.para_map["reply_id"], self.uid)

        # 答案点赞数 + 1
        if ret:
            AskAnswerReplyDao.update({
                "id": self.para_map["reply_id"],
                "like_num": (1, True),
            })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        return
