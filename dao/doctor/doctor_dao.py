# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class DoctorDao(BaseDao):
    db_name = "doctor"
    table_name = "doctor"

    @classmethod
    def get_by_section(cls, section_code, page_num, page_size):
        """
        分页获取...

        :return:
        """
        offset = (page_num - 1) * page_size
        sql = "select * from {db}.{table} where del_flag=0 " \
              "and  section_code={section_code} " \
              "order by `number` ASC limit {offset},{limit}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   offset=offset,
                   limit=page_size,
                   section_code=section_code)

        item_list = doctor_conn.fetchall(sql)
        return item_list

    @classmethod
    def get_by_location(cls, province_code, city_code, area_code, page_num, page_size):
        """
        分页获取...

        :return:
        """
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

        offset = (page_num - 1) * page_size
        sql = "select * from {db}.{table} where del_flag=0 " \
              "{location_str} " \
              "order by `number` ASC limit {offset},{limit}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   offset=offset,
                   limit=page_size,
                   location_str=location_str)

        item_list = doctor_conn.fetchall(sql)
        return item_list
