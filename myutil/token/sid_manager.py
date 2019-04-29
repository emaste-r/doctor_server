# coding=utf-8
import base64

from common import config
from common.mylog import logger
from myutil.crypt.MyDESCrypt import MyDESCryptUtil
from myutil.token.sid_info import SidInfo


class SidManager(object):
    '''管理sid_info'''

    @classmethod
    def sid2info(cls, sid):
        """
        SID ==> INFO对象
         "%s|%s|%s|%s|%s|%s" % (
            self.user_type, self.userid, self.version, self.timestamp, self.device_type, self.cuid)
        :param sid:
        :return:
        """
        try:
            if not sid:
                logger.info("sid -> info: sid is null.")
                return None

            if config.SID_ENCRYPT_KEY:  # 加密
                sid = base64.b64decode(sid)
                sid = MyDESCryptUtil.decrypt(sid)

            values = sid.split('|')
            if len(values) < 6:
                logger.info("sid -> info: sid trans error...")
                return None

            sid_info = SidInfo(*values)

            if sid_info.is_expired():
                logger.info("SID=%s 过期" % sid_info.to_string())
                return None
            return sid_info
        except Exception, ex:
            logger.error("sid -> info失败：%s" % str(ex), exc_info=1)
            logger.error(sid)
            return None

    @classmethod
    def info2sid(cls, sid_info):
        '''SidInfo -> SID'''
        if not sid_info:
            return ""
        try:
            if config.SID_ENCRYPT_KEY:
                _str = MyDESCryptUtil.encrypt(sid_info.to_string())
                return base64.b64encode(_str)
            return sid_info.to_string()
        except Exception, ex:
            logger.error("info -> sid失败:%s" % str(ex), exc_info=1)
            return ""

    @classmethod
    def get_uid_by_sid(cls, sid):
        '''根据sid拿到userid'''
        sid_info = cls.sid2info(sid)
        if not sid_info:
            return -1
        return sid_info.userid
