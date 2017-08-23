# -*- coding:utf8 -*-

# FileName: myweb.py

# Author: YMY

# Date: 2017/8/20

 

 

import urllib

import urllib2

import crypt

 

 

class MyWeb():

    def __init__(self, header = None):

        self.header = header

 

    def post(self, posturl, dictdata):

        """

        模拟post请求

 

        :param string posturl: url地址

        :param dict dictdata: 发送的数据

        """

 

        postdata = urllib.urlencode(dictdata)
        if self.header == None:
            request = urllib2.Request(posturl, postdata)
        else:
            request = urllib2.Request(posturl, postdata, self.header)

        try:

            content = urllib2.urlopen(request, timeout = 2)

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

        if self.header == None:
            request = urllib2.Request(url, None)
        else:
            request = urllib2.Request(url, None, self.header)

 
        try:

            content = urllib2.urlopen(request, timeout = 2)

            return content

        except Exception, e:

            print ("open:" + str(e))

            return None
if __name__ == "__main__":
    print MyWeb().get("http://www.baidu.com").read() 



 
