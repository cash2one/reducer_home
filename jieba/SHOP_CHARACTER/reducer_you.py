#!/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
import sys
import string
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
from string import join


tagdict={}

frist = 1
second = 1
dpfrist = u''
dpsecond = u''

shopid=0
cityid=0
dish = None

tempdp = []
shopdict = {}

tasty = set([])
k = 0.0

filename = sys.argv[1]

for line in file(filename):
    shopid = line.strip().split('\t')[0]
    c = int(line.strip().split('\t')[4])
    if shopid not in shopdict.keys():
        shopdict[shopid] = 0
    if shopdict[shopid] < c:
        shopdict[shopid] = c
#
# for line in stdin:
#   try:
#  #   line=line.decode('utf-8')
#     shopid = line.strip().split('\t')[0]
#     currentdish = line.strip().split('\t')[1]
#     dp = line.strip().split('\t')[2].decode("utf-8")
#     dpdetial = line.strip().split('\t')[4]
#     c = line.strip().split('\t')[6]
#
#     if c < 2 or len(dp) > 1:
#         continue
#     else:
#         if currentdish == dish and dp in tasty and dp == dpdetial:
#
#             if c > second:
#                 dpsecond = dp[:]
#                 second = c
#             if second > frist:
#
#                 temp = second
#                 tempdp = dpsecond[:]
#                 dpsecond = dpfrist[:]
#                 second = frist
#                 dpfrist = tempdp[:]
#                 frist = temp
#
#
#         elif currentdish != dish:
#             if frist > 1 and second > 1:
#                 print shopid ,dish, '又', dpfrist, '又' , dpsecond
#             dish = currentdish
#             frist = second = 1
#             dpfrist = dpsecond = u''
#
#   except IndexError,ex:
#     pass
#   except ValueError,ex:
#     pass
#   finally:
#     tagdict={}
#     shopid=0


for line in file(filename):
  try:
 #   line=line.decode('utf-8')
    shopid = line.strip().split('\t')[0]
    currentdish = line.strip().split('\t')[1]
    dp = line.strip().split('\t')[2].decode("utf-8")
    dpdetial = line.strip().split('\t')[3]
    c = int(line.strip().split('\t')[4])

    wahaha = dpdetial

    # if dp == u'干' or nv == u'象' or currentdish == u'没有' or c < 2:
    #     pass
    if c < 2:
        continue
    else:
        if c > 1 and len(dp) == 1 and dpdetial == dp:
            continue
            # print k , int(shopdict[shopid])
            # if k > 0.8:
            #     wahaha = u'很'+ dp
            # # print shopid,  int(shopdict[shopid]),currentdish, k , u'很'+ dp
            # elif k > 0.6:
            #     wahaha = u'挺'+dp
            # # print shopid,  int(shopdict[shopid]),currentdish, k ,u'挺'+dp
            # elif k > 0.1:
            #     wahaha = u'比较'+dp
            # # print shopid,  int(shopdict[shopid]),currentdish, k ,u'比较'+dp

        print '\t'.join([shopid,currentdish,dp,wahaha,str(c)])

  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0
