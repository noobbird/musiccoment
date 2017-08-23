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

def get_albums(singer_id):
    singer_albumlist_url = 'http://music.163.com/#/artist/album?id=%s&limit=100&offset=0'
    path = ".//*[@id='m-song-module']/li/p/a"
    res = get_path_obj(singer_albumlist_url, singer_id, path)
    album_dict = {}
    for e in res:
        album_dict[e.text] = e.get('href').split('=')[-1]
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
    return json.loads(res.read())
def album_thread(song_dict, album):
    song_dict = get_songs(v)
    for i,j in song_dict.items():
        count = get_song_comment(j)['total']
        name = i + ': ' + album
	gd[name] = count        
	print name +' ' + str(count)


if __name__ == "__main__":
    albums_dict = get_albums("6452")
    song_comment_dict = {}
    print "At", ctime(), "start get..."
    if sys.argv[1] == 2:
        for k,v in albums_dict.items():
            t = Thread(target = album_thread, args=(v,k))
            t.start()
            t.join()
    else:
        for k,v in albums_dict.items():
            song_dict = get_songs(v)
            for i,j  in song_dict.items():
                count = get_song_comment(j)['total']
                name = i + ': ' + k
                gd[name] = count
                print name +' ' + str(count)

    output = open("z.pick","wb")
    pickle.dump(gd,output)
@register
def _atexit():
    print 'all DONE at:', ctime()
