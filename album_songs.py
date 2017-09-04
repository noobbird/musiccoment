#_*_ coding: utf-8 _*_
#FileName: album_songs.py
#Author: YMY
#History: 2017/8/21

import urllib
import urllib2
import requests
import models
import re
from lxml import etree

album_id = "2489195"
album_songs_url = "http://music.163.com/album?id=%s" %album_id

def getPage(url):
    #s = urllib.urlopen(url)
    #return s.read().decode('utf-8')
    return requests.get(url).text

def getSonglist(url):
    page = getPage(url)
    title_path = ".//ul[@class='f-hide']/li/a"
    description_path = ".//meta[@name='description']"
    tree = etree.HTML(page)
    des = tree.xpath(description_path)
    return des[0].get('content')
    res = tree.xpath(title_path)
    for e in res:
        #print e.text +' ' + e.get('href')
        pass
    return res
if __name__ == '__main__':
    r = getSonglist(album_songs_url)
    l = r.split(u'。')
    sname = l[0].split(u'：')[-1]
    date = l[1].split(u'：')[-1]
    cop =  l[2].split(u'：')[-1]
    des =  l[3]
    album = models.Album(aid = album_id,\
                        singer = sname,\
                        name = 'ss',\
                        release_date = date,\
                        publisher = cop,\
                        description = des)
    album.save()

                        
