# coding=utf-8
from common import errcode
from dao.ask.answer_reply_img_dao import AskAnswerReplyImgDao
from dao.ask.ask_answer_dao import AskAnswerDao
from dao.ask.ask_answer_reply_dao import AskAnswerReplyDao
from handlers.base.base_handler import BaseHandler


class ReplyAnswerHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "ask_id": None,
            "answer_id": None,
            "reply_to_id": None,
            "content": None,
            "img_urls": None,
            "common_param": {},
        }
        need_para = (
            "ask_id",
            "answer_id",
            "reply_to_id",
            "content",
            "img_urls",
            "common_param",
        )
        super(ReplyAnswerHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        # 插入回复
        reply_id = AskAnswerReplyDao.insert({
            "user_id": self.uid,
            "ask_id": self.para_map["ask_id"],
            "answer_id": self.para_map["answer_id"],
            "reply_to_id": self.para_map["reply_to_id"],  # 默认给0，0表示回复答案， 有值表示回复 别人的回复
            "content": self.para_map["content"],
        })

        # 插入回复的图片
        for img_url in self.para_map["img_urls"]:
            AskAnswerReplyImgDao.insert({
                "ask_id": self.para_map["ask_id"],
                "answer_id": self.para_map["answer_id"],
                "reply_id": reply_id,
                "img_url": img_url
            })

        # 不管是回复答案还是回复别人的回复，答案的reply_num 都加1
        # 因为都是基于它产生的讨论
        # 答案点赞数 + 1
        AskAnswerDao.update({
            "id": self.para_map["answer_id"],
            "reply_num": (1, True),
        })

        # 如果是回复别人的回复，那么别人的回复数+1
        if self.para_map["reply_to_id"] > 0:
            AskAnswerReplyDao.update({
                "id": self.para_map["reply_to_id"],
                "reply_num": (1, True),
            })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "reply_id": reply_id
        }
        return
