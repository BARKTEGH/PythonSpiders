# coding:utf-8
import logging
import os
import re
import time
'''
python2会出现ascii无法decode成utf-8，因为str是以ascii存储，
导致无法识别pdfname出现问题
pdfkit.from_file(htmls, pdfname, options=options,configuration=config)

只需要改变廖雪峰class类，就可以爬取其他教程
'''

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""
proxies = {
  "https": "http://115.54.83.107:8998"
}

class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name,start_url):
        """
        初始化
        :param name: 保存问的PDF文件名,不需要后缀名
        :param start_url: 爬虫入口URL
        """
        self.name = name
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url))

    def crawl(self, url):
        """
        pass
        :return:
        """
        response = requests.get(url,proxies= proxies)
        return response

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表:由子类实现
        :param response 爬虫返回的response对象
        :return: url 可迭代对象(iterable) 列表,生成器,元组都可以
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html文本
        """
        raise NotImplementedError

    def run(self):
        start = time.time()

        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }

        f = open('a.html','wb')
        for index, url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            html = self.parse_body(self.crawl(url)).encode('utf-8')
            f.write(html)
        f.close()
        print '开始读入html,转为pdf'
        config = pdfkit.configuration(wkhtmltopdf= 'F:/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdfname = self.name + '.pdf'
        pdfkit.from_file('a.html', pdfname, options=options,configuration=config)
        os.remove('a.html')
        total_time = time.time() - start
        print "总共耗时：%f 秒" % total_time


class LiaoxuefengPythonCrawler(Crawler):
    """
    廖雪峰Python3教程
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
        for li in menu_tag.find_all("li"):
            url = li.a.get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])  # 补全为全路径
            yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_="x-wiki-content")[0]

            # 加入标题, 居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(3).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)

class cuiqingcaiCrawler(Crawler):

    def parse_menu(self, response):
        soup =BeautifulSoup(response.content,'html.parser')
        menu = soup.find(class_ ='article-content')
        for title in menu.find_all('a'):
            url = title.get('href')
            print url
            if url not in ['http://cuiqingcai.com','http://cuiqingcai.com/1052.html','javascript:;']:
                yield  url
            else:
                break


    def parse_body(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find(class_="article-content")
            # 加入标题, 居中显示
            title = soup.find('h1').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(3).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html.decode('utf-8')
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)








if __name__ == '__main__':
    start_url = "http://cuiqingcai.com/1052.html"
    crawler = cuiqingcaiCrawler('crawel', start_url)
    crawler.run()
