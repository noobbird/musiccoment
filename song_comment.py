#_*_coding: utf-8_*_
import reqweb
import crypt
import json
import models

song_id = "4154790"
song_url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=" %song_id
params = '{"rid":"R_SO_%s","offset":"0","total":"true","limit":"100","csrf_token":""}' %song_id
proxies = {"http": "http://47.52.24.117:80"}
data = crypt.get_postData(params)
res = reqweb.post(song_url, data)
comment_json = json.loads(res.text)
print comment_json["total"]
for h in comment_json["hotComments"]:
    content = h['content']
    commentId = h['commentId']
    likedCount = h['likedCount']
    time = h['time']
    replied = h['beReplied']
    rep = ''
    user= h['user']
    user_name = user['nickname']
    user_id = user['userId']
    user_avatar = user['avatarUrl']
    if replied:
        rep = replied[0]['content']
    comment = models.Comment(cid=commentId,\
                            song_id = song_id,\
                            user_name=user_name,\
                            user_id=user_id,\
                            user_avatar=user_avatar,\
                            liked_count = likedCount,\
                            time = time,\
                            content = content,\
                            rep = rep)
    comment.save()

    print '\trep: ' + rep +'\ncontent' + content
    print 'user: '+user_name+'\t'+str(user_id)+'\t'+user_avatar+str(likedCount)

#for c in comment_json["hotcomments"]:
#    print c["user"]["nickname"] + ': ' + c['content']
print res.headers['X-From-Src']

