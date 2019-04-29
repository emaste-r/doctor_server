# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class AskImgDao(BaseDao):
    db_name = "doctor"
    table_name = "ask_img"
    escape_list = ["img_url"]  # 需要转义的list
    quot_list = ["update_time", "create_time"]  # 需要带引号的list
    not_append_list = ["ask_id", "sort", "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_askid(cls, ask_id):
        """
        根据ask_id获取图片列表

        :return:
        """
        sql = "select img_url from {db}.{table} where del_flag=0 and ask_id={ask_id} order by sort desc ". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   ask_id=ask_id)

        item_list = doctor_conn.fetchall(sql)
        return item_list
