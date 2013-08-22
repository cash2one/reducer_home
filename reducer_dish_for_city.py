#!/bin/env python
# -*- coding: utf-8 -*-
import sys
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
from string import join



d1 = file("shop_dish1.txt",'w')
d2 = file("shop_dish2.txt",'w')
d3 = file("shop_dish3.txt",'w')

for line in file('shop_dishs.txt'):

 #   line=line.decode('utf-8')
    city=line.strip().split('\t')[0]
    shopid=line.strip().split('\t')[1]
    tag=line.strip().split('\t')[2]
    print city
    # a = float(rank)
    # print a
    if city == '1':
        d1.writelines("\t".join([shopid, tag.upper(),'\n']))
    elif city == '2':
        d2.writelines("\t".join([shopid, tag.upper(),'\n']))
    else:
        d3.writelines("\t".join([shopid, tag.upper(),'\n']))


d1.close()
d2.close()
d3.close()