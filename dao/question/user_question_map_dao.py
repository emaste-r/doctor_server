# coding=utf-8
from common import db_name_config
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_question_conn


class UserQuestionMapDao(BaseDao):
    db_name = db_name_config.DOCTOR_QUESTION_DB
    table_name = db_name_config.DOCTOR_QUESTION_USER_QUESTION_MAP_TBL

    @classmethod
    def insert(cls, user_type, user_id, question_id):
        sql = "insert into {db}.{tbl}(user_type, user_id, question_id) " \
              "values({user_type}, {user_id}, {question_id}) ON DUPLICATE KEY UPDATE del_flag=0". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   user_type=user_type,
                   user_id=user_id,
                   question_id=question_id)
        return doctor_question_conn.execute_sql(sql)

    @classmethod
    def update(cls, user_type, user_id, question_id, answer, result):
        sql = "update {db}.{tbl} set answer={answer}, result={result} " \
              "where user_type={user_type} and  user_id={user_id} and  question_id={question_id}" \
            .format(db=cls.db_name,
                    tbl=cls.table_name,
                    answer=answer,
                    result=result,
                    user_type=user_type,
                    user_id=user_id,
                    question_id=question_id)
        return doctor_question_conn.execute_sql(sql)
