#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql as MySQLdb

MySQLdb.install_as_MySQLdb()

C = MySQLdb.connect

if __name__ == '__main__':

    dp_file = sys.argv[1]

    total = 1
    for line in file(dp_file):
        total +=1
    print "total",total

    try:
        conn = None
        cur = None
        sql = None
        count = 0
        correct = 0
        end = 1

        dishbefor = None

        tagmap = {}

        for line in file(dp_file):

            if count % 10000 == 0:
                if conn:
                    conn.commit()
                    conn.close()
                conn = MySQLdb.connect(host='192.168.8.44', user='airec', passwd='dp!@VGSrf1cjE', db='airec', port=3306,
                                   charset='utf8')
                cur = conn.cursor()
                sql = """USE airec;"""
                cur.execute(sql)

            count += 1


            l = line.replace('\n','').split('\x01')

            shopID, dish, dp, rank = l[0], l[1].encode("utf-8"), l[2].encode("utf-8"), l[3]

            # dp = dp.encode("utf-8")
            if dishbefor is None:
                tagmap[dp.encode("utf-8")] = rank
                dishbefor = dish
            elif dish == dishbefor:
                tagmap[dp.encode("utf-8")] = rank
            else:
                # print tagmap.keys()
                record = json.dumps(tagmap, ensure_ascii=False).encode("utf-8")
                # print record
                tagmap = {}
                tagmap[dp.encode("utf-8")] = rank
                dishbefor = dish

                sql = """INSERT INTO DP_DishReview (Shopid,Tag,TagRankMap) value('%d','%s','%s');
                    """ % (int(shopID), dish, record.encode("utf-8"))
                sql = sql.encode("utf-8")
                print sql.encode("utf-8")
                ret = cur.execute(sql)
                if ret > 0:
                    correct += 1
                if count % 3000 == 0:
                    conn.commit()
                    print correct/count,correct,"/",count
                    print 100*count/total, '%'
                    print sql
                    time.sleep(1)
    except Exception, ex:
        print "DB ERROR:", ex
    finally:
        conn.close()
print "\ndone."



