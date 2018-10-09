#_*_coding: utf-8 _*_
#FileName: reqweb.py
#Author: yang
#History: 1#2017/8/24

import requests
import crypt
import json
import sys

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
<<<<<<< HEAD
            if proxies== None:
                r = requests.post(url=posturl, data=dictdata, timeout =2,headers=headers)
=======
            if proxies is None:
                r = requests.post(url=posturl, data=dictdata, timeout =2)
>>>>>>> 77e095be23a01042e606b53e66bcd965ede325ab
            else:
                r = requests.post(url=posturl, data=dictdata, proxies = proxies, timeout =2, headers=headers)
            return r
        except requests.exceptions.ConnectTimeout:
            sys.stderr.write('post ConnectTimeout except\n')
        except requests.exceptions.ProxyError,e:
            sys.stderr.write('post ProxyError\n')
        except requests.exceptions.ConnectionError,e:
            sys.stderr.write('post ConnectionError\n')
        except Exception,e:
            sys.stderr.write('post '+str(e))


def get(url, proxies = None):
        try:
<<<<<<< HEAD
            if proxies == None:
                r = requests.get(url=url, timeout = 2,headers=headers)
=======
            if proxies is None:
                r = requests.get(url=url, timeout = 2)
>>>>>>> 77e095be23a01042e606b53e66bcd965ede325ab
            else:
                r = requests.get(url=url, proxies = proxies, timeout = 2,headers=headers)
            return r
        except requests.exceptions.ConnectTimeout:
            sys.stderr.write('get ConnectTimeout except\n')
        except requests.exceptions.ProxyError, e:
            sys.stderr.write('get ProxyError\n')
        except requests.exceptions.ConnectionError, e:
            sys.stderr.write('get ConnectionError\n')
        except Exception, e:
            sys.stderr.write('get' + str(e))

if __name__ == "__main__":
    song_id = "4154790"
    song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
    params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
    proxies = {"http": "http://47.52.24.117:80"}
    data = crypt.get_postData(params)
<<<<<<< HEAD
    res = post(song_url, data, proxies)
=======
    res = post(song_url, data)
>>>>>>> 77e095be23a01042e606b53e66bcd965ede325ab
    comment_json = json.loads(res.text)
    print comment_json["total"]
    for h in comment_json["hotComments"]:
        content = h['content']
        commentId = h['commentId']
        likedCount = h['likedCount']
        time = h['time']
        replied = h['beReplied']
        rep = ''
        user= h['user']
        user_name = user['nickname']
        user_id = user['userId']
        user_avatar = user['avatarUrl']
        if replied:
            rep = replied[0]['content']
        
        print '\trep: ' + rep +'\ncontent' + content
        print 'user: '+user_name+'\t'+str(user_id)+'\t'+user_avatar+str(likedCount)
        
    #for c in comment_json["hotcomments"]:
    #    print c["user"]["nickname"] + ': ' + c['content']
    print res.headers['X-From-Src'] 
