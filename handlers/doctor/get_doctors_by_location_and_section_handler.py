# coding=utf-8
from common import errcode
from common import redis_key_config
from dao.doctor.hospital_doctor_map_dao import HospitalDoctorMapDao
from handlers.base.base_handler import BaseHandler


class GetDoctorsByLocationAndSectionHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "page_num": None,
            "page_size": None,
            "province": None,
            "city": 0,
            "area": 0,
            "section_outer": None,
            "section_inner": "",
            "common_param": {},
        }
        need_para = (
            "province",
            "page_num",
            "page_size",
            "common_param",
            "section_outer",
        )
        super(GetDoctorsByLocationAndSectionHandler, self).__init__(expect_request_para, need_para)

    def _construct_cache_key(self):
        """
        子类可返回具体key, 过期时间
        :return: (key, expire_seconds)
        """
        key = "{prefix}{province}:{city}:{area}:{section_outer}:{section_inner}:{page_num}:{page_size}". \
            format(prefix=redis_key_config.API_PREFIX_GET_DOCTOR_BY_LOCATION_SECTION,
                   province=self.para_map["province"],
                   city=self.para_map["city"],
                   area=self.para_map["area"],
                   section_outer=self.para_map["section_outer"],
                   section_inner=self.para_map["section_inner"],
                   page_num=self.para_map["page_num"],
                   page_size=self.para_map["page_size"],
                   )
        return key, redis_key_config.API_EXPIRE_GET_DOCTOR_BY_LOCATION_SECTION

    def _process_imp(self):
        doctors = HospitalDoctorMapDao.get_by_location_and_section(self.para_map["province"],
                                                                   self.para_map["city"],
                                                                   self.para_map["area"],
                                                                   self.para_map["section_outer"],
                                                                   self.para_map["section_inner"],
                                                                   self.para_map["page_num"],
                                                                   self.para_map["page_size"])

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "list": doctors
        }

        return
