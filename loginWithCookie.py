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
    url = "http://bbs.guitarera.com/thread-2049-1-1.html?mobile=no"
    t = session.post(url,headers=headers,allow_redirects=False)
    soup = BeautifulSoup(t.text)
    print(soup.prettify())
    print(soup.find(text=re.compile("1016zym")))

    return
if __name__ == '__main__':
    print("准备登陆")
    isLogin()

