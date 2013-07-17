#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime
import subprocess
import json
import pymysql as MySQLdb

MySQLdb.install_as_MySQLdb()

C = MySQLdb.connect
__author__ = 'linkerlin'

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
        deviceid_count = 0
        correct = 0
        end = 1
        while end:

            if deviceid_count % 5000 == 0:
                if conn:
                    conn.commit()
                    conn.close()
                conn = MySQLdb.connect(host='192.168.8.44', user='airec', passwd='dp!@VGSrf1cjE', db='airec', port=3306,
                                   charset='utf8')
                cur = conn.cursor()
                sql = """USE airec;"""
                cur.execute(sql)

            deviceid_count += 1

            deviceidrankmap = {}

            for l in iter.getOneDeviceDate():
                ll = list(l)
                if len(ll) == 0:
                    end = 0
                    break
                count += 1

                deviceid, cityID, shopID, score = l[0], l[1], l[2], l[3]
                deviceidrankmap[shopID] = score

            # print deviceid, cityID
            # print json.dumps(deviceidrankmap)

            sql = """REPLACE INTO airec.DP_MobileRec (DeviceID, CityID, ShopIDRankMap) VALUES('%s','%d',"%s")
            """ % (deviceid, int(cityID), deviceidrankmap)

            # print sql
            ret = cur.execute(sql)
            if ret > 0:
                correct += 1
            if deviceid_count % 1000 == 0:
                conn.commit()
                print correct/deviceid_count,correct,"/",deviceid_count
                print 100*count/total, '%'
                print sql
                time.sleep(1)

                #     sql = """DELETE FROM DP_MobileRec WHERE Deviceid = '%s' and CityID = '%s'
                #     """ % (deviceid, int(cityID))
                #     # print sql
                #     ret = cur.execute(sql)
                #
                # sql = """INSERT INTO DP_MobileRecommend (Deviceid, CityID, Shopid, Rank) value('%s','%d','%d','%f');
                #     """ % (deviceid, int(cityID),int(shopID), float(score))
                # # print sql
                # ret = cur.execute(sql)

    except Exception, ex:
        print "DB ERROR:", ex
    finally:
        conn.close()
print "\ndone."



