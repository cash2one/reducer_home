#!/bin/env python
# -*- coding: utf-8 -*-
import urllib
import sys
import re
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
pat1 = '搜索商户'
patE = r'^[0-9a-zA-Z \'\.]+$'
shopid = 0
f=stdin
for line in f:
  try:
    guid = line.strip().split('\t')[0]
    city= line.strip().split('\t')[1]
    url = line.strip().split('\t')[2]
    keyword = urllib.unquote(url)
    if type(keyword)=="str":
      keyword = keyword.decode("utf-8","ignore")
    k = len(keyword.split())
    if re.match(patE, keyword) and len(keyword) >=5 :
      # print len(keyword)
      print "\t".join([guid, city, keyword])
    elif ((k >= 1) and (k <= 2)) and not re.search(pat1,keyword) and not re.match(patE, keyword) :
      # print keyword
      keyword = keyword.replace(u'、',u' ').replace(u'，', u' ').replace(u'.', u' ').replace(u',', u' ').replace(u'。', u' ').replace(u'#', u' ')
      for key in keyword.split():
        if len(key) >=2 and len(key) <=7:
          print "\t".join([guid, city, key])
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0
