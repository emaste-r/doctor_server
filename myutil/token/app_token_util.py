# coding=utf-8
import time

import jwt

from common import config
from dao.user.user_dao import UserDao
from myutil.token import sid_info
from myutil.token import sid_manager

secret = "miehaha_yuchunderenleiya_chenfuzaiwodejiaoxiaba"


def make_jwt_app_token(user_id):
    encoded = jwt.encode({'user_id': user_id, 'exp': int(time.time()) + 15 * 24 * 3600}, secret, algorithm='HS256')
    return encoded


def make_sid(user_type, uid, device_type, cuid):
    """
    生成一个新的sid，使用场景：注册、登录

    :param user_type:
    :param uid:
    :param device_type:
    :param cuid:
    :return:
    """

    # 生成新的sid_info
    new_sid_info = sid_info.SidInfo(user_type=user_type,
                                    userid=uid,
                                    version=config.APP_BACKEND_VERSION,
                                    timestamp=int(time.time()),
                                    device_type=device_type,
                                    cuid=cuid
                                    )

    # 生成新的sid
    new_sid = sid_manager.SidManager.info2sid(new_sid_info)

    # 更新用户表的sid
    UserDao.update({
        "id": uid,
        "sid": new_sid
    })

    return new_sid


if __name__ == '__main__':
    a = make_jwt_app_token(100001)
    b = make_jwt_app_token(100002)

    c = jwt.decode(a, secret, algorithms=['HS256'])
    d = jwt.decode(b, secret, algorithms=['HS256'])
    print a
    print c
    print b
    print d
    time.sleep(5)
    print jwt.decode(a, secret, algorithms=['HS256'])
