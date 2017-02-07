#!Python
#coding=gbk
__version__ = "$Id$"

import cclogger
import ccurl

# 中文注释
import sys
reload(sys)
sys.setdefaultencoding("gbk")

MSGEXPRESS_ROOT_URL = "http://1290.me"
MSGEXPRESS_POST_URL = MSGEXPRESS_ROOT_URL + "/!push-msgadd"


def sendMsg(to, message):
    """向指定消息速递用户发送消息"""

    params = {
        "domains": to,
        "permitcode": "",
        "nickname": "",
        "sendtime": "",
        #"destory": "1",  # 手机收到消息1分钟后自动销毁
        "video": "",
        "act": "",
        "code": "",
        "size": "",
        "extension": "",
        "mime": "",
        "md5": "",
        "type": "",
        "upload": "",
        "uinfo": "",
        "q": to,
        "uploadname": "",
        "content": message.encode("utf-8"),
        "onlyme": "",
        "f": "2",
        "size": "",
        "yunstore": "",
        "imgtype": "",
        "width": "",
        "height": "",
        "cover": "",
        "zip": "",
        "json": "",
        "image": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.92 Safari/537.4",
        "Referer": MSGEXPRESS_ROOT_URL + "/" + to
    }
    request = ccurl.buildRequest(MSGEXPRESS_POST_URL, params)
    response = ccurl.tryOpenRequest(request)
    content = unicode(response.read(), 'utf-8', 'ignore').encode('gbk', 'ignore')
    logger = cclogger.buildLogger()
    logger.info("向[" + to + "]发送消息[" + message + "]")
    if content.find("success") >= 0:
        logger.info("成功")
        return True
    else:
        logger.info("失败[" + content + "]")
        return False

