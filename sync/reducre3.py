#!/bin/env python
# -*- coding: utf-8 -*-


import sys
import string
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
from string import join


dishb = None
count = 0
tmp = []
filename = sys.argv[1]

for line in file(filename):

    dish = line.strip().split('\t')[1].decode("utf-8")
    dp = line.split('\t')[2].decode("utf-8")
    line = line.strip()

    if dish == u'服务员' or dish == u'情侣':
        continue
    if dish != dishb:
        dishb = dish
        count = 1
        tmp = []
    else:
        count +=1
        # print count
    if count > 3:
        continue

    tmp.append(dp)
    f = True
    for item in tmp:
        if dp in item and len(dp) != len(item):
            f = False
    # print ' '.join(tmp)
    if f:
        print line




