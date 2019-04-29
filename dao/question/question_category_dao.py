# coding=utf-8
from common import db_name_config
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class QuestionCategoryDao(BaseDao):
    db_name = db_name_config.DOCTOR_QUESTION_DB
    table_name = db_name_config.DOCTOR_QUESTION_CATEGORY_TBL

    @classmethod
    def get_all(cls):
        """
        获取全部分类列表
        :return:
        """
        sql = "select id,`name` from {db}.{tbl} where del_flag=0 order by sort desc". \
            format(db=cls.db_name,
                   tbl=cls.table_name)
        items = doctor_conn.fetchall(sql)
        return items
