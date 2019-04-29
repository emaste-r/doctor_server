# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class AskAnswerReplyLikeDao(BaseDao):
    db_name = "doctor"
    table_name = "ask_answer_reply_like"
    escape_list = []  # 需要转义的list
    quot_list = ["update_time", "create_time"]  # 需要带引号的list
    not_append_list = ["user_id", "ask_id", "answer_id", "reply_id",
                       "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def insert(cls, ask_id, answer_id, reply_id, user_id):
        """

        :param ask_id:
        :param answer_id:
        :param user_id:
        :param reply_id:
        :return:
        """
        sql = "insert into {db}.{tbl}(ask_id, answer_id, reply_id, user_id) values ({ask_id}, {answer_id}, " \
              "{reply_id},{user_id}) " \
              "ON DUPLICATE KEY UPDATE del_flag=0 ".format(db=cls.db_name,
                                                           tbl=cls.table_name,
                                                           ask_id=ask_id,
                                                           answer_id=answer_id,
                                                           user_id=user_id,
                                                           reply_id=reply_id,
                                                           )

        # 这个返回值会影响是否 like_num + 1，所以原生执行sql即可，不需要做太多事：raw_execute_sql
        ret = doctor_conn.raw_execute_sql(sql)
        return ret

    @classmethod
    def get_by_answer_reply_user(cls, answer_id, reply_id, user_id):
        """
        获取用户对此回复的点赞信息
        :param answer_id:
        :param user_id:
        :return:
        """
        sql = "select 1 from {db}.{tbl} where del_flag=0 and answer_id={answer_id} and reply_id={reply_id} and user_id={user_id}". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   answer_id=answer_id,
                   reply_id=reply_id,
                   user_id=user_id
                   )

        ret = doctor_conn.fetchone(sql)
        return ret
