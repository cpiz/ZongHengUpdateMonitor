#!Python
#coding=gbk
__version__ = "$Id$"

import urllib, urllib2
import cookielib
import re
import os
import time

import cclogger
import ccmsgexpress
import ccurl

# 中文注释
import sys
reload(sys)
sys.setdefaultencoding("gbk")


class ZongHengNotify:
    #LIST_BOOK = ["188493", "189169"]
    #LIST_BOOK = ["188493"]
    CONFIG_FILE = "notify.cfg"
    BASE_URL = "http://m.zongheng.com"
    CHAPTER_LIST_URL = BASE_URL + "/chapter/list?bookid=[BOOK_ID]&asc=0&pageNum=1"

    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 2.3.5; zh-cn; MI-ONE Plus Build/GINGERBREAD) UC AppleWebKit/530+ (KHTML, like Gecko) Mobile Safari/530',
        'Referer':'http://m.zongheng.com' # 所有的请求都用这个来源页，也可以不用
    }

    logger = cclogger.buildLogger()

    def __init__(self):
        """初始化"""


    def run(self):
        """开始运行"""
        self.logger.info("==========================检查开始=============================")
        if not os.path.exists(self.CONFIG_FILE):
            self.logger.info("配置文件[" + self.CONFIG_FILE + "]不存在，取消任务")
            return

        f = file(self.CONFIG_FILE, 'r')
        file_content = f.readlines()
        f.close()

        for line in file_content:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue # 遇到无效行或注释行

            line_content = line.split(":")
            if len(line_content) != 2:
                continue

            book_id = line_content[0].strip()
            watcher_list = line_content[1].strip().split(",")
            self.checkBookWatcherList(book_id, watcher_list)
        self.logger.info("==========================检查结束=============================")


    def checkBookWatcherList(self, book_id, watcher_list):
        """为多个订阅者检查指定书号是否有更新并发送提醒"""
        if book_id == "":
            self.logger.info("书号无效，跳过")
            return

        if len(watcher_list) == 0:
            self.logger.info("订阅者为空，跳过")
            return

        # 访问目录页
        self.logger.info("开始查询[book_id = " + book_id + "]最新章节")
        url = self.CHAPTER_LIST_URL.replace('[BOOK_ID]', book_id)
        request = urllib2.Request(url, headers = self.headers)
        response = ccurl.tryOpenRequest(request)
        content = unicode(response.read(), 'utf-8', 'ignore').encode('gbk', 'ignore')

        # 获得书名
        book_name = ""
        pattern_book_name = re.compile("<title>(\S+)_手机纵横网</title>")
        result = pattern_book_name.search(content)
        if result:
            book_name = result.group(1)
        self.logger.info("book_name = " + book_name)

        # 获得最新章节
        latest_chapter_url = ""
        latest_chapter = ""
        pattern_chapter = re.compile("<div class=\"list\".+?<a href=\"(\S+)\".+?title=\S+>.+?\s+?(.+?)</a>", re.S | re.M)
        result = pattern_chapter.search(content)
        if result:
            latest_chapter_url = self.BASE_URL + result.group(1).strip()
            latest_chapter = result.group(2).strip()
        self.logger.info("latest_chapter = " + latest_chapter)
        self.logger.info("latest_chapter_url = " + latest_chapter_url)

        # 检查订阅了此书的人是否有更新
        for watcher in watcher_list:
            watcher = watcher.strip()
            self.checkBookWatcher(watcher, book_id, book_name, latest_chapter, latest_chapter_url)


    def checkBookWatcher(self, watcher, book_id, book_name, latest_chapter, latest_chapter_url):
        """为指定订阅者检查书是否有更新并发送提醒"""
        if watcher == "":
            self.logger.info("订阅者无效，跳过")
            return

        # 获得本地缓存的上一章信息
        self.logger.info("检查订阅者[" + watcher + "]")
        last_chapter = ""
        chapter_file = watcher + "_" + book_id + ".cpt"
        if os.path.exists(chapter_file):
            f = file(chapter_file, 'r')
            file_content = f.readlines();
            f.close()

            if len(file_content) > 0:
                last_chapter = file_content[len(file_content) - 1].split("|")[1].strip()
        self.logger.info("last_chapter = " + last_chapter)

        # 比对是否有更新
        if latest_chapter != last_chapter:
            # 发送消息通知
            msg = "《" + book_name + "》已更新，最新章节：" + latest_chapter + " " + latest_chapter_url
            if ccmsgexpress.sendMsg(watcher, msg):
                # 写入最新的章节
                now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
                f = file(chapter_file, 'a')
                f.write(now + "|" + latest_chapter + "\n")
                f.close()
        else:
            self.logger.info("此书无更新")


# 开始任务
def main():
    notify = ZongHengNotify()
    notify.run()


if __name__ == '__main__':
    main()


