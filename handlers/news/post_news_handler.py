# coding=utf-8
from common import constant
from common import errcode
from dao.news.news_category_map_dao import NewsCategoryMapDao
from dao.news.news_dao import NewsDao
from dao.news.news_img_dao import NewsImgDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class PostNewsHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "category_id": None,
            "title": None,
            "content": None,
            "img_urls": None,
            "common_param": {},
        }
        need_para = (
            "category_id",
            "title",
            "content",
            "img_urls",
            "common_param",
        )
        super(PostNewsHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        user = UserDao.get_by_id(self.uid)
        if user["source"] != constant.USER_SOURCE_DOCTOR:
            self.ret_code = errcode.USER_NOT_DOCTOR
            self.ret_msg = 'user not doctor'
            return

        # 插入帖子
        news_id = NewsDao.insert({
            "author_id": self.uid,
            "title": self.para_map["title"],
            "content": self.para_map["content"],
        })

        # 插入帖子的图片
        for img_url in self.para_map["img_urls"]:
            NewsImgDao.insert({
                "news_id": news_id,
                "img_url": img_url
            })

        # 插入帖子和news的映射
        NewsCategoryMapDao.insert({
            "news_id": news_id,
            "category_id": self.para_map["category_id"]
        })

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {
            "news_id": news_id
        }
        return
