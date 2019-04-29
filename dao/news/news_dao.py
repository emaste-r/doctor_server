# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class NewsDao(BaseDao):
    db_name = "doctor"
    table_name = "news"
    escape_list = ["title", "content", ]  # 需要转义的list
    quot_list = ["create_time", "update_time"]  # 需要带引号的list
    not_append_list = ["author_id", "sort", "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = ["like_num", "comment_num", "follow_num",
                   "keep_num"]  # int list, 但是可能有append操作的list，如add_cnt, view_cnt

    @classmethod
    def get_by_category(cls, category_id, page_num, page_size):
        """
        根据分类获取news
        :param category_id:
        :param page_num:
        :param page_size:
        :return:
        """
        sql = "select id, title, content, author_id, comment_num, follow_num, keep_num, like_num," \
              "UNIX_TIMESTAMP(create_time) as create_time, UNIX_TIMESTAMP(update_time) as update_time from {db}.{tbl} " \
              "where id in " \
              "(select news_id from {db}.{category_map_tbl} where category_id={category_id} ) " \
              "order by create_time desc limit {offset}, {page_size}" \
            .format(db=cls.db_name,
                    tbl=cls.table_name,
                    category_map_tbl="news_category_map",
                    category_id=category_id,
                    offset=(int(page_num) - 1) * page_size,
                    page_size=page_size
                    )
        items = doctor_conn.fetchall(sql)
        return items
