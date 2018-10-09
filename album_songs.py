#_*_ coding: utf-8 _*_
#FileName: album_songs.py
#Author: YMY
#History: 2017/8/21

import urllib
import urllib2
import requests
import models
import json
import re
from lxml import etree

album_id = "34720827"
album_songs_url = "http://music.163.com/album?id=%s" %album_id

def getPage(url):
    #s = urllib.urlopen(url)
    #return s.read().decode('utf-8')
    proxy = {'http':"http://184.185.166.27:8080"}
    return requests.get(url,proxies=proxy).text

def getSonglist(url):
    page = getPage(url)
    title_path = ".//ul[@class='f-hide']/li/a"
    description_path = ".//meta[@name='description']"
    song_path = './/div[@id="song-list-pre-cache"]/textarea'
    tree = etree.HTML(page)
    des = tree.xpath(description_path)
    #return des[0].get('content')
    res = tree.xpath(title_path)
    songs = tree.xpath(song_path)
    song_json = json.loads(songs[0].text)
    count = 0
    for e in song_json:
        song = models.Song()
        song.song_name = e["name"]
        song.song_id = e["id"]
        song.duration = e["duration"]
        song.comment_thread = e["commentThreadId"]
        artists = e["artists"]
        album = e["album"]
        song.album_id = album["id"]
        song.album_name = album["name"]
        artist_id = ''
        artist_name = ''
        artist_id ='/'.join([str(i["id"]) for i in artists])
        artist_name = '/'.join([i['name'] for i in artists])
        song.artist_name = artist_name
        song.artist_id = artist_id
        models.db.rollback()
        if count%2==0:
            song.save()
        count +=1
        print artist_id + '\t' + artist_name
    for e in res:
        #print e.text +' ' + e.get('href')
        pass
    return res
if __name__ == '__main__':
    r = getSonglist(album_songs_url)
    #l = r.split(u'。')
    #sname = l[0].split(u'：')[-1]
    #date = l[1].split(u'：')[-1]
    #cop =  l[2].split(u'：')[-1]
    #des = ''.join(l[3:-1])
    #print des
    #album = models.Album(aid = album_id,\
    #                    singer = sname,\
    #                    name = 'ss',\
    #                    release_date = date,\
    #                    publisher = cop,\
    #                    description = des)
    #album = models.Album()
    #album.aid = '123'
    #album.singer = 'me'
    #album.name = 'secret'
    #album.release_date = '1995-9-3'
    #album.description = 'hh'
    #album.publisher = 'ms'
    #album.save()
    #album.save()

                        
