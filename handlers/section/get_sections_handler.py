# coding=utf-8
from common import errcode
from dao.section.section_dao import SectionDao
from handlers.base.base_handler import BaseHandler


class GetSectionListHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "common_param": {},
        }
        need_para = (
            "common_param",
        )
        super(GetSectionListHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        sections = SectionDao.get_all()

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "list": sections
        }

        return
