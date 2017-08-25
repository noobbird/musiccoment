#_*_ coding : utf-8 _*_
#FileName: getAlbum.py
#Author: YMY
#History: 2017/8/20 1.0

from lxml import etree
import urllib
import re
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
'''
'''

myid = "139721511"
url = 'http://music.163.com/playlist?id=%s' %myid

#get the favor list page:
def getPage(url):
    s = urllib.urlopen(url)
    return s.read()

# Get the first and the second song from the page
def getSong(url):
    page = getPage(url).decode('utf-8')
    json_string = re.search(">(\[.*\])<", page).group(1)
    res = json.loads(json_string)
    count = 0
    singers = {}
    for i in res:
        singer = i["artists"][0]["name"]
        if singers.get(singer) == None:
            singers[singer] = 1
        else:
            singers[singer] += 1
    sorted_dic = sorted(singers.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    for i in sorted_dic:
        print i[0] +" "+ str(i[1])    
    path = "./STSONG.TTF"
    wordcloud = WordCloud(font_path = path,
                            background_color = "white",
                            width=1920,
                            height=1080, 
                            max_words=1600,
                            relative_scaling=1,
                            normalize_plurals=False).generate_from_frequencies(singers)
    # etree of the page
    wordcloud.to_file("yang.jpg")
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    epage = etree.HTML(page)
    #titlePath = './/*/ul/li/a'
    #return (res[0].text,res[0].get('href'))
    return res

res = getSong(url)
