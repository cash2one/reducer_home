#!/bin/env python
# -*- coding: utf-8 -*-
# reducer 推荐菜


import sys
import string
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
from string import join

tagdict={}

shopid=0
cityid=0

for line in file('shop_dish.txt'):
  try:
 #   line=line.decode('utf-8')
    dish = line.strip().split('\t')[1]
    # count = line.strip().split('\t')[1]
    # co = float(count)
    co = 1.0
    # a = float(rank)
    if ' ' not in dish:
        print " ".join([dish.upper(), str(co), 'n'])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0