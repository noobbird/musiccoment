#_*_coding:utf-8_*_
import psycopg2
import time
db = psycopg2.connect(database="music", user="yang", password="ssylqwjxhwykzz", \
                        host="47.94.84.186", port="5432")
#prepare a cursor object ussing cursor() method
cursor = db.cursor()

def select(song_id):
	sql = '''
		select * from hot_50 where song_id=%s
		'''
	try:
		cursor.execute(sql,(song_id,))
		return len(cursor.fetchall())
	except Exception,e:
		print e
		db.rollback()
	


def update(params):
	update_sql = '''
		UPDATE hot_50 SET comment_total=%s, 
		last_comment_total=comment_total, update_time=date_trunc('second',current_timestamp), last_update_time=update_time, status=%s WHERE song_id=%s 
		'''
	try:
		cursor.execute(update_sql,params)
		db.commit()
	except Exception,e:
		print e
		db.rollback()

def insert(params ):
	insert_sql = '''
		INSERT INTO hot_50 ( song_name, singer_name, album_name, comment_total, 
last_comment_total, song_id, comment_thread_id, duration, album_id, update_time, last_update_time, status) 
VALUES ( %s, %s, %s, %s,
 %s, %s, %s, 
%s, %s, date_trunc('second',current_timestamp), date_trunc('second',current_timestamp), %s);
		''' 
	sql = '''
		select * from hot_50 where song_id=1211
		'''
	try:
	    r = cursor.execute(insert_sql,params)
	    db.commit()
	except Exception,e:
	    print e
	    db.rollback()

if __name__ == "__main__":
	now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print now
	print select(12111)	
	#insert(('sun','jay','fantasy',100,121, 10086,'SO_4_31',12121,121,-1))
	update(('110010','3',10086))
