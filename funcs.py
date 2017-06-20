from bs4 import BeautifulSoup
import re
import os
import json
import time
import sys
from progress.spinner import Spinner


class Spider:
    headers = ""
    session = ""
    settingIndex = -1
    allPostUrls = []
    setting = {}
    scoreFolderPath = "./score/"

    # 构造函数
    def __init__(self, headers, session, scoreFolderPath,setting):
        self.headers = headers
        self.session = session
        self.settingIndex = setting['checkpoint']
        self.scoreFolderPath = scoreFolderPath
        self.setting = setting

    def formatSingleFloor(self, id, soup, postTitle):

        floorTitleList = soup.select("#"+id+" .pcb h2")
        postContentList = soup.select("#"+id+" .t_f")
        postDownloadList = soup.select("#"+id+" .attnm a");

        fullContent = ""
        floorTitle = ""
        postContent = ""
        downloadLinks = {}
        if len(floorTitleList) > 0:
            floorTitle = floorTitleList[0].string

        if len(postContentList) > 0:
            postContent = postContentList[0].text

        if len(postDownloadList) > 0 :
            for singleLink in postDownloadList:
                downloadLinks[singleLink.string] = singleLink.attrs['href'];
        #print(id);
        #print(postTitle)
        #print(postContent)

        fullContent += "## "+floorTitle + "\r\r"\
                       + postContent + "\r\r"\
                       + "##### 曲谱："+'\r\r'

        dst = self.scoreFolderPath+"/["+str(self.settingIndex+1)+"] "+postTitle
        if not os.path.exists(dst):
            os.makedirs(dst)

        for i in downloadLinks:
            downloadResult = self.download("http://bbs.guitarera.com/"+downloadLinks[i],dst=dst)
            if downloadResult is "success":
                tmpFullName = dst + "/tmp"
                fileFullName = dst + "/" + i
                self.rename(tmpFullName, fileFullName)
                fullContent += "<font color=green>[已下载][[点我打开](../"+fileFullName+")]</font>"
            elif downloadResult is "needPay":
                fullContent += "<font color=yellow>[未下载 需付费]</font>"
            elif downloadResult is "timeout":
                fullContent += "<font color=red>[下载失败 已超时]</font>"
            else:
                fullContent += "<font color=red>[下载失败]</font>"
            fullContent += "  原谱下载链接：[" + i +"](http://bbs.guitarera.com/" + downloadLinks[i] + ")" + "\r\r"

            time.sleep(5)

        fullContent += "--------------------------" + "\r\r"

        return fullContent

    def extractAllNumbers(self, str):
        m = re.findall('(\w*[0-9]+)\w*', str)
        return m

    def getPostAllPagesCountAndPageName(self, url):

        r = self.session.get(url, headers=self.headers)
        htmlContent = r.text
        #print(htmlContent)
        soup = BeautifulSoup(htmlContent)
        #print(soup.prettify())

        countInfoList =  soup.select("#pgt .pg label span")
        postSubjectList = soup.select("#thread_subject")
        if len(postSubjectList) <= 0:
            postSubject = "#thread_subject未找到，url："+url
            print(postSubject)
        else:
            postSubject = postSubjectList[0].string  # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

        if len(countInfoList) <= 0:
            count = 1
        else:
            countInfo = soup.select("#pgt .pg label span")[0].text
            count = int(self.extractAllNumbers(countInfo)[0])

        return [count,postSubject]

    # 获取当前版块页面的总页数和版块名
    def getBoardAllPagesCountAndBoardName(self, url):

        r = self.session.get(url, headers = self.headers)
        htmlContent = r.text
        soup = BeautifulSoup(htmlContent)
        countInfo = soup.select("#pgt .pg label span")[0].text
        boardSubject = soup.select(".bm .xs2 a")[0].string # select返回是一个list，即使只有一个元素也是，[0]表示第一个元素

        count = int(self.extractAllNumbers(countInfo)[0])
        return [count,boardSubject]

    # 获取当前版块页面所有的帖子页链接
    def getBoardOnePagePostUrl(self, url):

        r = self.session.get(url,headers = self.headers)
        htmlContent = r.text
        # print(r.text)
        soup = BeautifulSoup(htmlContent);

        postUrlPattern = re.compile("^thread-\d{1,10}-\d{1,3}-\d{1,3}.html$")  # 正则表达式 匹配形如 post_23456 的内容
        normalPostPattern = re.compile("^normalthread_\d{1,10}$")
        allPostsUrl = [];
        threadLista = soup.select("#threadlisttableid");
        if len(threadLista) > 0:
            threadList = threadLista[0]
        else:
            print("出错！ 当前版块未找到#threadlisttableid")
        singleThread = threadList.find_all_next(id = normalPostPattern)
        for tag in singleThread:
            postLink = tag.find(href = postUrlPattern,class_="s xst")
            print(postLink['href'])
            allPostsUrl.append("http://bbs.guitarera.com/"+postLink['href'])
        return allPostsUrl

    def getBoardAllPagesUrl(self, baseUrl):
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

    def getPostAllPagesUrl(self, baseUrl, totalPageCount):
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

    def getSinglePageAllDownloadLinks(self, soup):
        allLinks = []

        return

    # 爬取一个页面，比如一个帖子的一页
    def crawlSinglePage(self, url):
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
            mdContent += self.formatSingleFloor(singleFloorId,soup,postTitle=postSubject)

        self.getSinglePageAllDownloadLinks(soup)
        #print(mdContent)
        return mdContent

    # 爬取一个帖子（包含帖子的所有页) 比如 http://bbs.guitarera.com/thread-2049-1-1.html
    def crawlSinglePost(self, url, scoreFolderPath):
        # preprocess 获取总页数
        # test(url)
        [totalCount, pageName] = self.getPostAllPagesCountAndPageName(url)
        # 依据pageName新建一个文件夹（如果不存在的话）
        self.settingIndex += 1 # 设定当前的序号
        if not os.path.exists(scoreFolderPath):
            os.makedirs(scoreFolderPath)
        # 获取当前帖子的所有页面，即 1,2,3,...,7 (共7页）
        allUrls = self.getPostAllPagesUrl(url, totalCount)
        # print(allUrls)
        allContent = ""
        print("正在输出：",pageName)
        for singleUrl in allUrls:
            content = self.crawlSinglePage(singleUrl)  # 分别对每一个
            print("完成了一页帖子的输出，长度为", len(content), 'url:', singleUrl)
            allContent += content
            time.sleep(10)
            # 打开文件
        allContent = "原帖链接 ["+allUrls[0]+"]("+allUrls[0]+")\r\r" + allContent
        pdfIndex = self.settingIndex + 1;
        fo = open(scoreFolderPath + "/["+str(pdfIndex)+"] " + pageName + ".md", "w+")
        # print ("文件名: ", fo.name)
        line = fo.write(allContent)
        fo.close()
        if line > 0:
            self.updateSettingFile(checkpoint=self.settingIndex)


        print("------------------")

    # 爬取一个版块
    def crawlSingleBoard(self, boardUrl):
        allboardUrls = self.getBoardAllPagesUrl(boardUrl)
        if self.settingIndex is -1:
            for boardUrl in allboardUrls:
                currentBoardPageAllPostUrls = self.getBoardOnePagePostUrl(boardUrl)
                self.allPostUrls.extend(currentBoardPageAllPostUrls)

            self.updateSettingFile(allPostUrls=allboardUrls)
            #self.settingIndex = 0 # 标志着已开始进入正式的爬取工作
            # step 2: 获取当前board页面所有的帖子URL
            for postUrl in self.allPostUrls:
                self.crawlSinglePost(postUrl, self.scoreFolderPath)
        else:
            for i in range(self.settingIndex + 1,len(self.setting['allPostUrls'])):
                postUrl = self.setting['allPostUrls'][i]
                self.crawlSinglePost(postUrl, self.scoreFolderPath)

    def updateSettingFile(self,checkpoint=-1,allPostUrls=-1):
        settingFile = open("./setting.json", "w")
        if checkpoint is not -1:
            self.setting['checkpoint'] = self.settingIndex

        if allPostUrls is not -1:
            self.setting['allPostUrls'] = self.allPostUrls

        settingFile.write(json.dumps(self.setting, sort_keys=True, indent=4))
        settingFile.close()

    def download(self,link,dst):
        try:
            r = self.session.get(link, headers=self.headers, allow_redirects=True, stream=True,timeout = 3*60)
            filename = dst+"/tmp"
            print("开始下载：",link)
            print("开始写入文件：", filename)

            with open(filename, 'wb') as fd:
                i=1;
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
                    print("已写入："+str(128*i), end='\r')
                    i=i+1

            print("写入完毕")
            checkResult = self.check(dst=dst)
            if checkResult is "needPay":
                return "needPay"
            else:
                return "success"
        except Exception:
            print("请求超时")
            return "timeout"

    def check(self,dst):
        filename = dst+"/tmp"
        fo = open(filename, "r", encoding="gbk")
        try:
            content = fo.read()
        except (Exception, UnicodeDecodeError):
            print("乐谱下载成功")
            return "success"
        soup = BeautifulSoup(content)
        # print(soup.prettify())
        invalid = soup.find(text=re.compile("抱歉，原附件链接已失效"))
        needPay = soup.find(text=re.compile("附件需要付费，请您付费后下载"))

        if invalid is not None:
            print("链接失效")
            newlink = "http://bbs.guitarera.com/" + soup.select("#messagetext a")[0].attrs['href']
            print("新链接：", newlink)
            self.download(newlink,dst)
        elif needPay is not None:
            print("该附件收费")
            return "needPay"
        else:
            return

    def rename(self,src,dst):
        os.rename(src, dst)