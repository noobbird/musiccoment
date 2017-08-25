#_*_ coding: utf-8 _*_
#FileName: favor_singer.py
#Author: YMY
#History: 2017/8/20 1.0

from lxml import etree
import urllib
import re
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
import sys

def rank(file_name):
    f = file(file_name)
    d = pickle.load(f)
    word_in = {}
    album_stat = {}
    for k,v in d.items():
            #print k
            sum = 0
            count = 0
            album_stat[k] = {}
            for i,j in v.items():
                    name = i + ': ' + k
                    value = j
                    word_in[name] = value
                    #print '  ' + i + ' ' + str(j)
                    count += 1
                    sum += value
            album_stat[k]["sum"] = sum
            album_stat[k]["count"] = count
    sorted_dic = sorted(word_in.items(), lambda x,y:cmp(x[1], y[1]), reverse = True)
    print '****************单曲评论数排行****************'
    print '排名\t\t评论数' + '\t\t单曲名\n'
    single_limit = 20
    count = 0
    for i in sorted_dic:
            value = i[1]
            if value > 1000:
                    value /= 1000.0
                    value = '%.1fk' %value
            else:
                    value = str(value)
            if count < single_limit:
                    count += 1
                    single_name = i[0].split(':')[0]
                    album_name = i[0].split(':')[-1]
                    print str(count) + '\t\t' + value + '\t\t' + single_name+'\n' 
            else:
                    break


    print '****************专辑平均评论排行****************'
    print '单曲数\t平均评论数\t总评论数\t\t专辑名'
    for k, v in album_stat.items():
            if k.__contains__(u"演唱会"):
                    pass
            else:
                    ss = '%d\t%d\t\t%d\t\t%-20s' %( v['count'],v["sum"]/v["count"],v['sum'],k)
                    #print ss
                    #print 

    #path = "C:\Windows\Fonts\STSONG.TTF"
    #wordcloud = WordCloud(font_path = path,
                                                    # background_color = "white",
                                                    # width=1920,
                                                    # height=1080, 
                                                    # max_words=3200,
                                                    # relative_scaling=0.5,
                                                    # normalize_plurals=False).generate    _from_frequencies(word_in)
    # etree of the page
    #wordcloud.to_file("zhou.jpg")
    #plt.figure()
    #plt.imshow(wordcloud, interpolation="bilinear")
    #plt.axis("off")
    #plt.show()
if __name__ == '__main__':
    file_name = ''
    if len(sys.argv) > 1:
        file_name = sys.argv[1] + '.pick'
    else:
        file_name = u"王菲.pick"
    rank(file_name)
