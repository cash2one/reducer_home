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

for line in stdin:
  try:
    line=line.decode('utf-8')
    dp = line.strip()
    co = 100
    # a = float(rank)
    print " ".join([dp, str(co), 'feeling'])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0