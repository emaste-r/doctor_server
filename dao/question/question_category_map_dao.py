# coding=utf-8
from common import db_name_config
from dao.base.base_dao import BaseDao


class QuestionCategoryMapDao(BaseDao):
    db_name = db_name_config.DOCTOR_QUESTION_DB
    table_name = db_name_config.DOCTOR_QUESTION_QUESTION_CATEGORY_MAP_TBL
