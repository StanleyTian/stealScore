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
session.cookies = cookielib.LWPCookieJar("cookies_LWP")
#session.cookies = cookielib.FileCookieJar("cookies_File")
try:
    session.cookies.load(ignore_discard = True)
    print("Cookie 已加载")
except:
    print("Cookie 未能加载")

def login(account,password):
    formhash = getFormhash()
    print("formhash:",formhash)
    postUrl = "http://bbs.guitarera.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login"
    postData = {
        'fastloginfield':"username",
        'username':account,
        'password':password,
        'quickforward':'yes',
        'handlekey':'ls',
        'formhash':formhash
    }
    loginPage = session.post(postUrl,data=postData,headers=headers,allow_redirects=True)
    soup = BeautifulSoup(loginPage.text, 'lxml')
    #print(soup.prettify())

    print(session.cookies)
    A = session.cookies
    session.cookies.save(ignore_discard = True,ignore_expires=True)
    searchResult = soup.find(text=re.compile("1016zym"))
    if(len(searchResult) > 0):
        print("登陆成功")
    else:
        print("登录失败")
    return ""
def getFormhash():
    url = "http://bbs.guitarera.com/member.php?mod=register&mobile=no"
    page = session.get(url,headers=headers).text
    soup = BeautifulSoup(page,'lxml')
    # print(soup.prettify())
    k = soup.find_all(type="hidden")
    r = soup.find_all("formhash")
    pattern = r'name="formhash" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    formhash = re.findall(pattern, page)
    if len(formhash) < 1:
        print("formhash 获取失败")
    return formhash[0]

if __name__ == '__main__':
    print("准备登陆")
    account = '1016zym'
    password = "2424d24be57cacd465d3a574b4dbfafd"
    login(account,password)
