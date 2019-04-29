# coding=utf-8
import json

from common import constant
from common import errcode
from common.mylog import logger
from dao.homepage.homepage_dao import HomepageDao
from handlers.base.base_handler import BaseHandler


class GetHomepageHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "common_param": None,
        }
        need_para = (
            "common_param",
        )
        super(GetHomepageHandler, self).__init__(expect_request_para, need_para)

    def _wrap_items(self, _items):
        """
        精简返回值
        :param _items:
        :return:
        """
        for item in _items:
            if "id" in item:
                del item["id"]
            if "obj_id" in item:
                del item["obj_id"]
            if "ui_type" in item:
                del item["ui_type"]

            # 解析desc
            if "desc" in item:
                if "{" in item["desc"]:
                    try:
                        item["desc"] = json.loads(item["desc"])
                    except Exception, ex:
                        logger.error(ex, exc_info=1)
                        item["desc"] = {}

                if "[" in item["desc"]:
                    try:
                        item["desc"] = json.loads(item["desc"])
                    except Exception, ex:
                        logger.error(ex, exc_info=1)
                        item["desc"] = []
        return _items

    def _process_imp(self):
        items = HomepageDao.get_all()

        # banner位
        banner_lst = list(filter(lambda x: x["ui_type"] == constant.UI_TYPE_V1_BANNER, items))
        leaderboard_list = list(filter(lambda x: x["ui_type"] == constant.UI_TYPE_V1_LEADERBORAD, items))
        hot_topic_list = list(filter(lambda x: x["ui_type"] == constant.UI_TYPE_V1_HOT_TOPIC, items))
        hot_doctor_list = list(filter(lambda x: x["ui_type"] == constant.UI_TYPE_V1_HOT_DOCTOR, items))
        hot_article_list = list(filter(lambda x: x["ui_type"] == constant.UI_TYPE_V1_HOT_ARTICLE, items))

        banner_lst = self._wrap_items(banner_lst)
        leaderboard_list = self._wrap_items(leaderboard_list)
        hot_topic_list = self._wrap_items(hot_topic_list)
        hot_doctor_list = self._wrap_items(hot_doctor_list)
        hot_article_list = self._wrap_items(hot_article_list)

        data = {
            "list": [
                {
                    "tips_name": "banner",
                    "ui_type": constant.UI_TYPE_V1_BANNER,
                    "items": banner_lst,
                },
                {
                    "tips_name": "排行榜",
                    "ui_type": constant.UI_TYPE_V1_LEADERBORAD,
                    "items": leaderboard_list,
                },
                {
                    "tips_name": "热门话题",
                    "ui_type": constant.UI_TYPE_V1_HOT_TOPIC,
                    "items": hot_topic_list,
                },
                {
                    "tips_name": "人气医生",
                    "ui_type": constant.UI_TYPE_V1_HOT_DOCTOR,
                    "items": hot_doctor_list,
                },
                {
                    "tips_name": "健康知识",
                    "ui_type": constant.UI_TYPE_V1_HOT_ARTICLE,
                    "items": hot_article_list,
                },
            ]
        }

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = data
        return
