#!/bin/env python
# -*- coding: utf-8 -*-
import sys
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
    sid1=line.strip().split('\t')[0]
    sid2=line.strip().split('\t')[1]
    rank=line.strip().split('\t')[2]
    # a = float(rank)
    # print a
    print "\t".join([sid1, sid2, rank])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0