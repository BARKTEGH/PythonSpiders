import requests
import urllib
from  bs4 import BeautifulSoup as bs
import sys,os,re,time
import copy
from lxml import etree
from importlib import reload
from proxy import *
import random
#from urllib3 import quote
#代理
proxies = []
for i in range(10):
    proxy = get_proxy()
    if proxy != None:
        proxies.append({'https':'https://'+proxy})

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer' : '******'}

def login_linkedin(laccount,lpassword):
    s = requests.Session()
    r = s.get('https://www.linkedin.com/uas/login',proxies=proxies,headers=headers)
    #print(r.content)
    tree = etree.HTML(r.content)
    loginCsrfParam = ''.join(tree.xpath('//input[@id="loginCsrfParam-login"]/@value'))
    csrfToken = ''.join(tree.xpath('//input[@id="csrfToken-login"]/@value'))
    sourceAlias = ''.join(tree.xpath('//input[@id="sourceAlias-login"]/@value'))
    isJsEnabled = ''.join(tree.xpath('//input[@name="isJsEnabled"]/@value'))
    source_app = ''.join(tree.xpath('//input[@name="source_app"]/@value'))
    tryCount = ''.join(tree.xpath('//input[@id="tryCount"]/@value'))
    clickedSuggestion = ''.join(tree.xpath('//input[@id="clickedSuggestion"]/@value'))
    signin = ''.join(tree.xpath('//input[@name="signin"]/@value'))
    session_redirect = ''.join(tree.xpath('//input[@name="session_redirect"]/@value'))
    trk = ''.join(tree.xpath('//input[@name="trk"]/@value'))
    fromEmail = ''.join(tree.xpath('//input[@name="fromEmail"]/@value'))

    payload = {
        'isJsEnabled': isJsEnabled,
        'source_app': source_app,
        'tryCount': tryCount,
        'clickedSuggestion': clickedSuggestion,
        'session_key': laccount,
        'session_password': lpassword,
        'signin': signin,
        'session_redirect': session_redirect,
        'trk': trk,
        'loginCsrfParam': loginCsrfParam,
        'fromEmail': fromEmail,
        'csrfToken': csrfToken,
        'sourceAlias': sourceAlias
    }
    s.post('https://www.linkedin.com/uas/login-submit', data=payload)
    return s

def search():
    pass

def get_person_main(person_id):
    base_url = 'https://www.linkedin.com/in/'
    url = base_url + person_id
    pass


if __name__ =='__main__':
    sess = login_linkedin('zgg2018gg@sina.com','4@<?5;\5')
    r  = sess.get('https://www.linkedin.com/search/results/index/?keywords=uestc')
    soup = bs(r.content,'lxml')