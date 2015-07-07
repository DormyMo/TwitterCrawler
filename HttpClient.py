#coding:utf8
__author__ = 'modm'
import random
import time
import requests
import sys
class HttpClient():
    def __init__(self,delayTime=5):
        self.userAgents =self._getUserAgents()
        self.proxys = self._getProxys()
        self.delayTime=delayTime
        pass
    def _getUserAgents(self):
        userAgents=[]
        with open('UserAgents.txt','r') as f:
            userAgents = f.readlines()
        f.close
        return [userAgent[:-1] for userAgent in userAgents]
    def _getProxys(self):
        proxies=[]
        with open('proxies.json','r')as f:
            line = f.read()
            json = eval(line)['proxies']
            for i in range(len(json)):
                for key in json[i]:
                    proxies.append({json[i][key]:key})
        f.close
        return  proxies
    def _getRadomStr(self,length):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt
    def _getRadomInt(self,length):
        seed = "1234567890"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return salt
    def get(self,url,params={}):
        proxy = random.choice(self.proxys)
        #proxy = {'https':'127.0.0.1:1080'}
        userAgent = random.choice(self.userAgents)
        print ' current proxy and ua is :',proxy,userAgent
        getParams=params
        #auth_token='b16790df749970256973d938fbc34d7c00762fc1'  #gmail
        #auth_token='066611A66A33C89A9CD4D44AECAB2240C3D54AC5' #126
        auth_token = '54d39c360953479df7fd9eed646c2423422e7dd8'
        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36",
                 "Accept-Encoding": "gzip, deflate, sdch",
                 "Accept-Language": "zh-CN,zh;q=0.8",
                 "Cookie": 'guest_id=v1:'+self._getRadomStr(18)+'; \
                            pid="v3:'+self._getRadomStr(25)+'"; \
                            external_referer='+self._getRadomStr(32)+'|0; \
                            remember_checked_on=0; twid="u='+self._getRadomInt(9)+'"; \
                            auth_token='+auth_token+'; \
                            lang=zh-cn; eu_cn=1; _ga=GA1.2.1492061373.1422871268; _gat=1; \
                            _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGiEvElLAToMY3NyZl9p%250AZCIlZTUyYzE5ZGYzNGY2YTI5ZGY3M2IxOTdiMDkyYTRmYWM6B2lkIiU0ZDRm%250ANDY4OTNmYjdmYWNiMjJiMDc3YjAwMzFlY2Q2MjoJdXNlcmkEfhqjFA%253D%253D--337dd84539fd236e2b874ecd2fe9d0e8b7cd4f95',
                            "User-Agent" : userAgent}
        try:
            waitTime = random.randint(0,self.delayTime)
            print 'waitTime : ',waitTime
            time.sleep(waitTime)
            print 'http requests ing ... ',url
            res = requests.get(url,proxies=proxy,params=getParams,headers=headers,verify=False,timeout=30,allow_redirects=False)
            print 'http requests done ... ',url
        except Exception,e:
            print sys.stderr.write('http requests err : '+str(e))
            raise Exception('my http requests err',e)
        return res

