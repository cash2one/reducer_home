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

    keyword_hot = sys.argv[1]
    cityID = None
    total = 1
    for line in file(keyword_hot):
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

        for line in file(keyword_hot):
            count += 1
            keyword, newcityID , score = line.replace('\n', '').split('\t')
            score=float(score)
            if cityID == newcityID:
                pass
            else:
                cityID = newcityID
                sql = """DELETE FROM airec.DP_SearchKeyword_Hot WHERE CityID = '%d'
            """ % (int(newcityID))
                # print sql
                cur.execute(sql)


            sql = """INSERT INTO airec.DP_SearchKeyword_Hot (Keyword, CityID, Score) VALUES('%s','%d','%d')
            """ % ( keyword.replace("'","\\'"),int(newcityID),int(score))
            print sql
            ret = cur.execute(sql)

            if ret > 0:
                correct += 1
            if count % 100 == 0:

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



