import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import os


def crawlSinglePage(url):
    # url = "http://bbs.guitarera.com/thread-2049-1-1.html"
    mdContent = ""

    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url,headers = headers)
    htmlContent = r.text
    #print(r.text)
    soup = BeautifulSoup(htmlContent);
    #print(soup.title.string)
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
    #print(id);
    #print(postTitle)
    #print(postContent)

    fullContent += "## "+postTitle + "\r\r"\
                   + postContent + "\r\r"\
                   + "##### 曲谱下载链接："+'\r\r'

    for i in downloadLinks:
        fullContent += "[" + i +"](http://bbs.guitarera.com/" + downloadLinks[i] + ")" + "\r\r"

    fullContent += "--------------------------" + "\r\r"

    return fullContent

def extractAllNumbers(str):
    m = re.findall('(\w*[0-9]+)\w*', str)
    return m

def getPostAllPagesCountAndPageName(url):
    headers = {
        'Host':'bbs.guitarera.com',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.61 Mobile Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    htmlContent = r.text
    print(htmlContent)
    soup = BeautifulSoup(htmlContent)
    print(soup.prettify())

    countInfoList =  soup.select("#pgt .pg label span")
    postSubject = soup.select("#thread_subject")[0].string  # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

    if len(countInfoList) <= 0:
        count = 1
    else:
        countInfo = soup.select("#pgt .pg label span")[0].text
        count = int(extractAllNumbers(countInfo)[0])

    return [count,postSubject]

def getPostAllPagesUrl(baseUrl,totalPageCount):
    urlLength = len(baseUrl)
    allUrls = []
    a = baseUrl.rfind('-',0,urlLength) # 反向查找第一个'-'
    b = baseUrl.rfind('-',0,a)          # 反向查找第二个'-'

    #print(baseUrl[b+1:a])

    part1 = baseUrl[0:b+1]
    part2 = baseUrl[a:urlLength]

    for i in range(totalPageCount):
        allUrls.append(part1+str(i+1)+part2)
    return allUrls

# 爬取一个帖子（包含帖子的所有页) 比如 http://bbs.guitarera.com/thread-2049-1-1.html
def crawlSinglePost(url, scoreFolderPath):
    # preprocess 获取总页数
    # test(url)
    [totalCount, pageName] = getPostAllPagesCountAndPageName(url)
    # 依据pageName新建一个文件夹（如果不存在的话）

    if not os.path.exists(scoreFolderPath):
        os.makedirs(scoreFolderPath)
    # 获取当前帖子的所有页面，即 1,2,3,...,7 (共7页）
    allUrls = getPostAllPagesUrl(url, totalCount)
    # print(allUrls)
    allContent = ""
    for singleUrl in allUrls:
        content = crawlSinglePage(singleUrl)  # 分别对每一个
        print("完成了一页帖子的输出，长度为", len(content), 'url:', singleUrl)
        allContent += content
        # 打开文件
    fo = open(scoreFolderPath + "/" + pageName + ".md", "w+")
    # print ("文件名: ", fo.name)
    line = fo.write(allContent)
    fo.close()

# 获取当前版块页面的总页数和版块名
def getBoardAllPagesCountAndBoardName(url):
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url, headers=headers)
    htmlContent = r.text
    soup = BeautifulSoup(htmlContent)
    countInfo = soup.select("#pgt .pg label span")[0].text
    boardSubject = soup.select(".bm .xs2 a")[0].string # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

    count = int(extractAllNumbers(countInfo)[0])
    return [count,boardSubject]

# 获取当前版块页面所有的帖子页链接
def getBoardOnePagePostUrl(url):
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    r = requests.get(url,headers = headers)
    htmlContent = r.text
    #print(r.text)
    soup = BeautifulSoup(htmlContent);

    pattern = re.compile("^thread-\d{1,10}-\d-\d.html$")  # 正则表达式 匹配形如 post_23456 的内容
    pattern2 = re.compile("^normalthread_\d{1,10}$")
    allPostsUrl = [];
    threadList = soup.select("#threadlisttableid")[0]
    singleThread = threadList.find_all_next(id = pattern2)
    for tag in singleThread:
        postLink = tag.find(href = pattern,class_="s xst")
        print(postLink['href'])
        allPostsUrl.append("http://bbs.guitarera.com/"+postLink['href'])
    return allPostsUrl

def getBoardAllPagesUrl(baseUrl):
    # http://bbs.guitarera.com/forum-20-1.html
    [count,boardName] = getBoardAllPagesCountAndBoardName(baseUrl)
    urlLength = len(baseUrl)
    allUrls = []
    a = baseUrl.rfind('-', 0, urlLength)  # 反向查找第一个'-'
    b = baseUrl.rfind('.html')  # 反向查找'.html'

    # print(baseUrl[b+1:a])

    part1 = baseUrl[0:a + 1]
    part2 = baseUrl[b:urlLength]

    for i in range(count):
        allUrls.append(part1 + str(i + 1) + part2)
    return allUrls