#encoding:UTF-8
import requests
import re
import os
import funcs

# http://bbs.guitarera.com/thread-2049-1-1.html # 李斯特页面
# data = {}
# data['word'] = 'Apple'
#
# url_values = urllib.parse.urlencode(data)
url = "http://bbs.guitarera.com/thread-2049-1-1.html"

# preprocess 获取总页数
# test(url)
[totalCount,pageName] = funcs.getPostAllPagesCountAndPageName(url)
# 依据pageName新建一个文件夹（如果不存在的话）
scoreFolderPath = "./score"
if not os.path.exists(scoreFolderPath):
    os.makedirs(scoreFolderPath)
# 获取当前帖子的所有页面，即 1,2,3,...,7 (共7页）
allUrls = funcs.getPostAllPagesUrl(url,totalCount)
# print(allUrls)
allContent = ""
for singleUrl in allUrls:
    content = funcs.crawlSinglePage(singleUrl) #分别对每一个
    print("完成了一页帖子的输出，长度为",len(content),'url:',singleUrl)
    allContent +=content
    # 打开文件
fo = open(scoreFolderPath+"/"+pageName+".md", "w+")
#print ("文件名: ", fo.name)
line = fo.write(allContent)
fo.close()