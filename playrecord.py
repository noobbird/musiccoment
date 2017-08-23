#_*_coding : utf-8 _*_
#FileName : playrecord.py
#Author : YMY
#Create time: 2017/8/20
import myweb
import crypt
import json

class Record():
    def __init__(self, uid, epyt):
        self.refer = 'http://music.163.com/playlist?id=%s' %uid
        self.url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
        self.params = '{"uid":"%s","type":"%s","limit":"1000","offset":"0","total":"true","csrf_token":""}' %(uid, epyt)
    def get_json(self):
        web = myweb.MyWeb(self.refer)
        data = crypt.get_postData(self.params)
        res = web.post(self.url, data)
        return json.loads(res.read())

if __name__ == "__main__":
    rec = Record("54892316", "0")
    data = rec.get_json()
    li = data["allData"]
    count = 0
    for i in li:
        print str(count) +' ' + i["song"]["name"]
        count += 1 
