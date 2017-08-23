# -*- coding: cp936 -*-
#_*_ coding : utf-8 _*_
#FileName: Albumlist.py
#Author: YMY
#History: 2017/8/21

import urllib
import urllib2
import re
from lxml import etree
import album_songs
'''
得到歌手的专辑列表,调整limit来设置可能的最大专辑数法
'''

singer_id = "6452"
albumlist_url = "http://music.163.com/#/artist/album?id=%s&limit=100&offset=0" %singer_id

def getPage(url):
    s = urllib.urlopen(url)
    return s.read().decode('utf-8')

def getAlbumlist(url):
    page = getPage(url)
    title_path = ".//*[@id='m-song-module']/li/p/a"
    tree = etree.HTML(page)
    res = tree.xpath(title_path)
    return res

res = getAlbumlist(albumlist_url)
album_dict = {}
for e in res:
    album_dict[e.text] = e.get('href')
for (k,v) in album_dict.items():
    album_song_url = 'http://music.163.com/#%s' %v
    album_songs.getSonglist(album_song_url)
    
    
    
