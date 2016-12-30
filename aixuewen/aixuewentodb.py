# -*- coding:utf-8 -*-

import MySQLdb
import urllib2
import urllib
import re
import time
import sys
from bs4 import BeautifulSoup
import tool
import Mysql

class Spider(object):
    def __init__(self):
        self.URL = 'http://iask.sina.com.cn/c/187-all-1-new.html'
        #pageURllist存URL
        self.pageURllist = []
        #questiURllist
        self.questionsfullURL = []
        self.total_pagenum = None
        self.mysql = Mysql.Mysql()

    #得到某一页的内容
    def get_page(self,pageURL):
        request = urllib2.Request(pageURL)
        response = urllib2.urlopen(request)
        pagecontents = response.read().decode('utf-8')
        return pagecontents

    #得到目录有多少页
    def gettotalPageNum(self):
        pageURL = self.URL
        pagecontents = self.get_page(pageURL)
        pattern = re.compile(ur'<div class="pages"  pageCount="(.*?)".*?>', re.S)
        self.total_pagenum = re.search(pattern, pagecontents).group(1)
        return  True

    #在该页下得到所有问题的URL以及下一页的URL,pageURL为目录页的URL，num为该链接的位置在第几页
    def getquestionsURL(self,pageURL,num):
        pagecontents = self.get_page(pageURL)
        #得到问题的URL，存为questifullURL
        pattern = re.compile(r'<li class="list">.*?<div class="question-title">.*?<a href="(.*?)" target', re.S)
        questioninitalURl = re.findall(pattern, pagecontents)
        #print 'self.questionsfullURL插入问题的URL:'
        for URL in questioninitalURl:
            temURL = 'http://iask.sina.com.cn' + URL
            if temURL not in self.questionsfullURL:
                self.questionsfullURL.append(temURL)
                #print temURL

        #得到下一页的URL
        if num < int(self.total_pagenum):
            patternnextpage = re.compile(ur'<div class="pages".*?<a href=".*?" style=.*?>.*?</a>.*<a href="(.*?)" style="width: 65px">下一页</a>', re.S)
            nextpageURL = re.search(patternnextpage, pagecontents)
            if nextpageURL != None:
                tempageURL = 'http://iask.sina.com.cn/' + nextpageURL.group(1)
                if tempageURL not in self.pageURllist:
                    self.pageURllist.append(tempageURL)
                    print 'self.pageURllist插入第',str(num+1),'页的URL:' ,tempageURL
                    return True
            else:
                print '不能匹配到下一页URL'
                return False
        else:
            return True

    def get_questiondetail(self,questionurl):
        questioncontents =self.get_page(questionurl)
        #print '0'
        #问题
        patternquestion = re.compile(ur'<div class="question_text">.*?<pre style=.*?>(.*?)</pre>', re.S)
        question = re.search(patternquestion, questioncontents).group(1)
        #print '1'
        # 提问时间
        patterntime1 = re.compile(ur'<div class="ask_autho clearfix">.*<span class="ask-time mr10">(.*?)</span>', re.S)
        time1 = re.search(patterntime1, questioncontents).group(1)
        #print '2'
        #回答者
        patternanswerer = re.compile(ur'<div class="answer_tip clearfix">.*?<a href="(.*?)".*?>(.*?)</a>.*<span class="time mr10">(.*?)</span>', re.S)
        answer = re.search(patternanswerer, questioncontents)
        #print '3'
        if answer != None:
            answerURL = answer.group(1)
            answername = answer.group(2)
            answertime = answer.group(3)
            #回答内容
            pattern3 = re.compile(ur'<div class="answer_text">.*?<pre style=.*?">(.*?)</pre>', re.S)
            answercon = re.search(pattern3,questioncontents).group(1)
            ques_dict = {
                'question': question,
                'time': time1,
                'answerer': answername,
                'answererURL': answerURL,
                'answertime': answertime,
                'answertext': answercon,
                'questionURL': questionurl}
            insert_ID = self.mysql.insertData("iaskanswer",ques_dict)
            print '保存最佳答案成功,ID:',insert_ID
            #print question,time1,answername,answerURL,answertime,answercon,questionurl
            return True
        else:
            print '没有最佳答案，跳过此问题'
            return None

    def start(self):
        print '爬虫正在启动，开始爬取:',time.ctime()
        self.pageURllist.append(self.URL)
        self.gettotalPageNum()
        Totalpagenum = self.total_pagenum
        print '获取到目录共有' + str(Totalpagenum)+ '页:', time.ctime()
        for i in range(int(Totalpagenum)):
            print '开始读取第'+ str(i+1)+'页:', time.ctime()
            pageURL = self.pageURllist[i]
            if self.getquestionsURL(pageURL, i+1):
                print '这页读取完毕'
            else:
                break
        print '所有页都爬取完毕:', time.ctime(), '\n'

        print '开始爬取问题:' ,time.ctime()
        questionsnum = len(self.questionsfullURL)
        print '共有' + str(questionsnum)+ '问题:' ,time.ctime()
        for i in range(questionsnum):
            print '正在读取第' + str(i + 1) + '个问题:'
            temquestionURL = self.questionsfullURL[i]
            print temquestionURL
            self.get_questiondetail(temquestionURL)
        print '所有问题读取成功', time.ctime()
        print '正在结束爬虫...'
        print '爬虫结束：',time.ctime()
        return True

def main():
    #f_handler = open('out.log', 'w')
    #sys.stdout = f_handler
    spider = Spider()
    spider.start()

if __name__ == '__main__':
    main()
