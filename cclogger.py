#!Python
#coding=gbk
__version__ = "$Id$"

import logging

import sys
reload(sys)
sys.setdefaultencoding("gbk")

g_logger = None
def buildLogger():
    global g_logger
    if not g_logger:
        fmt = logging.Formatter('[%(asctime)s, %(funcName)s] %(message)s')
        filehandler = logging.FileHandler("log.log")
        filehandler.setFormatter(fmt)
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(fmt)

        g_logger = logging.getLogger()
        g_logger.setLevel(logging.DEBUG)
        g_logger.addHandler(filehandler)
        g_logger.addHandler(streamhandler)
    return g_logger

