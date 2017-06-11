import urllib.request
from bs4 import BeautifulSoup
import re


def power(x):
    return x*x

def crawlSinglePage(url):
    # url = "http://bbs.guitarera.com/thread-2049-1-1.html"
    mdContent = ""
    req = urllib.request.Request(url, headers={
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    data = urllib.request.urlopen(req).read()
    htmlContent = data.decode('gbk');# 吉他时代论坛是gbk编码

    soup = BeautifulSoup(htmlContent);
    print(soup.title.string)
    postSubject = soup.select("#thread_subject")[0].string # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素
    mdContent += postSubject+"\r\r"

    #postListTag = soup.select("#postlist")[0];
    pattern = re.compile("^post_\d{1,10}$") # 正则表达式 匹配形如 post_23456 的内容

    allFloorsId = [];
    for tag in soup.find_all(id = pattern):
        #print(tag.attrs['id'])
        allFloorsId.append(tag.attrs['id'])

    for singleFloorId in allFloorsId:
        mdContent += formatSingleFloor(singleFloorId,soup)

    #print(mdContent)
    return mdContent

def formatSingleFloor(id,soup):

    postTitleList = soup.select("#"+id+" .pcb h2")
    postContentList = soup.select("#"+id+" .t_f")
    postDownloadList = soup.select("#"+id+" .attnm a");

    fullContent = ""
    postTitle = ""
    postContent = ""
    downloadLinks = {}
    if len(postTitleList) > 0:
        postTitle = postTitleList[0].string

    if len(postContentList) > 0:
        postContent = postContentList[0].text

    if len(postDownloadList) > 0 :
        for singleLink in postDownloadList:
            downloadLinks[singleLink.string] = singleLink.attrs['href'];
    print(id);
    print(postTitle)
    print(postContent)

    fullContent += "## "+postTitle + "\r\r"\
                   + postContent + "\r\r"\
                   + "##### 曲谱下载链接："+'\r\r'

    for i in downloadLinks:
        fullContent += "[" + i +"](" + downloadLinks[i] + ")" + "\r\r"

    fullContent += "--------------------------" + "\r\r"

    return fullContent