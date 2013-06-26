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

def output(catlist , catshop):
  try:
    # print catlist
    # print catshop
    while len(catlist)>0:
        for cat1 in catlist:
            if len(catshop[cat1])>0:
                (shopid,rank) = catshop[cat1].pop(0)
                print "\t".join([deviceid_old,shopid,cat1,rank])
            else:
                catlist.remove(cat1)
  finally:
    pass

currentid = None
deviceid_old = None

catshop = {}
catlist = []
for line in stdin:
  try:
    line=line.decode('utf-8')
    deviceid,shopid,cat1,rank = line.strip().split()
    if deviceid != deviceid_old:
      deviceid_old = deviceid
      print 'id changed',deviceid
      # print catshop
      if len(catlist) > 0:
          output(catlist,catshop)
      catshop = {}
      catlist = []
    if cat1 not in catlist:
        catlist.append(cat1)
        catshop[cat1] = [tuple((shopid, rank))]
    catshop[cat1].append(tuple((shopid, rank)))

  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0