# coding=utf-8
import sys

from common import config

sys.path.append('..')

import logging
import base64

from Crypto.Cipher import DES, DES3
from pyDes import triple_des, CBC, PAD_PKCS5


class MyDESCryptUtil(object):
    """
    pip install pycrypto == 2.6.1
    pip install pyDes==2.0.1
    """

    @classmethod
    def decrypt(self, decryptText):
        try:
            k = DES.new(config.SID_ENCRYPT_KEY, DES.MODE_CBC, "\0\0\0\0\0\0\0\0")
            ret = k.decrypt(decryptText)

            # 去掉右边的空格
            ret = ret.rstrip()

            return ret
        except Exception, ex:
            logging.error(ex, exc_info=1)
            return ""

    @classmethod
    def encrypt(self, ecryptText):
        try:
            # 不够8位要用空格补齐八位，才能编码成功...
            if len(ecryptText) % 8 != 0:
                blank = ''
                for i in range(8 - len(ecryptText) % 8):
                    blank += ' '
                ecryptText = ecryptText + blank

            k = DES.new(config.SID_ENCRYPT_KEY, DES.MODE_CBC, "\0\0\0\0\0\0\0\0")
            ret = k.encrypt(ecryptText)
            return ret
        except Exception, ex:
            logging.error(ex, exc_info=1)
            return ""

    @classmethod
    def pydes_encrypt_des3(cls, s):
        """
        pydes 库 的des3加密 - 和系统配置中的wx-app-secret就是用此方法加密！
        :param s:
        :return:
        """
        k = triple_des(config.SID_DES3_KEY, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        return k.encrypt(s)

    @classmethod
    def pydes_decrypt_des3(cls, s):
        """
        pydes 库 的des3解密
        :param s:
        :return:
        """
        k = triple_des(config.SID_DES3_KEY, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        return k.decrypt(s)

    @classmethod
    def pycrypto_encrypt_des3(cls, ecryptText):
        """
        pycrypto 库 的des3加密
        :param ecryptText:
        :return:
        """
        # 必须满8的倍数
        if len(ecryptText) % 8 != 0:
            blank = ''
            for i in range(8 - len(ecryptText) % 8):
                blank += ' '
            ecryptText = ecryptText + blank

        k = DES3.new(config.SID_DES3_KEY, 2, "\0\0\0\0\0\0\0\0")
        return k.encrypt(ecryptText)

    @classmethod
    def pycrypto_decrypt_des3(cls, decryptText):
        """
        pycrypto 库 的des3解密
        :param decryptText:
        :return:
        """
        k = DES3.new(config.SID_DES3_KEY, 2, "\0\0\0\0\0\0\0\0")
        ret = k.decrypt(decryptText)

        # 去掉右边的空格
        ret = ret.rstrip()
        return ret


if __name__ == '__main__':
    s = 'f6dad5e062eb12a1e6e7644e753f1cb01'

    c = MyDESCryptUtil.pycrypto_encrypt_des3(s)
    d = base64.b64encode(c)
    print d

    f = base64.b64decode(d)
    e = MyDESCryptUtil.pycrypto_decrypt_des3(f)
    print e
