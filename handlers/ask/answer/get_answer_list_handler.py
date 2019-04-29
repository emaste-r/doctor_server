# coding=utf-8
from common import errcode
from dao.ask.answer_img_dao import AskAnswerImgDao
from dao.ask.ask_answer_dao import AskAnswerDao
from dao.ask.ask_answer_like_dao import AskAnswerLikeDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class GetAnswerListHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "page_num": None,
            "page_size": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetAnswerListHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        answer_list = AskAnswerDao.get_by_page(self.para_map["ask_id"], self.para_map["page_num"],
                                               self.para_map["page_size"])

        for answer in answer_list:
            # 回答用户
            user = UserDao.get_by_id(answer["user_id"])
            answer["user"] = user

            # 回答的图片
            ask_imgs = AskAnswerImgDao.get_by_answer(answer["id"])
            answer["imgs"] = ask_imgs

            # 该用户是否对这些回答点过赞
            if AskAnswerLikeDao.get_by_answer_user(answer["id"], answer["user_id"]):
                answer["is_like"] = 1
            else:
                answer["is_like"] = 0

            # 美化返回值
            answer["answer_id"] = answer["id"]
            del answer["id"]

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "answer_list": answer_list
        }
        return
