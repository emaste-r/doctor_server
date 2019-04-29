# coding=utf-8
import json
import logging
import urllib
from urllib import urlencode


class JHSJ_SMSClient(object):
    """
        聚合数据短信通道，把appkey等放于此方便以后抽离成独立模块
    """

    def __init__(self):
        self.appkey = "4d3b0518463b18a0a3d9230b0b44fc7e"

    def send_sms_helper(self, mobile, template_id, tpl_value, dtype="json", method="GET"):
        """
        发送短信辅助函数


        # 变量名和变量值对。如果你的变量名或者变量值中带有#&amp;=中的任意一个特殊符号，请先分别进行urlencode编码后再传递，
        &lt;a href=&quot;http://www.juhe.cn/news/index/id/50&quot; target=&quot;_blank&quot;&gt;详细说明&gt;&lt;/a&gt;

        :param mobile:  接收短信的手机号码
        :param template_id:  短信模板ID，请参考个人中心短信模板设置
        :param tpl_value: 模板对应的value
        :param dtype: 返回数据的格式,xml或json，默认json
        :param method: 发送方法
        :return:
        """
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": mobile,
            "tpl_id": template_id,
            "tpl_value": tpl_value,
            "key": self.appkey,
            "dtype": dtype,

        }
        params = urlencode(params)
        if method == "GET":
            f = urllib.urlopen("%s?%s" % (url, params))
        else:
            f = urllib.urlopen(url, params)

        content = f.read()
        res = json.loads(content)
        if res:
            error_code = res["error_code"]
            if error_code == 0:
                # 成功请求
                logging.info(res["result"])
            else:
                logging.info("%s:%s" % (res["error_code"], res["reason"]))
        else:
            logging.info("request api error")

    def send_sms(self, mobile, tpl_value, dtype="json", method="GET"):
        """

        【自在家】您的验证码是#code#。如非本人操作，请忽略本短信。

        :param mobile:
        :param tpl_value:
        :param dtype:
        :param method:
        :return:
        """
        template_id = 98868
        self.send_sms_helper(mobile, template_id, tpl_value, dtype, method)

    def send_login(self, mobile, tpl_value, dtype="json", method="GET"):
        """
        注册
        :param mobile:
        :param tpl_value:
        :param dtype:
        :param method:
        :return:
        """
        template_id = 102378
        self.send_sms_helper(mobile, template_id, tpl_value, dtype, method)

    def send_register(self, mobile, tpl_value, dtype="json", method="GET"):
        """
        注册
        :param mobile:
        :param tpl_value:
        :param dtype:
        :param method:
        :return:
        """
        template_id = 98907
        self.send_sms_helper(mobile, template_id, tpl_value, dtype, method)

    def send_forget_pass(self, mobile, tpl_value, dtype="json", method="GET"):
        """
        找回密码
        :param mobile:
        :param tpl_value:
        :param dtype:
        :param method:
        :return:
        """
        template_id = 98908
        self.send_sms_helper(mobile, template_id, tpl_value, dtype, method)

    def send_change_phone(self, mobile, tpl_value, dtype="json", method="GET"):
        """
        改绑定手机
        :param mobile:
        :param tpl_value:
        :param dtype:
        :param method:
        :return:
        """
        template_id = 98909
        self.send_sms_helper(mobile, template_id, tpl_value, dtype, method)


jhsj_client = JHSJ_SMSClient()
