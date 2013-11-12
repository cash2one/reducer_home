#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'mantou'

# input = file("keyword_real.txt")
output = file(sys.argv[1],'w')
keywordBef = None
cityidBef = None
sids = ['','','','']
i = 0
flag = False
for line in file("keyword_real2.txt"):

    cityid, keyword, sid, score = line.split('\t')
    sid = sid.decode("utf-8")

    # print keyword,keywordBef
    if keyword != keywordBef or cityid != cityidBef or keywordBef == None:
        flag = True
    else:
        flag = False
    # print keyword,keywordBef
    # print cityid,cityidBef
    # print flag
    # print sids

    if flag:
        if keywordBef != None:
            output.writelines('\t'.join([cityidBef,keywordBef,sids[0],sids[1],sids[2],sids[3],'\n']))
        keywordBef = keyword
        cityidBef = cityid
        sids = ['','','','']
        i = 0
    else:
        i += 1
    sids[i] = sid






