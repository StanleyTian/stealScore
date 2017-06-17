#encoding:UTF-8
import requests
import re
import os
import http.cookiejar as cookielib

import funcs
import simuLogin
# http://bbs.guitarera.com/thread-2049-1-1.html # 李斯特页面
# data = {}
# data['word'] = 'Apple'
#
# url_values = urllib.parse.urlencode(data)
scoreFolderPath = "./score"
url = "http://bbs.guitarera.com/thread-2049-1-1.html"
url = "http://bbs.guitarera.com/thread-6013-1-1.html"
boardBaseUrl = "http://bbs.guitarera.com/forum-20-1.html"
# board
# step 1: 获取当前board总页数
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'

headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    "Host":"bbs.guitarera.com",
    "Referer":"http://bbs.guitarera.com/forum.php",
    'User-Agent':agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies_LWP')
try:
    session.cookies.load(ignore_discard = True,ignore_expires=True)
    print("Cookie 已加载")
except:
    print("Cookie 未能加载")

# account = '1016zym'
# password = "2424d24be57cacd465d3a574b4dbfafd"
# simuLogin.login(account, password)

spider = funcs.Spider(headers,session)
allboardUrls = spider.getBoardAllPagesUrl(boardBaseUrl)

for boardUrl in allboardUrls:
    allPostUrl = spider.getBoardOnePagePostUrl(boardUrl)
    # step 2: 获取当前board页面所有的帖子URL
    for postUrl in allPostUrl:
        spider.crawlSinglePost(postUrl,scoreFolderPath)