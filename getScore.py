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

funcs.crawlSinglePost(url,scoreFolderPath)


