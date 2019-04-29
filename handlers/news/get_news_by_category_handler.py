# coding=utf-8
from common import errcode
from dao.news.news_dao import NewsDao
from handlers.base.base_handler import BaseHandler
from services.news.news_service import NewsService


class GetNewsByCategoryHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "category_id": None,
            "page_num": None,
            "page_size": None,
            "common_param": {},
        }
        need_para = (
            "category_id",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetNewsByCategoryHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        news_list = NewsDao.get_by_category(self.para_map["category_id"],
                                            self.para_map["page_num"],
                                            self.para_map["page_size"])

        for news in news_list:
            NewsService.wrap_news(news)

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {"news_list": news_list}
        return
