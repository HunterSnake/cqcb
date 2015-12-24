# -*- coding: utf-8 -*-
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class spider(object):
    def __init__(self):
        print u'开始爬取内容。。。'

    # getsource用来获取网页源代码
    def getsource(self, url):
        html = requests.get(url)
        html.encoding = 'gb2312'
        return html.text

    # changepage用来生产不同页数的链接
    def changepage(self, url, total_page):
        now_page = int(re.search('list_(\d+)\.htm', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page + 1):
            link = re.sub('list_\d+', 'list_%s' % i, url, re.S)
            page_group.append(link)
        return page_group

    # getContent用来抓取内容块的信息
    def getContent(self, source):
        content = re.search('<table width="94%" border="1" align="center" cellpadding="0" cellspacing="0" class="table-line">(.*?)</table>', source, re.S).group(1)
        return content

    def getLinkContent(self, content):
        everyclass = re.findall('<td  height="22" class="pad-left">(.*?)<br></td>', content, re.S)
        return everyclass

    # getinfo用来从每个链接块中提取出我们需要的信息
    def getinfo(self, linkContent):
        info = {}
        info['title'] = re.search('target="_blank">(.*?)</a>', linkContent, re.S).group(1)
        info['link'] = re.search('href="(.*?)"', linkContent, re.S).group(1)
        info['date'] = re.search('color=#999999>(.*?)</font>', linkContent, re.S).group(1)
        return info

    # saveinfo用来保存结果到info.txt文件中
    def saveinfo(self, classinfo):
        f = open('titles.txt', 'a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('link:' + each['link'] + '\n')
            f.writelines('date:' + each['date'] + '\n')
        f.close()


if __name__ == '__main__':
    classinfo = []
    url = 'http://www.cqcb.net/cqcb_net/news/list_1.htm'
    newsSpider = spider()
    all_links = newsSpider.changepage(url, 8)
    for link in all_links:
        print u'正在处理页面：' + link
        html = newsSpider.getsource(link)
        content = newsSpider.getContent(html)
        everyNews = newsSpider.getLinkContent(content)
        for each in everyNews:
            info = newsSpider.getinfo(each)
            classinfo.append(info)
    newsSpider.saveinfo(classinfo)
