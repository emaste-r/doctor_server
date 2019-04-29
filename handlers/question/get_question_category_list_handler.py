# coding=utf-8
from common import errcode
from dao.question.question_category_dao import QuestionCategoryDao
from handlers.base.base_handler import BaseHandler


class GetQuestionCategoryListHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "common_param": {},
        }
        need_para = (
            "common_param",
        )
        super(GetQuestionCategoryListHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        category_list = QuestionCategoryDao.get_all()

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "category_list": category_list
        }
        return
