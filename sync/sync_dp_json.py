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
        self.shopid = None

    def getOneDeviceDate(self):
        ret = self.keywordData
        for line in self.file:
            # print line
            try:
                if len(line) > 5:
                    shopid, tag, detial,rank = line.replace('\n', '').split('\t')
                else:
                    print "too short"
                    continue
            except ValueError as e:
                print "."
                pass
            else:
                #print keyword,cityid,score,self.lastkeyword
                if shopid == self.shopid:
                    # print "old keyword",keyword
                    self.keywordData.append((shopid,tag,detial,rank))
                elif self.shopid is None:
                    # print "first time"
                    self.shopid = shopid
                    self.keywordData.append((shopid, tag,detial, rank))
                else:
                    # print "new keyword",keyword
                    ret = self.keywordData
                    self.keywordData = [(shopid, tag,detial, rank)]
                    self.shopid = shopid
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
    total = 1
    for line in file(mobile_update):
        total +=1
    print "total",total

    iter = DeviceIter(mobile_update)

    try:
        conn = None
        cur = None
        sql = None
        count = 0
        shopid_count = 0
        correct = 0
        end = 1
        while end:

            if shopid_count % 5000 == 0:
                if conn:
                    conn.commit()
                    conn.close()
                conn = MySQLdb.connect(host='192.168.8.44', user='airec', passwd='dp!@VGSrf1cjE', db='airec', port=3306,
                                   charset='utf8')
                cur = conn.cursor()
                sql = """USE airec;"""
                cur.execute(sql)

            shopid_count += 1

            shopidrankmap = {}

            for l in iter.getOneDeviceDate():
                ll = list(l)
                if len(ll) == 0:
                    end = 0
                    break
                count += 1

                shopid, tag, dpdetial, score = l[0], l[1], l[2], l[3]
                # word = word.encode("utf-8")
                # if "'" in word:
                #     continue
                # word = word.replace("'","\\'")
                tagmap = {}
                tagmap[dpdetial] = score
                if not shopidrankmap.has_key(tag):
                    shopidrankmap[tag] = []

                shopidrankmap[tag].append(tagmap)


            # print shopid
            # print json.dumps(shopidrankmap,ensure_ascii = False))

            sql = """REPLACE INTO airec.DP_ShopTagCloud (ShopID, ShopRankMap) VALUES('%s','%s')
            """ % (shopid, json.dumps(shopidrankmap, ensure_ascii=False))
            if json.dumps(shopidrankmap, ensure_ascii=False) == "{}":
                print "pass: "+sql
            else:
             # print sql
                ret = cur.execute(sql)
            if ret > 0:
                correct += 1



            if shopid_count % 200 == 0:
                conn.commit()
                print correct/shopid_count, correct,"/",shopid_count
                print 100*count/total, '%'
                print sql
                time.sleep(0.05)
                # break
    except Exception, ex:
        print "DB ERROR:", ex
    finally:
        conn.commit()
        conn.close()
print "\ndone."



