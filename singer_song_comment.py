#_*_ coding: utf-8 _*_
#FileName: singer_song_comment
#Author: YMY
#History: 2017/8/22

import sys
from time import ctime, sleep
import urllib
from lxml import etree
import crypt
import myweb
import json
from threading import Thread, Lock
from atexit import register
import pickle
gd = {}
web = myweb.MyWeb()
def getPage(url):
    s = urllib.urlopen(url)
    return s.read().decode('utf-8')

def path_filter(page, path):
    tree = etree.HTML(page)
    res = tree.xpath(path)
    return res

def get_path_obj(url, uid, xpath):
	url = url %uid
	page = getPage(url)
	return path_filter(page, xpath)

def is_exclude_album(name):
    if name.__contains__(u"演唱会") or\
        name.__contains__("live") or\
        name.__contains__("Live"):
        return True
    else:
        return False

def get_albums(singer_id):
    singer_albumlist_url = 'http://music.163.com/#/artist/album?id=%s&limit=120&offset=0'
    path = ".//*[@id='m-song-module']/li/p/a"
    res = get_path_obj(singer_albumlist_url, singer_id, path)
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
    album_songlist_url = "http://music.163.com/#/album?id=%s" 
    title_path = ".//ul[@class='f-hide']/li/a"
    res = get_path_obj(album_songlist_url, album_id, title_path)
    song_dict = {}
    for e in res:
        song_dict[e.text] = e.get('href').split('=')[-1]
    return song_dict

def get_song_comment(song_id):
    song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
    params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
    data = crypt.get_postData(params)
    res = web.post(song_url, data)
    if res == None:
        return None
    else:
        return json.loads(res.read())
def album_thread(song_dict, album):
    song_dict = get_songs(v)
    for i,j in song_dict.items():
        count = get_song_comment(j)['total']
        name = i 
	gd[name] = count        
	print name +' ' + str(count)


if __name__ == "__main__":
    albums_dict = get_albums("6452")
    song_comment_dict = {}
    print "At", ctime(), "start get..."
    if len(sys.argv) > 1 and sys.argv[1] == 2:
        for k,v in albums_dict.items():
            t = Thread(target = album_thread, args=(v,k))
            t.start()
            t.join()
    else:
        for k,v in albums_dict.items():
            song_dict = get_songs(v)
            tmp = {}
            for i,j  in song_dict.items():
                name = i
                song_comment = get_song_comment(j)
                if song_comment == None:
                    print "get " + name + " fail"
                    continue
                else:
                    value = get_song_comment(j)['total']
                tmp[name] = value
                print name +' ' + str(value)
                sleep(1)
            gd[k] = tmp
            tmp = {}

    output = open("z.pick","wb")
    pickle.dump(gd,output)
@register
def _atexit():
    print 'all DONE at:', ctime()
