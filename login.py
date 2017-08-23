# -*- coding:utf8 -*-
# FileName: netmusic.py
# Author: YMY
# Date: 2017/6/24
 
 
import urllib
import urllib2
import cookielib
import crypt
 
 
class MyWeb():
    def __init__(self):
        self.cookie_path = "cookie.txt"
        self.header = {
            'Host': 'music.163.com',
            'Content-Type': "application/x-www-form-urlencoded",
            'Referer': 'http://music.163.com',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
	    "Origin": "http://music.163.com"
		}
        self.cookie = cookielib.MozillaCookieJar(self.cookie_path)
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookie_support,
                                           urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
 
    def post(self, posturl, dictdata):
        """
        模拟post请求
 
        :param string posturl: url地址
        :param dict dictdata: 发送的数据
        """
 
        postdata = urllib.urlencode(dictdata)
        request = urllib2.Request(posturl, postdata, self.header)
        try:
            content = urllib2.urlopen(request)
            self.cookie.save(ignore_discard=True, ignore_expires=True)
            return content
        except Exception, e:
            print ("post:" + str(e))
            return None
 
    def get(self, url):
        """
        模拟get请求
 
        :param url: url地址
        :return content: 常使用read的方法来读取返回数据
        :rtype : instance or None
        """
        request = urllib2.Request(url, None, self.header)
        try:
            content = urllib2.urlopen(request)
            return content
        except Exception, e:
            print ("open:" + str(e))
            return None
    def get_cookie(self, name):
        for item in self.cookie:
            if item.name == name:
                return item.value
	

 
 
if __name__ == "__main__":
    import hashlib
    web = MyWeb()
    params = '{"phone":"18628909429","password":"058a6c8161c5abdf0367daff31d0bd19","rememberLogin":"true","csrf_token":""}'
    url = 'http://music.163.com/weapi/login/cellphone?csrf_token='
    data = crypt.get_postData(params)
    res = web.post(url, data)
    print res
    print web.get_cookie("__csrf");
	
