#_*_coding: utf-8_*_
from peewee import * 

db = PostgresqlDatabase('netease', user='test',password='test',host='localhost')

class Album(Model):
    aid = CharField()
    name = CharField()
    singer = CharField()
    release_date = DateField()
    publisher = CharField()
    pic_url = CharField()
    description = TextField()
    
    class Meta:
        database = db

class Comment(Model):
    cid = IntegerField()
    comment_thread = CharField()
    user_name = CharField()
    user_id = IntegerField()
    user_avatar = CharField()
    liked_count = IntegerField()
    time = DoubleField()
    content = TextField()
    rep = TextField()
    class Meta:
        database = db
class Song(Model):
    song_id = CharField()
    song_name = CharField()
    duration = DoubleField()
    comment_thread = CharField()
    artist_name = CharField()
    artist_id = CharField()
    album_id = IntegerField()
    album_name = CharField()
    class Meta:
        database = db

class CommentThread(Model):
    comment_thread = CharField()
    total = IntegerField()
    
    class Meta:
        database = db


if __name__ == '__main__': 
    try:
        Album.create_table()
    except Exception,e:
        print str(e)
    try:
        Comment.create_table()
    except Exception,e:
        print str(e)
    try:
        Song.create_table()
    except Exception,e:
        print str(e)
    try:
        CommentThread.create_table()
    except Exception,e:
        print str(e)
