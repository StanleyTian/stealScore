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
scoreFolderPath = "./score"
url = "http://bbs.guitarera.com/thread-2049-1-1.html"
url = "http://bbs.guitarera.com/thread-6013-1-1.html"
boardUrl = "http://bbs.guitarera.com/forum-20-1.html"
# board
# step 1: 获取当前board总页数
a = funcs.getBoardAllPagesCountAndBoardName(boardUrl)


allPostUrl = funcs.getBoardAllPostUrl(boardUrl)





# step 2: 获取当前board页面所有的帖子URL
for postUrl in allPostUrl:
    funcs.crawlSinglePost(postUrl,scoreFolderPath)


