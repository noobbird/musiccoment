# -*- coding: cp936 -*-
#_*_ coding : utf-8 _*_
#FileName: song_comment.py
#Author: YMY
#History: 2017/8/22

import urllib
import urllib2
import json
import re
import crypt
from lxml import etree
'''
得到歌曲的评论
'''

song_id = "4154790"
song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
def post( posturl, dictdata):

	"""

	模拟post请求



	:param string posturl: url地址

	:param dict dictdata: 发送的数据

	"""



	postdata = urllib.urlencode(dictdata)

	request = urllib2.Request(posturl, postdata)

	try:

	    content = urllib2.urlopen(request)

	    return content

	except Exception, e:

	    print ("post:" + str(e))

	    return None



def get(url):

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

data = crypt.get_postData(params)
res = post(song_url, data)
print res.read()
comment_json = json.loads(res.read())
#print comment_json["total"]
for c in comment_json["hotComments"]:
    print c["user"]["nickname"] + ': ' + c['content']
    
    
