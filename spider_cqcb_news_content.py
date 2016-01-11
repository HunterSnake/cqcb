#-*-coding:utf8-*-
import re
import requests
import time
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def spider(url):
    info = {}
    file = re.search('(\d+\.htm)', url).group(1)
    print file
    info["file"] = file
    html = requests.get("http://www.cqcb.net/cqcb_net/news/" + url)
    html.encoding = 'gb2312'
    selector = etree.HTML(html.text)
    title = selector.xpath("//strong[@class='title']/text()")[0]
    print title
    info["title"] = title
    time = selector.xpath("//td[@align='center']/text()")[0]
    print time
    time = re.search('(\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}\:\d{1,2}\:\d{1,2})', time, re.S).group(1)
    print time

    info["time"] = time
    content = re.search('<td height="200" valign="top">(.*?)</td>', html.text, re.S).group(1)
    pic_url = re.findall('src="/editor/(.*?)"',content,re.S)
    for each in pic_url:
        img = re.search('(\d+\.jpg)', each).group(1)
        print 'now downloading:' + img
        pic = requests.get("http://www.cqcb.net/editor/" + each)
        fp = open('./News/pics/' + img,'wb')
        fp.write(pic.content)
        fp.close()
        content = re.sub('src="/editor/'+each+'"','src="pics/%s"'%img, content)
    fhtml = open('./News/' + file,'w')
    fhtml.writelines(content)
    fhtml.close()


    hit = requests.get("http://www.cqcb.net/hit.asp?hit="+file)
    hit = re.search('(\d+)</font>', hit.text).group(1)
    print hit
    info["hit"] = hit
    newsInfos.append(info)


if __name__ == '__main__':
    timebegin = time.time()
    f = open('./News/titles.txt','r')
    fileContent = f.read()
    f.close()
    pool = ThreadPool(4)
    url = re.findall('link:(.*?htm)',fileContent)
    print len(url)
    newsInfos = []

    pool = ThreadPool(4)
    results = pool.map(spider, url)
    pool.close()
    pool.join()


    # for u in url:
    #     spider(u)
    #

    f = open('./News/newsinfo.txt', 'w')
    for each in newsInfos:
        f.writelines('title:' + each['title'] + '\n')
        f.writelines('file:' + each['file'] + '\n')
        f.writelines('time:' + each['time'] + '\n')
        f.writelines('hit:' + each['hit'] + '\n')
        f.writelines('------------------------------' '\n')
    f.close()
    timeend = time.time()
    print u'抓取完毕,共耗时：' + str(timeend-timebegin)
