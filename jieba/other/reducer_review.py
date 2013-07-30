#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
# from string import join
# reducer 点评

tagdict={}

shopid=0
cityid=0

shops = []
dishs = []
for lines in file("cold.txt"):
    shopid = lines.strip().split('\t')[1].strip()
    if shopid not in shops:
        shops.append(shopid)


# for lines in file("dp_review 2.txt"):
#     try:
#         body = lines.strip().split('\t')[3].strip()
#         shopid = lines.strip().split('\t')[2].strip()
#     except IndexError,ex:
#         continue
#     # if shopid == '2607334':
#         # print '-------------'
#     # if dish not in dishs:
#     #     dishs.append(dish)
#     # if shopid not in shops:
#     #     shops.append(shopid)
#     print '\t'.join([shopid,body])

# print '\n'.join(dishs)
# print '\n'.join(shops)

for line in stdin:
  try:
    shopid = line.strip().split("\t")[0]
    # co = len(dp)
    # a = float(rank)
    # print shopid
    if shopid in shops:
        print line
    # print " ".join([dp, str(co), 'dp'])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0