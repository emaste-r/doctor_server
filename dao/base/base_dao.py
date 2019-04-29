# coding=utf-8
import _mysql

from common import db_name_config
from common.mylog import logger
from support.db.mysql_db import doctor_conn, doctor_user_conn, doctor_question_conn


class BaseDao(object):
    db_name = ""
    table_name = ""
    escape_list = []  # 需要转义的list
    quot_list = []  # 需要带引号的list
    not_append_list = []  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_id(cls, _id):
        """
        根据id获取
        :param _id:
        :return:
        """
        sql = "select * from {db}.{tbl} where id = {_id}". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   _id=_id,
                   )
        if cls.db_name == "doctor":
            item = doctor_conn.fetchone(sql)
        elif cls.db_name == "doctor_user":
            item = doctor_user_conn.fetchone(sql)
        elif cls.db_name == "doctor_question":
            item = doctor_question_conn.fetchone(sql)
        else:
            logger.error("get_by_id() find no db to exec.")
            item = None
        return item

    @classmethod
    def update(cls, dic, where_col='id', where_col_str=False):
        """
        更新Something...
        :param dic: 字典
        :return:
        """
        key_value_lst = []
        for key, value in dic.items():
            logger.info("%s=%s" % (key, value))
            if key == where_col:
                continue

            # 普通字符串
            if type(value) == str or type(value) == unicode:
                value = _mysql.escape_string(value)
                item = "%s='%s'" % (key, value)

            # 需要追加的int，比如 like_num: (1, True)，那么是like_num = like_num + 1
            elif type(value) == tuple and len(value) == 2:
                if value[1]:
                    item = "%s=%s+%s" % (key, key, value[0])
                else:
                    item = "%s=%s" % (key, value[0])

            # 普通int， 比如 del_flag: 1, 直接 def_flag = 1
            else:
                item = "%s=%s" % (key, value)

            key_value_lst.append(item)

        sql = "update {db}.{tbl} set ".format(db=cls.db_name, tbl=cls.table_name)
        sql += ",".join(key_value_lst)

        # where 列默认是id
        where_value = dic[where_col]
        if where_col_str:
            sql += " where %s = '%s'" % (where_col, where_value)
        else:
            sql += ' where %s = %s' % (where_col, where_value)

        logger.info("base_update: %s" % sql)

        if cls.db_name == db_name_config.DOCTOR_DB:
            ret = doctor_conn.execute_with_exception(sql)
        elif cls.db_name == db_name_config.DOCTOR_USER_DB:
            ret = doctor_user_conn.execute_with_exception(sql)
        elif cls.db_name == db_name_config.DOCTOR_QUESTION_DB:
            ret = doctor_question_conn.execute_with_exception(sql)
        else:
            logger.error("error db...")
            ret = None
        return ret

    @classmethod
    def insert(cls, _dic):
        """
        插入Something...
        :param _dic: 新增的字典
        :return:
        """

        key_value_lst = []
        for key, value in _dic.items():
            # 普通字符串
            if type(value) == str or type(value) == unicode:
                value = _mysql.escape_string(value)
                item = "'%s'" % value
            else:
                item = "%s" % value

            key_value_lst.append(item)
        sql = "insert into {db}.{tbl}({column_list}) values ({value_list})". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   column_list=','.join(["`%s`" % v for v in _dic.keys()]),
                   value_list=','.join(key_value_lst))

        logger.info("base_insert===> %s" % sql)

        if cls.db_name == db_name_config.DOCTOR_DB:
            ret = doctor_conn.execute_with_exception(sql)
        elif cls.db_name == db_name_config.DOCTOR_USER_DB:
            ret = doctor_user_conn.execute_with_exception(sql)
        elif cls.db_name == db_name_config.DOCTOR_QUESTION_DB:
            ret = doctor_question_conn.execute_with_exception(sql)
        else:
            logger.error("error db...")
            ret = None
        return ret
