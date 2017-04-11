#! -*- coding:utf-8 -*-
'''
    使用request库进行模拟知乎登陆
    class zhihulogin 运行run,输入验证码，返回session和带有cookie的header,logger
    添加cookie保存，可以不用每次都要输入账号密码
'''
from bs4 import BeautifulSoup as BS
import json
import requests
import logging
import cookielib
import os
proxies = {
    "https": "http://116.28.206.126:8998",
    "https": "http://182.240.62.187:8998"
}
class zhihulogin(object):
    def __init__(self):
        self.url = 'https://www.zhihu.com/'
        self.account_name = None
        self.username = None
        self.password = None
        self._xsrf = None
        self.post_data = None
        self.session = requests.Session()
        self.cookies = 'temp/cookie.txt'
        self.session.cookies = cookielib.LWPCookieJar(filename=self.cookies)
        self.logger = self.createLogger('mylogger','temp/logger.log')
        # 请求的头内容
        self.header =  {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.zhihu.com/',
        'Accept-Language': 'en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        'Host': 'www.zhihu.com'
        }


    def get_parm(self):
        response = self.session.get(self.url,headers=self.header).content
        soup =BS(response,'html.parser')
        self._xsrf = soup.find('input', {'type': 'hidden'}).get('value')

    def get_account_password(self):
        username = raw_input('please input username: ')
        password = raw_input('please input password: ')
        account_name = None
        if '@' in self.username:
            self.account_name = 'email'
        else:
            self.account_name = 'phone_num'

    def get_captcha(self):
        captchaURL = r"https://www.zhihu.com/captcha.gif?type=login"
        picture = self.session.get(captchaURL,headers=self.header).content  # 用openr访问验证码地址,获取cookie
        local = open('temp/captcha.jpg', 'wb')
        local.write(picture)
        local.close()

    def creat_posrdata(self):
        self.post_data = {
            '_xsrf': self._xsrf,
            self.account_name: self.username,
            'password': self.password,
            'remember_me': 'true',
            'captcha':raw_input("Please input captcha: ")
        }
    def run(self):
        if not os.path.exists(self.cookies):
            self.get_parm()
            self.get_account_password()
            self.get_captcha()
            self.creat_posrdata()
            url = r"https://www.zhihu.com/login/" + self.account_name
            resText = self.session.post(url, data=self.post_data, headers=self.header).content.decode('utf8')
            jsonText = json.loads(resText)
            if jsonText["r"] == 0:
                '''
                # 把cookies添加到headers中
                cookies = self.session.cookies.get_dict()
                cookies = [key + "=" + value for key, value in cookies.items()]
                cookies = "; ".join(cookies)
                self.session.headers["Cookie"] = cookies
                '''
                self.session.cookies.save()
                self.logger.info("Login success!")
            else:
                self.logger.error("Login Failed!")
                self.logger.error("Error info ---> " + jsonText["msg"])
        else:
            # "从 cookie 文件加载上次的 cookie，这样就不需要重复登陆"
            r = self.session.cookies.load()
            self.logger.info("Login success!")
        return self.session,self.header,self.logger

    def createLogger(self, logger_name, log_file):
        # 创建一个logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 定义handler的输出格式formatter
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
 #运行实例

def main():
    zhihu = zhihulogin()
    session,headers,logger = zhihu.run()
    r = session.get('https://www.zhihu.com/',headers=headers,
                    timeout=10).content
    logger.info('开始')
    f=open('temp/home.html','w+')
    f.write(r)
    f.close()
if __name__ == '__main__':
    main()
