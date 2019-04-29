# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class NewsImgDao(BaseDao):
    db_name = "doctor"
    table_name = "news_img"
    escape_list = []  # 需要转义的list
    quot_list = ["img_url", "thumb_url", "create_time", "update_time"]  # 需要带引号的list
    not_append_list = ["news_id", "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_news_id(cls, news_id):
        """
        根据分类获取news
        :param news_id:
        :return:
        """
        sql = "select img_url, thumb_url from {db}.{tbl} where news_id={news_id}". \
            format(db=cls.db_name,
                   tbl=cls.table_name,
                   news_id=news_id,
                   )
        items = doctor_conn.fetchall(sql)
        return items
