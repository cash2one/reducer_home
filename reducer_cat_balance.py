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

def output(tagdict):
  try:
    if cityid==0: return
    if len(tagdict)==0: return
    if shopid==0: return
    for key in tagdict:
        print "\t".join([cityid,shopid,key.encode('utf-8'),tagdict[key]])
  finally:
    pass

currentid = None
cat = {}
deviceid_old = None
for line in stdin:
  try:
    line=line.decode('utf-8')
    deviceid,shopid,rank = line.strip().split()
    if deviceid != deviceid_old:
      deviceid_old = deviceid
      print 'id changed',deviceid

  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0