#_*_coding: utf-8 _*_
#FileName: reqweb.py
#Author: yang
#History: 1#2017/8/24

import requests
import crypt
import json

headers = {
"host": "music.163.com",
"connection": "keep-alive",
"upgrade-insecure-requests": "1",
"user-agent": "mozilla/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/69.0.3497.100 safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"referer": "https://music.163.com/",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-cn,zh;q=0.9,en;q=0.8"
}

def post(posturl, dictdata, proxies = None, headers=headers):
        try:
            if proxies== None:
                r = requests.post(url=posturl, data=dictdata, timeout =2,headers=headers)
            else:
                r = requests.post(url=posturl, data=dictdata, proxies = proxies, timeout =2, headers=headers)
            return r
        except requests.exceptions.ConnectTimeout:
            print 'ConnectTimeout except'
        except requests.exceptions.ProxyError,e:
            print str(e)
        except requests.exceptions.ConnectionError,e:
            print str(e)
        except Exception,e:
            print str(e)
            return None
def get(url, proxies = None):
        try:
            if proxies == None:
                r = requests.get(url=url, timeout = 2,headers=headers)
            else:
                r = requests.get(url=url, proxies = proxies, timeout = 2,headers=headers)
            return r
        except Exception, e:
            print "get: " + str(e)
            return None

if __name__ == "__main__":
    song_id = "4154790"
    song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
    params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
    proxies = {"http": "http://47.52.24.117:80"}
    data = crypt.get_postData(params)
    res = post(song_url, data, proxies)
    comment_json = json.loads(res.text)
    print comment_json["total"]
    for c in comment_json["hotComments"]:
        print c["user"]["nickname"] + ': ' + c['content']
    print res.headers['X-From-Src'] 
