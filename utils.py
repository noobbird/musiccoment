# _*_ coding:utf-8_*_
# Date: 2018/10/6
import requests
import re
import db
import json
import crypt
from lxml import etree
home_url = 'https://music.163.com/artist?id=%d'
headers = {
"host": "music.163.com",
"connection": "keep-alive",
"upgrade-insecure-requests": "1",
"user-agent": "mozilla/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/69.0.3497.100 safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"referer": "https://music.163.com/",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-cn,zh;q=0.9,en;q=0.8"
}
def path_filter(page, path):
    tree = etree.HTML(page)
    res = tree.xpath(path)
    return res
def get_albums(singer_id=5781):
	'''
	return dict{album_name:album_id}
	'''
	singer_albumlist_url='http://music.163.com/artist/album?id=%s&limit=300&offset=0'
	url = singer_albumlist_url %singer_id
	path = ".//*[@id='m-song-module']/li/p/a"
	singer_name_path = ".//h2[@id='artist-name']"
	response = requests.get(url, headers=headers)
	res = path_filter(response.text, path) 
	singer_name = path_filter(response.text, singer_name_path)[0].text
	print u'歌手: ' + singer_name
	album_dict = {}
	for e in res:
	    name = e.text
	    value = e.get('href').split('=')[-1]
	    print name, e.get('href'),value#name = e.text
	    album_dict[name] = value
	return album_dict

#by commentThreadid get song comment
def comment(cmtid = 'R_SO_4_29732650'):
	url = 'https://music.163.com/weapi/v1/resource/comments/%s?csrf_token='
	params = '{"rid":"%s","offset":"0","total":"true","limit":"100","csrf_token":""}'
	data = crypt.get_postData(params%cmtid)
	r = requests.post(url%cmtid, data= data, headers = headers)
	comment_json = json.loads(r.text)
	return comment_json

#50 hot song on singer homepage 
def get_hot(singer_id=7219):
	r = requests.get(home_url % singer_id, headers = headers)
	#print(r.text)
	json_text = re.search('\[{.*}\]', r.text).group(0)
	#print json_text
	hot_json = json.loads(json_text)
	#print hot_json
	song_list =[]
	for i in hot_json:
		t_dict={
		'commentThreadId' : i['commentThreadId'],
		'song_name' : i['name'],
		'singer_name' : '\\'.join([art['name'] for art in i['artists']]),
		'album_name' : i['album']['name'],
		'song_id' : i['id'],
		'album_id' : i['album']['id'],
		'duration' : i['duration'],
		'status' : i['status'],
		}
		song_list.append(t_dict)	
	return song_list

def search(key_word):
	url = "https://music.163.com/weapi/search/suggest/web?csrf_token="
	params = '{"s":"%s","limit":"8","csrf_token":""}'
	data = crypt.get_postData(params%key_word)
	headers["Content-Type"]= "application/x-www-form-urlencoded"
	r = requests.post(url, data = data, headers = headers)
	print r.text

def update(singer_id):
	md = get_hot()
	for m in md:
		total = comment(m['commentThreadId'])['total']
		if db.select(m['song_id'])==0:
			db.insert((m['song_name'],m['singer_name'],m['album_name'],total,total,m['song_id'],m['commentThreadId'],m['duration'],m['album_id'],m['status']))
		else:
			db.update((total,m['status'],m['song_id']))
		print m['song_name'],total


	
if __name__ == '__main__':
	print len(get_hot())
	#comment(cmtid)
	#get_albums()
	search("zhou")
	

