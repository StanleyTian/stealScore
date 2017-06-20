#encoding:UTF-8
import requests
import re
import os
import http.cookiejar as cookielib
import json
import funcs
from progress.bar import Bar
# http://bbs.guitarera.com/thread-2049-1-1.html # 李斯特页面
# data = {}
# data['word'] = 'Apple'
#{
#   "checkpoint":-1
# }
# url_values = urllib.parse.urlencode(data)

settingFile = open("./setting.json", "r+")
settingContent = settingFile.read()
setting = json.loads(settingContent)
settingFile.close()

# checkpoint 表示已爬的post
checkpoint = int(setting["checkpoint"])

if checkpoint > 0:
    a = input("发现上次的爬取未完成，是否继续？(y/n)")
    if a is not "y" or "Y":
        # 重新爬取
        checkpoint = -1
        setting['checkpoint'] = -1

boardBaseUrl = "http://bbs.guitarera.com/forum-20-1.html"
scoreFolderPath = "./score"

# board
# step 1: 获取当前board总页数
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'

headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    "Host": "bbs.guitarera.com",
    "Referer": "http://bbs.guitarera.com/forum.php",
    'User-Agent': agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='./cookies_LWP')
try:
    session.cookies.load(ignore_discard=True, ignore_expires=True)
    print("Cookies 已加载")
except:
    print("Cookie 未能加载")

# account = '1016zym'
# password = "2424d24be57cacd465d3a574b4dbfafd"
# simuLogin.login(account, password)

spider = funcs.Spider(headers,session,scoreFolderPath,setting)

if __name__ == '__main__':
    print("准备登陆")

    coinfree = "http://bbs.guitarera.com/forum.php?mod=attachment&aid=Mjc3NzN8ZWFjZjgwOWF8MTQ5Nzg3ODE3M3wzODMwNXw2NDg3"
    coin1 = "http://bbs.guitarera.com/forum.php?mod=attachment&aid=MTE4Mjg3fDdjMGJiMGM2fDE0OTc3Nzc3Nzl8MHwxOTM5" #1 时代币
    spider.download(coinfree,".")
    spider.rename("tmp","new2.pdf")
    # check()


