# -*- coding: utf-8 -*-
import requests
import re
import sys
import torndb
import os

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

    #抓取每个文章的相关链接块
    def getLinkContent(self, content):
        linkcontent = re.findall('<td  height="22" class="pad-left">(.*?)<br></td>', content, re.S)
        return linkcontent

    # getinfo用来从每个链接块中提取出我们需要的信息
    def getinfo(self, typeId, linkContent):
        # info = {}
        # info['title'] = re.search('target="_blank">(.*?)</a>', linkContent, re.S).group(1)
        # info['link'] = re.search('href="(.*?)"', linkContent, re.S).group(1)
        # info['date'] = re.search('color=#999999>(.*?)</font>', linkContent, re.S).group(1)
        # return info
        info = (typeId, re.search('target="_blank">(.*?)</a>', linkContent, re.S).group(1),re.search('href="(.*?)"', linkContent, re.S).group(1))
        return info

    # saveinfo用来保存结果到info.txt文件中
    def saveinfo(self, folder, classinfo):
        if os.path.isdir('./' + folder):
            print 'folder exists'
        else:
            os.mkdir('./' + folder)
            print 'create folder: ' + folder
        f = open('./' + folder + '/titles.txt', 'a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('link:' + each['link'] + '\n')
            f.writelines('date:' + each['date'] + '\n')
            f.writelines('-'*38 + '\n')
        f.close()

if __name__ == '__main__':
    sql = ('select s.*, t.dest_folder from tb_sources s inner join tb_page_type t on s.typeId = t.id where spiderFlag=false;')
    sql_insert = 'INSERT INTO `tb_titles` (`typeId`,`title`,`link`) VALUES (%s, %s, %s)'
    sql_update = 'update tb_sources set spiderFlag=true where id=%s'
    import torndb

    db2 = torndb.Connection(
        host='localhost',
        database='cqcb',
        user='root',
        password='1',
        charset='utf8'
    )
    rows = db2.query(sql)
    for row in rows:
        print(row['firstpageurl'])
        classinfo = []
        newsSpider = spider()
        all_links = newsSpider.changepage(row['firstpageurl'], row['pagecount'])
        for link in all_links:
            print u'正在处理页面：' + link
            html = newsSpider.getsource(link)
            content = newsSpider.getContent(html)
            everyNews = newsSpider.getLinkContent(content)
            for each in everyNews:
                info = newsSpider.getinfo(row['typeId'], each)
                classinfo.append(info)
        #newsSpider.saveinfo(row['dest_folder'], classinfo)
        db2.insertmany(sql_insert, classinfo)
        db2.update(sql_update, row['id'])
        print u'源%s处理完毕：'%row['dest_folder']
