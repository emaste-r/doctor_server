# coding=utf-8
from common.mylog import logger
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HospitalDoctorMapDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital_doctor_map"

    @classmethod
    def get_by_location_and_section(cls, province_code, city_code, area_code, section_outer, section_inner, page_num,
                                    page_size):
        """
        分页获取...

        :return:
        """

        # 省市区
        location_str = ""
        if province_code != 0 and city_code == 0 and area_code == 0:
            location_str = " and province={province} ".format(province=province_code)
        elif province_code != 0 and city_code != 0 and area_code == 0:
            location_str = " and province={province} and city={city} ". \
                format(province=province_code,
                       city=city_code)
        elif province_code != 0 and city_code != 0 and area_code != 0:
            location_str = " and province={province} and city={city} and area={area} ". \
                format(province=province_code,
                       city=city_code,
                       area=area_code)

        # 科室
        section_str = ""
        if section_outer and section_inner:
            section_str = " and section_p='{section_outer}' and section_c='{section_inner}' ". \
                format(section_outer=section_outer,
                       section_inner=section_inner
                       )
        elif section_outer and not section_inner:
            section_str = " and section_p='{section_outer}' ". \
                format(section_outer=section_outer,
                       )
        # 分页
        offset = (page_num - 1) * page_size

        sql = "select * from {db}.{table} where del_flag=0 " \
              "{location_str} {section_str} " \
              "limit {offset},{limit}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   offset=offset,
                   limit=page_size,
                   location_str=location_str,
                   section_str=section_str,
                   )
        logger.error(sql)
        item_list = doctor_conn.fetchall(sql)
        return item_list
