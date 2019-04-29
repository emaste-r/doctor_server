# coding:utf-8
import json
import pickle
import time

from flask import jsonify
from flask import request
from flask.views import MethodView

from common import config
from common import constant
from common import errcode
from common.mylog import logger
from dao.user.user_dao import UserDao
from myutil.token import sid_manager
from support.redis.redis_helper import redis_conn


class BaseHandler(MethodView):
    def __init__(self, expect_request_para, need_para):
        """
        # 这是每个请求的公共参数如net、version
        "common_param": {
            "client": "android_7.0",
            "cuid": "ffffffff-f5c5-8962-ffff-ffff8a0d869e",
            "did": "479f4826-472d-4913-866d-e94cfc68418c",
            "flavor": "main",
            "network": 1,
            "utc": 1524299337188,
            "version": "1.4.4",
            "sid": "xxxxxxxxxx"
        }

        :param expect_request_para:
        :param need_para:
        """
        super(BaseHandler, self).__init__()

        t = time.time()
        self.trace_id = self.__class__.__name__ + str(int(round(t * 1000)))
        self.request = None
        self.ret_data = {}
        self.ret_code = errcode.NO_ERROR
        self.ret_msg = "ok"
        self.ret_user_msg = None
        self.parse_from_body = True
        self.para_map = {}
        self.expected_para = expect_request_para
        self.required_para = need_para
        self.common_param = {}
        self.os = ""  # android 或者ios
        self.flavor = ""  # 渠道
        self.version = ""  # 版本

        # 默认所有的api 接口的sid都必须是正确，如果有特殊如登录，则特殊去指定
        self.sid_control_level = constant.SID_NEED_BE_CORRECT

    def _handle_request(self):
        body = {}
        if self.parse_from_body:
            try:
                body = json.loads(request.data)

                # 统一打印下请求参数
                for key, value in body.iteritems():
                    if key == "common_param":
                        self.common_param = value
                        self.os = self.common_param["device_type"]
                        self.app_version = self.common_param["app_version"]

                        self.cuid = self.common_param["cuid"]  # 游客id
                        self.user_id = self.common_param["user_id"]  # 用户id

                logger.debug(body)
            except Exception, ex:
                logger.error("[%s] request.body not json str, ex: %s", self.trace_id, ex, exc_info=1)
                self.ret_code = errcode.JSON_BODY_DECODE_ERROR
                self.ret_msg = "request.body not json str"
                return False

        return self._check_sid() & self._parse_and_check_parameters()

    def _check_sid(self):
        """
        校验每一个请求的sid，后台服务，就是通过sid来控制整个app的生命账户的生命周期！！
        :return:
        """

        # 检查接口是否允许空字符串的sid，如登录、注册、忘记密码等可以允许空字符串
        if self.sid_control_level == constant.SID_CAN_BE_NULL:
            logger.info("sid can be null...")
            return True

        # 调试模式，可以不带sid
        if config.debug_mode == 1:
            try:
                logger.info("调试模式开启，不检查sid!")
                sid = self.common_param["sid"]
                sid_info = sid_manager.SidManager.sid2info(sid)
                if sid_info:
                    self.uid = sid_info.userid  # 这个是医生、用户的id，可能是游客id
                    self.user_type = sid_info.user_type  # 这个是用户类型，0-游客，1-用户，2-医生
                else:
                    self.uid = 0
                    self.user_type = 0

                return True
            except Exception, ex:
                logger.error(ex, exc_info=1)
                self.ret_code = errcode.SID_NOT_CORRECT
                self.ret_msg = "common_param sid not correct..."
                logger.error("common_param sid not correct...")
                return False

        # 其他情况走正常流程
        try:
            sid = self.common_param["sid"]
        except KeyError, _:
            self.ret_code = errcode.SID_NOT_CARRY
            self.ret_msg = "common_param without sid..."
            logger.error("common_param without sid...")
            return False

        # 检查sid是否解析正确
        sid_info = sid_manager.SidManager.sid2info(sid)
        if not sid_info:
            self.ret_code = errcode.SID_CANNOT_RESOLVE
            self.ret_msg = "sid cannot resolve to sid_info"
            logger.error("sid cannot resolve to sid_info: %s" % sid)
            return False

        # 如果是登录用户或者医生，则需要校验
        if sid_info.user_type in [constant.USER_SOURCE_LOGIN_USER, constant.USER_SOURCE_DOCTOR]:
            # 检查sid在db（也可以是redis中）中是否和用户匹配
            # todo: 优化为从redis中获取
            ret = UserDao.check_sid(sid_info.userid, sid)
            if not ret:
                self.ret_code = errcode.SID_NOT_CORRECT
                self.ret_msg = "sid not correct"
                logger.error("uid:%s, sid:%s is not correct!!!" % (sid_info.userid, sid))
                return False

        self.uid = sid_info.userid  # 这个是医生、用户的id，可能是游客id
        self.user_type = sid_info.user_type  # 这个是用户类型，0-游客，1-用户，2-医生
        return True

    def _parse_and_check_parameters(self):
        """
        1、解析参数 -> self.para_map中。
        2、检验参数是否正确？是否必传的参数没有传？

        :return: True, False
        """
        body = json.loads(request.data)

        for key, default_value in self.expected_para.iteritems():
            value = body.get(key, default_value)
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            self.para_map[key] = value
        if request.cookies:
            for key, default_value in self.expected_para.iteritems():
                value = request.cookies.get(key, default_value)
                if value != default_value:
                    self.para_map[key] = value

        for key in self.required_para:
            if self.para_map[key] is None:
                logger.error("request param is blank：%s" % key)
                self.ret_code = errcode.PARAM_REQUIRED_IS_BLANK
                self.ret_msg = "request param is blank"
                return False
        return True

    def _return_map(self):
        ret_map = {
            "ret": self.ret_code,
            "msg": self.ret_msg
        }
        if self.ret_data:
            ret_map["data"] = self.ret_data
        else:
            ret_map["data"] = {}
        if self.ret_user_msg:
            ret_map["user_msg"] = self.ret_user_msg
        return ret_map

    def _construct_cache_key(self):
        """
        子类可返回具体key, 过期时间
        :return: (key, expire_seconds)
        """
        return None, None

    def _try_read_cache(self):
        """
        尝试从缓存获取数据
        :return:
        """
        # 如果redis挂了，则直接返回False
        if not redis_conn.readable():
            return False

        cache_key, expire_seconds = self._construct_cache_key()
        if cache_key:
            cache_str = redis_conn.get(cache_key)
            if cache_str:
                logger.info("走缓存, key=%s" % cache_key)
                self.ret_code = errcode.NO_ERROR
                self.ret_msg = "ok."
                self.ret_data = pickle.loads(cache_str)
                return True

        return False

    def _try_write_cache(self):
        """
        尝试写返回数据到缓存中...
        :return:
        """
        # 如果redis挂了，则直接返回False
        if not redis_conn.writeable():
            return False

        key, expire_seconds = self._construct_cache_key()
        if key:
            logger.info("设置redis,key=%s, 过期时间=%ss" % (key, expire_seconds))
            redis_conn.set(key, pickle.dumps(self.ret_data))
            redis_conn.expire(key, expire_seconds)
        return True

    def _process_imp(self):
        logger.critical("need implement!!")
        pass

    def _handle_return(self):
        ret_map = self._return_map()
        logger.debug("[%s ###### END] 返回值: code=%s, msg=%s", self.trace_id, ret_map['ret'], ret_map['msg'])
        return jsonify(ret_map)

    def _stat(self):
        """
        每个接口自己实现相关的统计代码
        :return:
        """
        pass

    def _version_control(self):
        """
        每个接口实现自己的版本控制
        :return:
        """
        pass

    def post(self):
        self.request = request
        logger.debug("[%s ###### START]", self.trace_id)

        ret = self._handle_request()
        if ret is False:
            return self._handle_return()

        # 在最上层处理异常
        try:
            # 读到cache就直接返回
            if self._try_read_cache():
                return self._handle_return()

            self._version_control()
            self._process_imp()

            # 尝试写 redis 缓存
            self._try_write_cache()

        except Exception, ex:
            logger.error(ex, exc_info=1)
            self.ret_code = errcode.DB_OPERATION_ERROR
            self.ret_msg = "operation error"

        return self._handle_return()

    def _output_error(self, name):
        logger.error("不正确的参数：%s=%s" % (name, self.para_map[name]))
        self.ret_code = errcode.PARAMETER_ERROR
        self.ret_msg = "invalid parameter: %s" % name
