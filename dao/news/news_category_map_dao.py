# coding=utf-8
from dao.base.base_dao import BaseDao


class NewsCategoryMapDao(BaseDao):
    db_name = "doctor"
    table_name = "news_category_map"
    escape_list = []  # 需要转义的list
    quot_list = ["create_time", "update_time"]  # 需要带引号的list
    not_append_list = ["news_id", "category_id", "sort", "del_flag"]  # int list，但是不可能有append操作的list，如 img_id
    append_list = []  # int list, 但是可能有append操作的list，如add_cnt, view_cnt
