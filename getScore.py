#encoding:UTF-8
import urllib.parse
import urllib.request
import funcs

# http://bbs.guitarera.com/thread-2049-1-1.html # 李斯特页面
# data = {}
# data['word'] = 'Apple'
#
# url_values = urllib.parse.urlencode(data)
url = "http://bbs.guitarera.com/thread-2049-1-1.html"

content = funcs.crawlSinglePage(url);
# req = urllib.request.Request(url, headers = {
#     'Connection': 'Keep-Alive',
#     'Accept': 'text/html, application/xhtml+xml, */*',
#     'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
# })
# data = urllib.request.urlopen(req).read()
# data = data.decode('gbk')
#
#
#
#
# print(data)

# 打开文件
fo = open("test.md", "w+")
print ("文件名: ", fo.name)

line = fo.write(content)

fo.close()