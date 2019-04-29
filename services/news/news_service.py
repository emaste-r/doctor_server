# coding=utf-8
from common.mylog import logger
from dao.news.news_img_dao import NewsImgDao
from dao.user.user_dao import UserDao
from services.base.base_service import BaseService


class NewsService(BaseService):
    @classmethod
    def wrap_news(cls, news_item):
        if not news_item:
            return

        # 图片
        imgs = NewsImgDao.get_by_news_id(news_item["id"])
        news_item["imgs"] = imgs

        # 作者
        author = UserDao.get_by_id(news_item["author_id"])
        logger.error("author= %s" % author)
        news_item["author"] = author if author else {}
        del news_item["author_id"]
