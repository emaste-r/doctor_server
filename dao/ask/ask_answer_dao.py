# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class AskAnswerDao(BaseDao):
    db_name = "doctor"
    table_name = "ask_answer"
    escape_list = ["content"]  # 需要转义的list
    quot_list = ["update_time", "create_time"]  # 需要带引号的list
    not_append_list = ["user_id", "ask_id", "answer_id", "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = ["reply_num", "like_num"]  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_page(cls, ask_id, page_num, page_size):
        """
        分页获取问题...

        :return:
        """

        offset = (page_num - 1) * page_size
        sql = "select * from {db}.{table} where ask_id={ask_id} and  del_flag=0 limit {offset},{limit}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   ask_id=ask_id,
                   offset=offset,
                   limit=page_size)

        item_list = doctor_conn.fetchall(sql)
        return item_list
