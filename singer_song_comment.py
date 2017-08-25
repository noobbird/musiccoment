#_*_ coding: utf-8 _*_
#FileName: singer_song_comment
#Author: YMY
#History: 2017/8/22

import sys
from time import ctime, sleep
import urllib
import reqweb
import random
from lxml import etree
import crypt
import myweb
import json
from threading import Thread, Lock
from atexit import register
import pickle

gd = {}
singer_name = ['n']
web = myweb.MyWeb()

def path_filter(page, path):
    tree = etree.HTML(page)
    res = tree.xpath(path)
    return res

def is_exclude_album(name):
    if name.__contains__(u"演唱会") or\
        name.__contains__("live") or\
        name.__contains__(u'音乐会')or\
        name.__contains__("Live"):
        return True
    else:
        return False

def get_albums(singer_id):
    singer_albumlist_url = 'http://music.163.com/artist/album?id=%s&limit=120&offset=0'
    url = singer_albumlist_url %singer_id
    path = ".//*[@id='m-song-module']/li/p/a"
    singer_name_path = ".//h2[@id='artist-name']"
    response = reqweb.get(url)
    res = path_filter(response.text, path) 
    singer_name[0] = path_filter(response.text, singer_name_path)[0].text
    print u'歌手: ' + singer_name[0]
    album_dict = {}
    for e in res:
        name = e.text
        value = e.get('href').split('=')[-1]
        if is_exclude_album(name):
            print "exclutde: " + name
        else:
            album_dict[name] = value
    return album_dict

def get_songs(album_id):
    album_songlist_url = "http://music.163.com/album?id=%s" 
    url = album_songlist_url %album_id
    title_path = ".//ul[@class='f-hide']/li/a"
    response = reqweb.get(url)
    res = path_filter(response.text, title_path)
    song_dict = {}
    for e in res:
        song_dict[e.text] = e.get('href').split('=')[-1]
    return song_dict

def get_song_comment(song_id,proxy = None):
    song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
    params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
    data = crypt.get_postData(params)
    res = reqweb.post(song_url, data, proxy)
    if res == None:
        return None
    else:
        try:
            comment = json.loads(res.text)
            return comment
        except Exception, e:
            print str(e)
            return None

def album_thread(song_dict, album):
    song_dict = get_songs(v)
    for i,j in song_dict.items():
        count = get_song_comment(j)['total']
        name = i 
	gd[name] = count        
	print name +' ' + str(count)

def get_all_songs(singer_id):
    res_dict = {}
    albums_dict = get_albums(singer_id)
    print '专辑数: ' + str(len(albums_dict))
    if not albums_dict:
        print 'get baned'
        return None
    for k,v in albums_dict.items():
        song_dict = get_songs(v)
        tmp = {}
        for i,j  in song_dict.items():
            tmp[i] = j
            print i,j
        sleep(2)
        res_dict[k] = tmp
        tmp = {}
    return res_dict
      
if __name__ == "__main__":
    albums_dict = get_albums(sys.argv[1])
    if not albums_dict:
        print "baned"
    else:
        print u'专辑数: ' + str(len(albums_dict))
    song_comment_dict = {}
    proxies_pick = file("proxy.pick")
    proxies = pickle.load(proxies_pick)
    lenp = len(proxies)
    index = 0
    proxy_count_dict = {}
    proxy_count_dict[index] = 0
    proxy_stat = {}
    isbaned = False
    print "At", ctime(), "start get..."
    if len(sys.argv) > 1 and sys.argv[1] == 3:
        for k,v in albums_dict.items():
            t = Thread(target = album_thread, args=(v,k))
            t.start()
            t.join()
    else:
        for k,v in albums_dict.items():
            song_dict = get_songs(v)
            tmp = {}
            print k
            for i,j  in song_dict.items():
                name = i
                if not isbaned:
                    song_comment = get_song_comment(j)
                    isbaned = True
                if not song_comment:
                    isbaned = True
                song_comment = None
                while song_comment == None:
                    proxy = {"http":"http://"+proxies[index%lenp]}
                    song_comment = get_song_comment(j, proxy)                 
                    #print proxy_count_dict[index]
                    if not song_comment or proxy_count_dict[index] > 20:
                        proxy_count_dict[index] = 0
                        index = (index+1)%lenp
                        proxy_count_dict[index] = 0
                        print 'System: proxy is changed to ' + proxies[index]
                    else:
                        proxy_count_dict[index] += 1
                value = song_comment['total'] 
                tmp[name] = value
                print '\t' + name +' ' + str(value)
                sleep(1)
            gd[k] = tmp
            tmp = {}

    fname = singer_name[0] + '.pick'
    output = open(fname,"wb")
    pickle.dump(gd,output)
@register
def _atexit():
    print 'all DONE at:', ctime()
