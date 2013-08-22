#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
sys.path+=["/Library/Python/2.7/site-packages"]
reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime
import subprocess
import json
import pymysql as MySQLdb

MySQLdb.install_as_MySQLdb()

C = MySQLdb.connect

class DeviceIter(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        # self.cityIDs = {}
        self.city = None
        self.keywordData = []
        self.last = []
        self.deviceid = None

    def getOneDeviceDate(self):
        ret = self.keywordData
        for line in self.file:
            # print line
            try:
                if len(line) > 5:
                    deviceid, cityid, shopid, rank = line.replace('\n', '').split('\t')
                else:
                    print "too short"
                    continue
            except ValueError as e:
                print "."
                pass
            else:
                #print keyword,cityid,score,self.lastkeyword
                if deviceid == self.deviceid and cityid == self.city:
                    # print "old keyword",keyword
                    self.keywordData.append((deviceid, cityid, shopid, rank))
                elif self.deviceid is None:
                    # print "first time"
                    self.city = cityid
                    self.deviceid = deviceid
                    self.keywordData.append((deviceid, cityid, shopid, rank))
                else:
                    # print "new keyword",keyword
                    ret = self.keywordData
                    self.keywordData = [(deviceid, cityid, shopid, rank)]
                    self.city = cityid
                    self.deviceid = deviceid
                    break

        if ret != self.last:
            self.last = ret
            for l in ret:
                yield l
        else:
            # return
            yield StopIteration()

if __name__ == '__main__':

    mobile_update = sys.argv[1]

    total = 67851701
    # for line in file(mobile_update):
    #     total +=1
    # print "total",total

    iter = DeviceIter(mobile_update)

    try:
        conn = None
        cur = None
        sql = None
        count = 0
        userid_count = 0
        correct = 0
        end = 1
        while end:

            if userid_count % 5000 == 0:
                if conn:
                    conn.commit()
                    conn.close()
                conn = MySQLdb.connect(host='192.168.8.41', user='airec', passwd='dp!@VGSrf1cjE', db='airec', port=3306,
                                   charset='utf8')
                cur = conn.cursor()
                sql = """USE airec;"""
                cur.execute(sql)

            userid_count += 1

            useridrankmap = {}

            for l in iter.getOneDeviceDate():
                ll = list(l)
                if len(ll) == 0:
                    end = 0
                    break
                count += 1

                userid, cityID, word, score = l[0], l[1], l[2], l[3]
                # word = word.encode("utf-8")
                if "'" in word:
                    continue
                # word = word.replace("'","\\'")
                useridrankmap[word] = score

            # print userid, cityID
            # print json.dumps(deviceidrankmap)

            sql = """REPLACE INTO airec.DP_SearchKeyword (Userid, CityID, KeywordRankMap) VALUES('%s','%d','%s')
            """ % (userid, int(cityID), json.dumps(useridrankmap, ensure_ascii = False))

            # print sql
            ret = cur.execute(sql)
            if ret > 0:
                correct += 1
            if userid_count % 2000 == 0:

                conn.commit()
                print correct/userid_count,correct,"/",userid_count
                print 100*count/total, '%'
                print sql
                time.sleep(0.5)
                # break


    except Exception, ex:
        print "DB ERROR:", ex
    finally:
        conn.close()
print "\ndone."



