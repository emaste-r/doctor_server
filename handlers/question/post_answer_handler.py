# coding=utf-8
from common import constant
from common import errcode
from common.mylog import logger
from dao.question.question_dao import QuestionDao
from dao.question.user_question_map_dao import UserQuestionMapDao
from handlers.base.base_handler import BaseHandler
from myutil import tools


class PostAnswerHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "question_id": None,
            "answer": None,
            "common_param": None,
        }
        need_para = (
            "question_id",
            "answer",
            "common_param",
        )
        super(PostAnswerHandler, self).__init__(expect_request_para, need_para)

    def _parse_and_check_parameters(self):
        if not super(PostAnswerHandler, self)._parse_and_check_parameters():
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "param error!"
            return False

        self.question_id = tools.str_to_int(self.para_map["question_id"])
        if self.question_id <= 0:
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "question param error!"
            return False

        self.answer = tools.str_to_int(self.para_map["answer"])
        if self.answer <= 0:
            self.ret_code = errcode.PARAMETER_ERROR
            self.ret_msg = "answer param error!"
            return False

        return True

    def _process_imp(self):
        question_item = QuestionDao.get_by_id(self.question_id)
        if not question_item:
            logger.error("question not exist: %s" % self.question_id)
            self.ret_code = errcode.QUESTION_NOT_EXIST
            self.ret_msg = "question not exist"
            return

        if self.answer != question_item["correct_answer"]:
            logger.error("question:%s, answer:%s not correct" % (self.question_id, self.answer))

            # 标记题目为错误
            UserQuestionMapDao.update(self.user_type, self.swing_id, self.question_id, self.answer,
                                      constant.QUESTION_RESULT_NOT_CORRECT)

            self.ret_code = errcode.NO_ERROR
            self.ret_msg = 'ok'
            self.ret_data = {
                "answer_result": constant.QUESTION_RESULT_NOT_CORRECT,
                "score": 0
            }
            return
        else:
            logger.error("question:%s, answer:%s correct" % (self.question_id, self.answer))

            # 标记题目为正确
            UserQuestionMapDao.update(self.user_type, self.swing_id, self.question_id, self.answer,
                                      constant.QUESTION_RESULT_CORRECT)

            self.ret_code = errcode.NO_ERROR
            self.ret_msg = 'ok'
            self.ret_data = {
                "answer_result": constant.QUESTION_RESULT_CORRECT,
                "score": 10
            }
            return
