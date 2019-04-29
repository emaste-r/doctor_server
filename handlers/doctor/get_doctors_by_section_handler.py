# coding=utf-8
from common import errcode
from dao.doctor.doctor_dao import DoctorDao
from handlers.base.base_handler import BaseHandler


class GetDoctorsBySectionHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "page_num": None,
            "page_size": None,
            "section": None,
            "common_param": {},
        }
        need_para = (
            "section",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetDoctorsBySectionHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        doctors = DoctorDao.get_by_section(self.para_map["section"],
                                           self.para_map["page_num"],
                                           self.para_map["page_size"])

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "list": doctors
        }

        return
