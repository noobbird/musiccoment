# -*- coding: cp936 -*-
#_*_ coding : utf-8 _*_
#FileName: album_songs.py
#Author: YMY
#History: 2017/8/21

import urllib
import urllib2
import re
from lxml import etree
'''
�õ����ֵ�ר���б�,����limit�����ÿ��ܵ����ר����
'''

album_id = "2489195"
album_songs_url = "http://music.163.com/#/album?id=%s" %album_id

def getPage(url):
    s = urllib.urlopen(url)
    return s.read().decode('utf-8')

def getSonglist(url):
    page = getPage(url)
    title_path = ".//ul[@class='f-hide']/li/a"
    tree = etree.HTML(page)
    res = tree.xpath(title_path)
    for e in res:
        print e.text +' ' + e.get('href')
    return res
    
    
    
