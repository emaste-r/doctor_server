# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_user_conn


class UserDao(BaseDao):
    db_name = "doctor_user"
    table_name = "user"

    escape_list = ['user_name', 'avatar', 'device_model']  # 需要转义的list
    quot_list = ['cuid', 'phone', 'wxopenid', 'push_token', 'cookie', 'channel', 'app_version',
                 'device_type', 'device_os', 'register_ip', 'create_time', 'update_time', 'sid']  # 需要带引号的list
    not_append_list = ['sex', 'source', 'del_flag']  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_id(cls, user_id):
        """
        根据id获取用户

        :return:
        """

        sql = "select id, user_name, avatar, sex, phone, source from {db}.{table} where del_flag=0 and id={user_id}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   user_id=user_id)

        item = doctor_user_conn.fetchone(sql)
        return item

    @classmethod
    def get_by_phone(cls, phone):
        """
        根据id获取用户

        :return:
        """

        sql = "select id, source from {db}.{table} where del_flag=0 and phone='{phone}'". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   phone=phone)

        item = doctor_user_conn.fetchone(sql)
        return item

    @classmethod
    def get_profile_by_phone(cls, phone):
        """
        根据id获取用户

        :return:
        """

        sql = "select id as uid, user_name, phone, avatar, sex  from {db}.{table} where del_flag=0 and phone='{phone}'". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   phone=phone)

        item = doctor_user_conn.fetchone(sql)
        return item

    @classmethod
    def get_sid_by_userid(cls, uid):
        sql = "select sid, update_time from {db}.{table} where del_flag=0 and uid='{uid}'". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   uid=uid)

        item = doctor_user_conn.fetchone(sql)
        return item

    @classmethod
    def check_sid(cls, uid, sid):
        sql = "select 1 from {db}.{table} where del_flag=0 and id={uid} and sid='{sid}'". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   uid=uid,
                   sid=sid,
                   )

        item = doctor_user_conn.fetchone(sql)
        return item
