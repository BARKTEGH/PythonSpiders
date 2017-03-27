# -*- coding:utf-8 -*-
import os
import requests
import tool
from bs4 import BeautifulSoup
import urllib
'''
从顶点小说网下载小说，输入小说名novelname，得到novelname.txt文件
'''
URL = 'http://www.32xs.com/'
proxies = {
  "https": "http://115.54.83.107:8998"
}
class xiaoshuodownload(object):
    def __init__(self):
        self.url = URL
        self.novelname = ''
        self.menu  = ''
        self.chapterlistURL = [] # sava chaptelistURl
        self.tool= tool.Tool()
    def get_page(self,url):
        response = requests.post(url,proxies= proxies)
        return response.content

    #通过小说名得到该小说的index界面,是找到搜索界面的搜索到第一个小说
    def get_xiaoshuoURL(self):
        queryurl ='http://so.32xs.com/cse/search?q='+ self.novelname.encode('utf8')\
                  +'&click=1&entry=1&s=10214632002682711881&nsid='
        url = urllib.quote(queryurl,safe='/')
        resopnse = self.get_page(queryurl)
        soup = BeautifulSoup(resopnse,'html.parser')
        URLl = soup.find(cpos='title').get('href')
        novelname = soup.find(cpos='title').get('title')
        xiaoshuondexpage = URLl
        self.menu = xiaoshuondexpage.split('index')[0]
        return xiaoshuondexpage,novelname

    def get_xiaoshuomenuURL(self,indexURL):
        menupage = self.get_page(indexURL)
        soup = BeautifulSoup(menupage,'html.parser')
        chapterlist = soup.find(class_='chapterlist')
        for chapterURl in chapterlist.find_all('a'):
            chapterURL = chapterURl.get('href')
            chapterURL1 = self.menu + chapterURL
            self.chapterlistURL.append(chapterURL1)

    #通过chapterURl得到该章节的内容，返回title和小说章节内容
    def get_chaptercontent(self,chapterURl):
        chapterpage = self.get_page(chapterURl)
        soup = BeautifulSoup(chapterpage,'html.parser')
        title = soup.find('h1').string.encode('utf-8')
        chaptercontent = soup.find(id='BookText').get_text().encode('utf8')
        chaptercontent1 = self.tool.replace(chaptercontent)
        return chaptercontent1,title

    def run(self):
        self.novelname = raw_input('请输入小说名:').decode('utf8')
        #self.novelname = u'雪中悍刀行'
        xiaoshuopage,novelname1 = self.get_xiaoshuoURL()
        if novelname1 == self.novelname:
            print '在顶点小说网找到小说'
            print '开始爬取小说'
            print '小说目录界面：', xiaoshuopage
            filename = self.novelname + '.txt'
            f = open(self.novelname, 'w+')
            f.write(self.novelname.encode('utf8') + '\n')
            self.get_xiaoshuomenuURL(xiaoshuopage) # 得到小说章节目录的url
            for chapterURL in self.chapterlistURL:
                chaptercontent,chaptertitle = self.get_chaptercontent(chapterURL)
                print chaptertitle
                print chapterURL
                f.write(chaptertitle + '\n')
                f.write(chaptercontent + '\n')
                f.write('--------------------------' +'\n')
            f.close()
            print '小说下载完毕'
        else:
            print '未找到该小说，程序结束'

def main():
    xiaoshuo = xiaoshuodownload()
    xiaoshuo.run()

if __name__ == '__main__':
    main()
