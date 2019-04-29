# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class SectionDao(BaseDao):
    db_name = "doctor"
    table_name = "hospital_section"

    @classmethod
    def get_all(cls):
        """
        分页获取...

        :return:
        """
        sql = "select id as code, `name`, `level` from {db}.{table} where del_flag=0 ". \
            format(db=cls.db_name,
                   table=cls.table_name)

        item_list = doctor_conn.fetchall(sql)
        return item_list
