# coding=utf-8
import json

from common import constant
from common import errcode
from common.mylog import logger
from dao.question.question_dao import QuestionDao
from dao.question.user_question_map_dao import UserQuestionMapDao
from handlers.base.base_handler import BaseHandler
from myutil import tools


class GetQuestionListByCategoryHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "category_id": None,
            "page_num": None,
            "page_size": None,
            "common_param": None,
        }
        need_para = (
            "category_id",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetQuestionListByCategoryHandler, self).__init__(expect_request_para, need_para)

    def _parse_and_check_parameters(self):
        """
        参数校验
        :return:
        """
        if not super(GetQuestionListByCategoryHandler, self)._parse_and_check_parameters():
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "param error!"
            return False

        self.category_id = tools.str_to_int(self.para_map["category_id"], 0)
        if self.category_id <= 0:
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "category param error!"
            return False

        self.page_num = tools.str_to_int(self.para_map["page_num"], 0)
        if self.page_num <= 0:
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "page_num param error!"
            return False

        self.page_size = tools.str_to_int(self.para_map["page_size"], 0)
        if self.page_size <= 0:
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "page_size param error!"
            return False

        if self.user_type == constant.USER_SOURCE_LOGIN_USER:
            self.uid = self.rid
        else:
            self.uid = self.tid

        return True

    def _process_imp(self):
        question_list = QuestionDao.get_by_category(self.category_id, self.page_num, self.page_size)

        # 将答案json规范
        for question_item in question_list:
            try:
                question_item["answer"] = json.loads(question_item["answer"])
            except Exception, ex:
                logger.error(ex, exc_info=1)
                question_item["answer"] = []
                continue

            # 用户获取的答案记录在案
            UserQuestionMapDao.insert(self.user_type, self.uid, question_item["id"])

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "questions": question_list
        }
        return
