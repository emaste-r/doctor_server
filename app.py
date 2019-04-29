# coding=utf-8
import os

from flask import Flask

from handlers.ask.answer.answer_ask_handler import AnswerAskHandler
from handlers.ask.answer.get_answer_list_handler import GetAnswerListHandler
from handlers.ask.answer.like_answer_handler import LikeAnswerHandler
from handlers.ask.get_ask_list_handler import GetAskListHandler
from handlers.ask.post.doctor_post_ask_handler import DoctorPostAskHandler
from handlers.ask.post.post_ask_handler import PostAskHandler
from handlers.ask.post.user_post_ask_handler import UserPostAskHandler
from handlers.ask.reply.get_reply_list_handler import GetReplyListHandler
from handlers.ask.reply.like_answer_reply_handler import LikeAnswerReplyHandler
from handlers.ask.reply.reply_answer_handler import ReplyAnswerHandler
from handlers.doctor.get_doctors_by_location_and_section_handler import GetDoctorsByLocationAndSectionHandler
from handlers.doctor.get_doctors_by_location_handler import GetDoctorsByLocationHandler
from handlers.doctor.get_doctors_by_section_handler import GetDoctorsBySectionHandler
from handlers.hello_handler import HelloHandler
from handlers.homepage.get_homepage_handler import GetHomepageHandler
from handlers.news.get_news_by_category_handler import GetNewsByCategoryHandler
from handlers.news.get_news_by_id_handler import GetNewsByIdHandler
from handlers.news.get_news_categories_handler import GetNewsCategoriesHandler
from handlers.news.post_news_handler import PostNewsHandler
from handlers.question.get_question_category_list_handler import GetQuestionCategoryListHandler
from handlers.question.get_question_list_by_category_handler import GetQuestionListByCategoryHandler
from handlers.question.post_answer_handler import PostAnswerHandler
from handlers.section.get_sections_handler import GetSectionListHandler
from handlers.sms.sms_change_phone import SmsChangePhoneHandler
from handlers.sms.sms_forget_pass import SmsForgetPassHandler
from handlers.sms.sms_login import SmsLoginHandler
from handlers.sms.sms_register import SmsRegisterHandler
from handlers.user.account.change_phone_handler import ChangePhoneHandler
from handlers.user.account.phone_login_handler import PhoneLoginHandler
from handlers.user.account.phone_register_handler import PhoneRegisterHandler
from handlers.user.account.tourist_login_handler import TouristLoginHandler
from handlers.user.report_status_handler import UserReportStatusHandler
from handlers.user.update_profile_handler import UpdateProfileHandler

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', "docx"])

app.add_url_rule('/hello', view_func=HelloHandler.as_view("index"))

# 问答
app.add_url_rule('/v1/ask/post', view_func=PostAskHandler.as_view("post_ask"))
app.add_url_rule('/v1/ask/get_list', view_func=GetAskListHandler.as_view("ask_get_list"))
app.add_url_rule('/v1/ask/doctor_post', view_func=DoctorPostAskHandler.as_view("doctor_post_ask"))
app.add_url_rule('/v1/ask/user_post', view_func=UserPostAskHandler.as_view("user_post_ask"))
app.add_url_rule('/v1/ask/do_answer', view_func=AnswerAskHandler.as_view("answer_ask"))
app.add_url_rule('/v1/ask/do_reply', view_func=ReplyAnswerHandler.as_view("reply_answer"))
app.add_url_rule('/v1/ask/answer/do_like', view_func=LikeAnswerHandler.as_view("answer_lile_ask"))
app.add_url_rule('/v1/ask/answer/reply/do_like', view_func=LikeAnswerReplyHandler.as_view("answer_reply_lile_ask"))
app.add_url_rule('/v1/ask/answer/get_list', view_func=GetAnswerListHandler.as_view("answer_get_list"))
app.add_url_rule('/v1/ask/answer/reply/get_list', view_func=GetReplyListHandler.as_view("reply_get_list"))

# 头条
app.add_url_rule('/v1/news/categories', view_func=GetNewsCategoriesHandler.as_view("news_category_list"))
app.add_url_rule('/v1/news/by_category', view_func=GetNewsByCategoryHandler.as_view("news_by_category"))
app.add_url_rule('/v1/news/detail', view_func=GetNewsByIdHandler.as_view("news_by_id"))
app.add_url_rule('/v1/news/post', view_func=PostNewsHandler.as_view("post_news"))

# 医生
app.add_url_rule('/v1/doctors/by_location', view_func=GetDoctorsByLocationHandler.as_view("doctors_by_location"))
app.add_url_rule('/v1/doctors/by_section', view_func=GetDoctorsBySectionHandler.as_view("doctors_by_section"))
app.add_url_rule('/v1/doctors/by_location_and_section',
                 view_func=GetDoctorsByLocationAndSectionHandler.as_view("doctors_by_location_and_section"))

# 科室
app.add_url_rule('/v1/section/list', view_func=GetSectionListHandler.as_view("section_list"))

# 短信
app.add_url_rule('/v1/sms/change_phone', view_func=SmsChangePhoneHandler.as_view("sms_change_phone"))
app.add_url_rule('/v1/sms/register', view_func=SmsRegisterHandler.as_view("sms_register"))
app.add_url_rule('/v1/sms/login', view_func=SmsLoginHandler.as_view("sms_login"))
app.add_url_rule('/v1/sms/forget_pass', view_func=SmsForgetPassHandler.as_view("sms_forget_pass"))

# 用户
app.add_url_rule('/v1/user/report_status', view_func=UserReportStatusHandler.as_view("user_report_status"))
app.add_url_rule('/v1/user/update_profile', view_func=UpdateProfileHandler.as_view("user_update_profile"))
app.add_url_rule('/v1/user/account/tourist_login', view_func=TouristLoginHandler.as_view("tourist_login"))
app.add_url_rule('/v1/user/account/phone_register', view_func=PhoneRegisterHandler.as_view("phone_register"))
app.add_url_rule('/v1/user/account/phone_login', view_func=PhoneLoginHandler.as_view("phone_login"))
app.add_url_rule('/v1/user/account/change_phone', view_func=ChangePhoneHandler.as_view("change_phone"))

# 答题模式
app.add_url_rule('/v1/question/by_category/get',
                 view_func=GetQuestionListByCategoryHandler.as_view("get_question_by_category"))
app.add_url_rule('/v1/question/category/get',
                 view_func=GetQuestionCategoryListHandler.as_view("get_question_category_list"))
app.add_url_rule('/v1/question/answer/post', view_func=PostAnswerHandler.as_view("post_question_answer"))

# 首页
app.add_url_rule('/v1/homepage/get', view_func=GetHomepageHandler.as_view("get_homepage"))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
