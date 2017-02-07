#!Python
#coding=gbk
__version__ = "$Id$"

import cclogger
import urllib, urllib2

# 中文注释
import sys
reload(sys)
sys.setdefaultencoding("gbk")

def buildRequest(url, params, headers = {}):
    """构造一个request"""
    return urllib2.Request(url, urllib.urlencode(params), headers)


def tryOpenRequest(request):
    """打开一个Request并返回Response，遇到异常将退出应用"""
    response = None
    logger = cclogger.buildLogger()
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        logger.info("打开 " + request.get_full_url() + " 失败，HTTP错误：" + str(e.code))
    except urllib2.URLError, e:
        logger.info("打开 " + request.get_full_url() + " 失败，网络连接错误：" + str(e.reason[0]) + " " + e.reason[1])

    if response:
        return response
    else:
        exit()

