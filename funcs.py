from bs4 import BeautifulSoup
import re
import os

class Spider:
    headers = ""
    session = ""
    # 构造函数
    def __init__(self,headers,session):
        self.headers = headers
        self.session = session
    def crawlSinglePage(self,url):
        # url = "http://bbs.guitarera.com/thread-2049-1-1.html"
        mdContent = ""

        r = self.session.get(url,headers = self.headers)
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
            mdContent += self.formatSingleFloor(singleFloorId,soup)

        #print(mdContent)
        return mdContent

    def formatSingleFloor(self,id,soup):

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

    def extractAllNumbers(self,str):
        m = re.findall('(\w*[0-9]+)\w*', str)
        return m

    def getPostAllPagesCountAndPageName(self,url):

        r = self.session.get(url, headers = self.headers)
        htmlContent = r.text
        #print(htmlContent)
        soup = BeautifulSoup(htmlContent)
        #print(soup.prettify())

        countInfoList =  soup.select("#pgt .pg label span")
        postSubject = soup.select("#thread_subject")[0].string  # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

        if len(countInfoList) <= 0:
            count = 1
        else:
            countInfo = soup.select("#pgt .pg label span")[0].text
            count = int(self.extractAllNumbers(countInfo)[0])

        return [count,postSubject]

    def getPostAllPagesUrl(self,baseUrl,totalPageCount):
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
    def crawlSinglePost(self,url, scoreFolderPath):
        # preprocess 获取总页数
        # test(url)
        [totalCount, pageName] = self.getPostAllPagesCountAndPageName(url)
        # 依据pageName新建一个文件夹（如果不存在的话）

        if not os.path.exists(scoreFolderPath):
            os.makedirs(scoreFolderPath)
        # 获取当前帖子的所有页面，即 1,2,3,...,7 (共7页）
        allUrls = self.getPostAllPagesUrl(url, totalCount)
        # print(allUrls)
        allContent = ""
        for singleUrl in allUrls:
            content = self.crawlSinglePage(singleUrl)  # 分别对每一个
            print("完成了一页帖子的输出，长度为", len(content), 'url:', singleUrl)
            allContent += content
            # 打开文件
        fo = open(scoreFolderPath + "/" + pageName + ".md", "w+")
        # print ("文件名: ", fo.name)
        line = fo.write(allContent)
        fo.close()

    # 获取当前版块页面的总页数和版块名
    def getBoardAllPagesCountAndBoardName(self,url):
        headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        r = self.session.get(url, headers=headers)
        htmlContent = r.text
        soup = BeautifulSoup(htmlContent)
        countInfo = soup.select("#pgt .pg label span")[0].text
        boardSubject = soup.select(".bm .xs2 a")[0].string # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

        count = int(self.extractAllNumbers(countInfo)[0])
        return [count,boardSubject]

    # 获取当前版块页面所有的帖子页链接
    def getBoardOnePagePostUrl(self,url):

        r = self.session.get(url,headers = self.headers)
        htmlContent = r.text
        print(r.text)
        soup = BeautifulSoup(htmlContent);

        pattern = re.compile("^thread-\d{1,10}-\d-\d.html$")  # 正则表达式 匹配形如 post_23456 的内容
        pattern2 = re.compile("^normalthread_\d{1,10}$")
        allPostsUrl = [];
        threadLista = soup.select("#threadlisttableid");
        if len(threadLista) > 0:
            threadList = threadLista[0]
        else:
            print("出错！ 当前版块未找到#threadlisttableid")
        singleThread = threadList.find_all_next(id = pattern2)
        for tag in singleThread:
            postLink = tag.find(href = pattern,class_="s xst")
            print(postLink['href'])
            allPostsUrl.append("http://bbs.guitarera.com/"+postLink['href'])
        return allPostsUrl

    def getBoardAllPagesUrl(self,baseUrl):
        # http://bbs.guitarera.com/forum-20-1.html
        [count,boardName] = self.getBoardAllPagesCountAndBoardName(baseUrl)
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