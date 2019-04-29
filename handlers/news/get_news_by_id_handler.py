# coding=utf-8
from common import errcode
from dao.news.news_dao import NewsDao
from handlers.base.base_handler import BaseHandler
from services.news.news_service import NewsService


class GetNewsByIdHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "news_id": None,
            "common_param": {},
        }
        need_para = (
            "news_id",
            "common_param",
        )
        super(GetNewsByIdHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        news = NewsDao.get_by_id(self.para_map["news_id"])
        NewsService.wrap_news(news)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {"news": news}
        return
