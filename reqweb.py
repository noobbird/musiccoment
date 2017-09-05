#_*_coding: utf-8 _*_
#FileName: reqweb.py
#Author: yang
#History: 1#2017/8/24

import requests
import crypt
import json

def post(posturl, dictdata, proxies = None):
        try:
            if proxies== None:
                r = requests.post(url=posturl, data=dictdata, timeout =2)
            else:
                r = requests.post(url=posturl, data=dictdata, proxies = proxies, timeout =2)
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
                r = requests.get(url=url, timeout = 2)
            else:
                r = requests.get(url=url, proxies = proxies, timeout = 2)
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
    res = post(song_url, data)
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
