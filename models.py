#_*_coding: utf-8_*_
from peewee import *

db = MySQLDatabase('netease',user='cain',charset = 'utf8')

class Album(Model):
    aid = CharField()
    name = CharField()
    singer = CharField()
    release_date = DateField()
    publisher = CharField()
    description = CharField()
    
    class Meta:
        database = db
try:
    Album.create_table()
except Exception,e:
    print str(e)
