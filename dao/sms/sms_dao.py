# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class SmsDao(BaseDao):
    db_name = "doctor_user"
    table_name = "sms"

    @classmethod
    def insert(cls, phone, msg, sms_type):
        """
        分页获取...

        :return:
        """
        sql = "insert into {db}.{tbl}(phone,msg,sms_type) values ('{phone}', '{msg}', {sms_type}) ". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   phone=phone,
                   msg=msg,
                   sms_type=sms_type,
                   )

        item = doctor_conn.execute_sql(sql)
        return item

    @classmethod
    def get_by_phone_and_code(cls, phone, code):
        """
        获取用户的手机号
        :param phone:
        :param code:
        :return:
        """
        sql1 = "select max(id) as id from {db}.{tbl} where  phone='{phone}'".format(
            db=cls.db_name,
            tbl=cls.table_name,
            phone=phone,
        )
        item1 = doctor_conn.fetchone(sql1)
        if not item1 or not item1["id"]:
            return None

        sql2 = "select * from {db}.{tbl} where id={id} and msg='{code}'".format(
            db=cls.db_name,
            tbl=cls.table_name,
            id=item1["id"],
            code=code,
        )
        item2 = doctor_conn.fetchone(sql2)
        return item2
