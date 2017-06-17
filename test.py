# 测试自动下载
#encoding:UTF-8
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
from bs4 import BeautifulSoup

agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.61 Mobile Safari/537.36'

headers = {
    "Host":"bbs.guitarera.com",
    "Referer":"http://bbs.guitarera.com/forum.php",
    'User-Agent':agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies_LWP')
try:
    session.cookies.load(ignore_discard = True,ignore_expires=True)
    print("Cookie 已加载")
    print(session.cookies)
except:
    print("Cookie 未能加载")

def isLogin():
    url = "http://bbs.guitarera.com/forum.php?mod=attachment&aid=MjU0MTd8MTYzNzZmNzR8MTQ5NzY2MzU5NnwzODMwNXw2MDEz"
    r = session.get(url,headers=headers,allow_redirects=True, stream=True)
    filename = "test.pdf"
    print("开始写入文件：",filename)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    print("写入完毕")
    return
if __name__ == '__main__':
    print("准备登陆")
    isLogin()

