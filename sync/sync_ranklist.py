#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime
import pymysql as MySQLdb

MySQLdb.install_as_MySQLdb()

C = MySQLdb.connect

HOST = '192.168.8.41'
PASSWORD = 'dp!@VGSrf1cjE'

if __name__ == '__main__':

    inputfile = sys.argv[1]
    cityID = None
    total = 1
    for line in file(inputfile):
        total +=1
    print "total",total

    try:
        conn = None
        cur = None
        sql = None
        count = 0
        correct = 0

        conn = MySQLdb.connect(host= HOST , user='airec', passwd=PASSWORD , db='airec', port=3306,
                                   charset='utf8')
        cur = conn.cursor()
        sql = """USE airec;"""
        cur.execute(sql)

        for line in file(inputfile):
            count += 1
            cityID,keyword, shopid,shopname, score = line.replace('\n', '').split('\t')
            score=float(score)

            sql = """INSERT INTO airec.DP_Ranklist (CityID, Word, ShopID, Shopname, Score) VALUES('%d', '%s','%d','%s','%f')
            """ % ( int(cityID), keyword , int(shopid) ,shopname.replace("'","\\'") ,score)
            print sql
            ret = cur.execute(sql)

            if ret > 0:
                correct += 1
            if count % 500 == 0:

                conn.commit()
                print correct/count,correct,"/",count
                print 100*count/total, '%'
                print sql
                time.sleep(0.5)
                # break

    except Exception, ex:
        print "DB ERROR:", ex
    finally:
        conn.commit()
        conn.close()
print "\ndone."



