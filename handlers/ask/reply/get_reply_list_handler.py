# coding=utf-8
from common import errcode
from dao.ask.answer_reply_img_dao import AskAnswerReplyImgDao
from dao.ask.ask_answer_reply_dao import AskAnswerReplyDao
from dao.ask.ask_answer_reply_like_dao import AskAnswerReplyLikeDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class GetReplyListHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "answer_id": None,
            "page_num": None,
            "page_size": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "answer_id",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetReplyListHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        reply_list = AskAnswerReplyDao.get_by_page(self.para_map["ask_id"], self.para_map["answer_id"],
                                                   self.para_map["page_num"], self.para_map["page_size"])

        for reply in reply_list:
            # 回复用户
            user = UserDao.get_by_id(reply["user_id"])
            reply["user"] = user

            # 回复的图片
            ask_imgs = AskAnswerReplyImgDao.get_by_reply(reply["answer_id"], reply["id"])
            reply["imgs"] = ask_imgs

            # 该用户是否对这些回答点过赞
            if AskAnswerReplyLikeDao.get_by_answer_reply_user(reply["answer_id"], reply["id"], reply["user_id"]):
                reply["is_like"] = 1
            else:
                reply["is_like"] = 0

            # 美化返回值
            reply["reply_id"] = reply["id"]
            del reply["id"]

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "reply_list": reply_list
        }
        return
