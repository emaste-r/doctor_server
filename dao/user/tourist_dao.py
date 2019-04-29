# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn, doctor_user_conn


class TouristDao(BaseDao):
    db_name = "doctor_user"
    table_name = "user_tourist"

    @classmethod
    def get_by_cuid(cls, cuid):
        """
        根据id获取
        :param cuid:
        :return:
        """
        sql = "select id as tid from {db}.{tbl} where cuid = '{cuid}'". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   cuid=cuid,
                   )
        item = doctor_user_conn.fetchone(sql)
        return item

    @classmethod
    def insert(cls, cuid, device_type, device_os, device_model, app_version, channel, open_push, push_token):
        """
        根据id获取用户

        :return:
        """

        sql = "insert into {db}.{tbl}(cuid, device_type, device_os, device_model, app_version, channel, " \
              "open_push, push_token) values ('{cuid}', '{device_type}', '{device_os}', '{device_model}', " \
              "'{app_version}', '{channel}', {open_push}, '{push_token}') " \
              "on duplicate key update device_type='{device_type}', device_os='{device_os}', " \
              "device_model='{device_model}', app_version='{app_version}', push_token='{push_token}', " \
              "channel='{channel}' ".format(db=cls.db_name,
                                            tbl=cls.table_name,
                                            cuid=cuid,
                                            device_type=device_type,
                                            device_os=device_os,
                                            device_model=device_model,
                                            app_version=app_version,
                                            channel=channel,
                                            open_push=open_push,
                                            push_token=push_token,
                                            )

        item = doctor_conn.execute_sql(sql)
        return item
