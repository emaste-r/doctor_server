# coding=utf-8
import sys

from common import config
from common.mylog import logger
from myutil.tools import getCurrentTimestamp, timestamp2datetime

sys.path.append('..')
sys.path.append('../..')

iv = "\0\0\0\0\0\0\0\0"


class SidInfo(object):
    '''Sidinfo 生成通讯对象'''

    def __init__(self, user_type, userid, version, timestamp, device_type, cuid):
        self.user_type = user_type
        self.userid = userid
        self.version = version
        self.timestamp = int(timestamp)
        self.device_type = device_type
        self.cuid = cuid

    def is_available(self, t):
        '''传入：Terminal t, 判断SID是否有效'''
        if not self.version or not self.cuid or not self.device_type or not self.timestamp or self.userid < 1:
            return False

        if "android" == self.device_type:
            if t.IMEI != self.cuid:
                logger.info("[安卓]: t.IMEI = %s 不等于 cuid = %s" % (t.IMEI, self.cuid))
                return False
        elif "apple" == self.device_type:
            if t.ADID != self.cuid:
                logger.info("[苹果]: t.ADID = %s, 不等于 = %s" % (t.ADID, self.cuid))
                return False

        if self.is_expired():
            return False
        return True

    def is_expired(self):
        now = getCurrentTimestamp(bit_type=10)
        expires = config.SID_ExpiresSeconds
        expires_time = self.timestamp + expires

        if now > expires_time:
            logger.info("过期: 当前 = %s, 过期时间 = %s " % (
                timestamp2datetime(now, bit_type=10)[0], timestamp2datetime(expires_time, bit_type=10)[0]))
            return True
        return False

    def to_string(self):
        return "%s|%s|%s|%s|%s|%s" % (
            self.user_type, self.userid, self.version, self.timestamp, self.device_type, self.cuid)
