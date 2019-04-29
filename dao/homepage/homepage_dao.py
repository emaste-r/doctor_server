# coding=utf-8
import datetime

from common import db_name_config
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class HomepageDao(BaseDao):
    db_name = db_name_config.DOCTOR_DB
    table_name = db_name_config.DOCTOR_HOMEPAGE_TBL

    @classmethod
    def get_all(cls, is_white_mode=False):
        """
        获取全部的homepage items
        如果是白名单模式，则可以看到未上架未过期的item，否则只能看到已上架未过期的item。

        :param is_white_mode: 是否为白名单模式
        :return:
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_white_mode:
            sql = "select id, ui_type, `title`, `desc`, obj_id, link, float_txt, img_url from {db}.{table} " \
                  "where del_flag=0  " \
                  "and end_time>='{now}' order by sort desc".format(db=cls.db_name,
                                                                    table=cls.table_name,
                                                                    now=now)
        else:
            sql = "select id, ui_type, `title`, `desc`, obj_id, link, float_txt, img_url from {db}.{table} " \
                  "where del_flag=0  " \
                  "and start_time<='{now}' and end_time>='{now}' " \
                  "order by sort desc".format(db=cls.db_name,
                                              table=cls.table_name,
                                              now=now)
        item_list = doctor_conn.fetchall(sql)
        return item_list
