# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class AskDao(BaseDao):
    db_name = "doctor"
    table_name = "ask"

    @classmethod
    def get_by_type(cls, ask_type, page_num, page_size):
        """
        分页获取问题...

        :return:
        """

        offset = (page_num - 1) * page_size
        sql = "select * from {db}.{table} where del_flag=0 and ask_type={ask_type} " \
              "order by sort desc limit {offset},{limit}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   ask_type=ask_type,
                   offset=offset,
                   limit=page_size)

        item_list = doctor_conn.fetchall(sql)
        return item_list
