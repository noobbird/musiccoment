#_*_ coding: utf-8 _*_
#FileName: singer_song_comment
#Author: YMY
#History: 2017/8/22

import sys
from time import ctime, sleep, time
import cloudoffile
import threading
import models
import urllib
import Queue
import reqweb
import random
from lxml import etree
import crypt
import json
from threading import Thread, Lock
import pickle
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8') 

#all album and song
gd = {}
singer_name = ['n']
pqueue = Queue.Queue()
queue = Queue.Queue()
use_stat = {}
fail_stat = {}
L = Lock()
singer_set = set()


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


def get_albums(singer_id,proxy=None):
    singer_albumlist_url = 'http://music.163.com/artist/album?id=%s&limit=50000&offset=0'
    url = singer_albumlist_url %singer_id
    path = ".//*[@id='m-song-module']/li/p/a"
    singer_name_path = ".//h2[@id='artist-name']"
    response = reqweb.get(url,proxy)
    if not response:
        return None
    res = path_filter(response.text, path)
    try:
        singer_name[0] = path_filter(response.text, singer_name_path)[0].text
    except Exception,e:
        print 'get albums: ' +str(e)
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


def save_songs(song_json):
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
        artist_id ='/'.join([str(i["id"]) for i in artists])
        artist_name = '/'.join([i['name'] for i in artists])
        song.artist_name = artist_name
        song.artist_id = artist_id
        try:
            song.save()
        except Exception,e:
            models.db.rollback()
            sys.stderr.write('song.save: ' +str(e))


def get_songs(album_tuple,proxy=None):
    album_songlist_url = "http://music.163.com/album?id=%s" 
    album_id = album_tuple[1]
    album_name = album_tuple[0]
    url = album_songlist_url %album_id
    title_path = ".//ul[@class='f-hide']/li/a"
    description_path = ".//meta[@name='description']"
    song_path = './/div[@id="song-list-pre-cache"]/textarea'
    response = reqweb.get(url,proxy)
    if not response:
        print 'out index: '+album_name
        return None 
    res = path_filter(response.text, title_path)
    des = path_filter(response.text, description_path)
    songs = path_filter(response.text, song_path)
    if len(songs)==0:
        return None
    try:
        song_json = json.loads(songs[0].text)
    except Exception,e:
        sys.stderr.write(str(e)+album_name+songs[0].text)
        return None
    save_songs(song_json)
    pic_url = song_json[0]["album"]["picUrl"]
    r = des[0].get('content')
    l = r.split(u'。')
    sname = l[0].split(u'：')[-1]
    date = l[1].split(u'：')[-1]
    cop =  l[2].split(u'：')[-1]
    des =  ''.join(l[3:-1])
    album = models.Album(aid = album_id,\
                        singer = singer_name[0],\
                        name = album_name,\
                        release_date = date,\
                        publisher = cop,\
                        pic_url = pic_url,\
                        description = des)
    try:
        album.save()
    except Exception,e:
        models.db.rollback()
        sys.stderr.write('album.save: aid= '+ str(album_id)+str(e))
    song_dict = {}
    for e in song_json:
        name = e["name"]
        comment_thread = e["commentThreadId"]
        song_dict[name] = comment_thread 
    return song_dict


def get_song_comment(comment_thread,proxy = None):
    song_url = "http://music.163.com/weapi/v1/resource/comments/%s?csrf_token=" %comment_thread
    params = '{"rid":"%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %comment_thread
    data = crypt.get_postData(params)
    res = reqweb.post(song_url, data, proxy)
    if res is None:
        return None
    else:
        try:
            comment = json.loads(res.text.encode('utf-8'))
            return comment
        except Exception, e:
            #print 'get_song_comment: ' + str(e)
            return None


def save_comment(comment,comment_thread):
    L.acquire()
    thread_count = models.CommentThread()
    thread_count.comment_thread = comment_thread
    thread_count.total = comment["total"]
    try:
        thread_count.save()
    except Exception,e:
        models.db.rollback()
        sys.stderr.write('thread_count.save: comment_thread = '+ comment_thread+str(e))
    hot_comment = comment['hotComments']
    for h in hot_comment:
        content = h['content']
        commentId = h['commentId']
        likedCount = h['likedCount']
        time = h['time']
        replied = h['beReplied']
        rep = ' '
        user= h['user']
        user_name = user['nickname']
        user_id = user['userId']
        user_avatar = user['avatarUrl']
        if replied:
            rep = replied[0]['content']
        if not rep:
            rep = ' '
        comment = models.Comment(cid=commentId,\
                                comment_thread = comment_thread,\
                                user_name=user_name,\
                                user_id=user_id,\
                                user_avatar=user_avatar,\
                                liked_count = likedCount,\
                                time = time,\
                                content = content,\
                                rep = rep)
        try:
            comment.save()
        except Exception,e:
            models.db.rollback()
            sys.stderr.write('comment.save: ' + str(e))
    L.release()
    

def album_thread():
    while not queue.empty():
        album_tuple = queue.get()
        song_dict = None
        try_count = 0
        while song_dict is None:
                tp1 = pqueue.get()
                pqueue.put(tp1)
                use_stat[tp1] +=1
                proxy = {"http":"http://"+tp1}
                song_dict= get_songs(album_tuple, proxy)
                if not song_dict:
                    fail_stat[tp1] +=1
                if try_count>10:
                    break
                try_count += 1
        if try_count>10:
            print 'bad proxy '
            queue.task_done()
            continue
        k = album_tuple[0]
        tmp = {}
        print k
        for i,j  in song_dict.items():
            name = i
            song_comment = None
            try_count = 0
            while song_comment is None:
                tp = pqueue.get()
                pqueue.put(tp)
                use_stat[tp] += 1
                proxy = {"http":"http://"+tp}
                song_comment = get_song_comment(j, proxy)
                if try_count>10:
                    break
                try_count +=1
                if not song_comment:
                    fail_stat[tp] +=1
            if try_count>10:
                continue
            try:
                value = song_comment['total']
            except Exception,e:
                print name + j+'NO count'
                continue
            save_comment(song_comment,j)
            tmp[name] = value
            print '\t' + name +' ' + str(value)
            sleep(1)
        gd[k] = tmp
        tmp = {}
        queue.task_done()


def load_albums_in_queue(albums):
    for k,v in albums.items():
        queue.put((k,v))


def load_proxies_in_queue(proxies):
    for p  in proxies:
        pqueue.put(p)


def log(start_time, end_time):
    # count songs
    song_sum = 0
    for k, v in gd.items():
        song_sum += len(v)
    print 'song count: %d' % song_sum
    total_time = int(end_time - start_time)
    print 'total time: %dmin %ds' % (total_time / 60, total_time % 60)
    try:
        f = open('time_stat.txt', 'a')
        line = singer_name[0] + ' ' + str(song_sum) + ' ' + str(total_time) + '\n'
        f.write(line)
    except Exception, e:
        sys.stderr.write('write time stat' + str(e))
    finally:
        f.close()


def get_singer_all_song(singer_id):
    albums_dict = get_albums(singer_id)
    while albums_dict == None:
        tp1 = pqueue.get()
        pqueue.put(tp1)
        use_stat[tp1] +=1
        proxy = {"http": "http://" + tp1}
        albums_dict = get_albums(singer_id,proxy)
        if not albums_dict:
            fail_stat[tp1] += 1

    load_albums_in_queue(albums_dict)
    print u'专辑数: ' + str(len(albums_dict))
    threads_nums = 12
    for i in xrange(threads_nums):
        t = threading.Thread(target = album_thread)
        t.setDaemon(True)
        t.start()
    queue.join()
    singer = models.Singer()
    singer.singer_id = singer_id
    singer.singer_name = singer_name[0]
    try:
        singer.save()
    except Exception,e:
        models.db.rollback()
        print 'save singer fail'



    
if __name__ == "__main__":

    #load proxies and init
    proxies_pick = open("proxy.pick")
    proxies = pickle.load(proxies_pick)
    proxies_pick.close()
    for i in proxies:
        fail_stat[i] = 0
        use_stat[i] = 0
    load_proxies_in_queue(proxies)

    #load used_singers
    try:
        o = open('used_singers.pick')
        singer_set = pickle.load(o)
    except Exception,e:
        print 'open set fail'
    finally:
        o.close()

    # start_time = time()
    # get_singer_all_song(6452)
    # end_time = time()
    # try:
    #     log(start_time, end_time)
    #     fname = singer_name[0] + '.pick'
    #     path = './pick/%s'% fname
    #     output = open(path, "wb")
    #     pickle.dump(gd, output)
    # except Exception, e:
    #     sys.stderr.write(str(e))
    # finally:
    #     output.close()
    #
    # for k,v in fail_stat.items():
    #     if use_stat[k] == fail_stat[k]:
    #         proxies.remove(k)
    #     print k + '\t'+str(use_stat[k])+'\t'+str(v)
    # print 'left: %d' %len(proxies)
    #
    # gd = {}

    #in practice
    f = open('singer_id.pick')
    l = pickle.load(f)
    f.close()
    for e in l:
        if e in singer_set:
            continue
        singer_set.add(e)
        start_time = time()
        get_singer_all_song(e)
        end_time = time()
        for k,v in fail_stat.items():
            print k + '\t'+ str(v)+'\t'+str(use_stat[k])
            use_stat[k] =0
            fail_stat[k] = 0

        #log info
        try:
            log(start_time, end_time)
            fname = singer_name[0] + '.pick'
            path = './pick/%s'% fname
            output = open(path, "wb")
            pickle.dump(gd,output)
        except Exception,e:
            print str(e)
        finally:
            output.close()
        #save set
        try:
            o = open('used_singers.pick', 'wb')
            pickle.dump(singer_set, o)
        except Exception, e:
            print 'open set fail'
        finally:
            o.close()
        gd = {}




    filtered = open('proxy.pick','wb')
    pickle.dump(proxies,filtered)
    # output.close()
    # cloudoffile.rank(fname)
