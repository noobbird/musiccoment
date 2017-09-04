#_*_ coding: utf-8 _*_
#FileName: singer_song_comment
#Author: YMY
#History: 2017/8/22

import sys
from time import ctime, sleep, time
import cloudoffile
import threading
import urllib
import Queue
import reqweb
import random
from lxml import etree
import crypt
import json
from threading import Thread, Lock
from atexit import register
import pickle
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8') 

#all album and song
gd = {}
singer_name = ['n']
pqueue = Queue.Queue()
queue = Queue.Queue()
global_proxies = []
proxy_stat = {}

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
    singer_albumlist_url = 'http://music.163.com/artist/album?id=%s&limit=50000&offset=0'
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

def get_songs(album_id,proxy=None):
    album_songlist_url = "http://music.163.com/album?id=%s" 
    url = album_songlist_url %album_id
    title_path = ".//ul[@class='f-hide']/li/a"
    response = reqweb.get(url,proxy)
    if not response:
        return None
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
            #print 'get_song_comment: ' + str(e)
            return None

def album_thread():
    while not queue.empty():
        album_tuple = queue.get()
        song_dict = get_songs(album_tuple[1])
        while song_dict == None:
                tp1 = pqueue.get()
                proxy = {"http":"http://"+tp1}
                song_dict= get_songs(album_tuple[1], proxy)
                if not song_dict:
                    proxy_stat[tp1] += 1                
                pqueue.put(tp1)

        k = album_tuple[0]
        tmp = {}
        print k
        for i,j  in song_dict.items():
            name = i
            song_comment = None
            while song_comment == None:
                tp = pqueue.get()
                proxy = {"http":"http://"+tp}
                song_comment = get_song_comment(j, proxy)                 
                if not song_comment:
                    proxy_stat[tp] += 1
                pqueue.put(tp)
            value = song_comment['total'] 
            tmp[name] = value
            print '\t' + name +' ' + str(value)
            sleep(1)
        gd[k] = tmp
        tmp = {}
        queue.task_done()

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
      
def put_data_in_queue(albums, proxies):
    for k,v in albums.items():
        queue.put((k,v))
    for p  in proxies:
        pqueue.put(p)

def init_proxy_stat_dict(proxies):
    stat_dict = {}
    for i in proxies:
        stat_dict[i] = 0
    return stat_dict
    
if __name__ == "__main__":
    albums_dict = get_albums(sys.argv[1])
    if not albums_dict:
        print "baned"
    else:
        print u'专辑数: ' + str(len(albums_dict))
    single_thread = False
    song_comment_dict = {}
    proxies_pick = file("proxy.pick")
    proxies = pickle.load(proxies_pick)
    lenp = len(proxies)
    index = 0
    proxy_count_dict = {}
    proxy_count_dict[index] = 0
    proxy_stat = init_proxy_stat_dict(proxies)
    isbaned = False
    print "At", ctime(), "start get..."
    start_time = time()
    if not single_thread:
        put_data_in_queue(albums_dict,proxies)
        threads_nums = 6
        for i in xrange(threads_nums):
            t = threading.Thread(target = album_thread)
            t.setDaemon(True)
            t.start()
        queue.join()
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
    #count songs
    song_sum = 0
    for k,v in gd.items():
         song_sum += len(v)
    print 'song count: %d'%song_sum
    end_time = time()
    total_time = int(end_time - start_time)
    print 'total time: %dmin %ds' %(total_time/60, total_time%60)
    try:
        f = open('time_stat.txt', 'a')
        line = singer_name[0]+ ' '+ str(song_sum)+' '+ str(total_time)+\
' ' + str(single_thread)+'\n'
        f.write(line)
    except Exception,e:
        print 'write time stat' +str(e)
    finally:
        f.close()
    #print '\n代理失败次数统计\n'
    #for k,v in proxy_stat.items():
    #    print k + ': ' + str(v)
    fname = singer_name[0] + '.pick'
    output = open(fname,"wb")
    pickle.dump(gd,output)
    output.close()
    cloudoffile.rank(fname)
@register
def _atexit():
    print 'all DONE at:', ctime()
