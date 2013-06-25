#!/bin/env python
# -*- coding: utf-8 -*-
import urllib
import sys
import re
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')

pat1 = u'搜索商户'
patE = r'^[0-9a-zA-Z \']+$'
shopid=0
f=stdin
for line in f:
  try:
    guid = line.strip().split('\t')[0]
    city= line.strip().split('\t')[1]
    url = line.strip().split('\t')[2]
    keyword = urllib.unquote(url)
    if type(keyword)=="str":
      keyword = keyword.decode("utf-8","ignore")
    keyword = keyword.replace(u'、',u' ').replace(u'，', u' ').replace(u'.', u' ').replace(u',', u' ').replace(u'。', u' ').replace(u'#', u' ')
    k = len(keyword.split())
    if re.match(patE, keyword):
      print "\t".join([guid, city, keyword])
    elif ((k >= 1) and (k <= 3)) and not re.search(pat1,keyword):
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

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False


def is_english(uchar):
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

#中文数字 去标点符号，分开，长度限制
#英文 什么都不干