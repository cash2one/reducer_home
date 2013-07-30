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

for line in stdin:
  try:
 #   line=line.decode('utf-8')
    shopid = line.strip().split('\t')[0]
    dish = line.strip().split('\t')[1]

    # a = float(rank)
    if ' ' not in dish:
        print "\t".join([shopid , dish.upper()])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0