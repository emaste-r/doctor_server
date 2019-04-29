# coding=utf-8
from common import db_name_config
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_question_conn


class QuestionDao(BaseDao):
    db_name = db_name_config.DOCTOR_QUESTION_DB
    table_name = db_name_config.DOCTOR_QUESTION_QUESTION_TBL

    @classmethod
    def get_by_category(cls, category_id, page_num, page_size):
        """
        根据分类获取问题
        :param category_id:
        :param page_num:
        :param page_size:
        :return:
        """
        sql = "select id, title, answer, UNIX_TIMESTAMP(create_time) as create_time, " \
              "UNIX_TIMESTAMP(update_time) as update_time from {db}.{tbl} " \
              "where id in " \
              "(select question_id from {db}.{category_map_tbl} where category_id={category_id} ) " \
              "order by create_time desc limit {offset}, {page_size}" \
            .format(db=cls.db_name,
                    tbl=cls.table_name,
                    category_map_tbl="question_category_map",
                    category_id=category_id,
                    offset=(int(page_num) - 1) * page_size,
                    page_size=page_size
                    )
        items = doctor_question_conn.fetchall(sql)
        return items
