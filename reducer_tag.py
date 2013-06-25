#!/bin/env python
# -*- coding: utf-8 -*-
import sys
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')
from string import join

tagdict={}
atmosphere2 = {u'随便吃吃':'1',u'家庭聚会':'1',u'情侣约会':'1',u'商务宴请':'1',u'休闲小憩':'1',u'朋友聚餐':'1'}
atmosphere = [u'随便吃吃',u'家庭聚会',u'情侣约会',u'商务宴请',u'休闲小憩',u'朋友聚餐']

character2 = {u'可以刷卡':'1',u'无线上网':'1',u'24小时营业':'1',u'有生日优惠':'1',u'有无烟区':'1',u'有午市套餐':'1'\
    ,u'有下午茶':'1',u'供应夜宵':'1',u'供应早餐':'1',u'是老字号':'1',u'有表演':'1',u'有景观位':'1',u'免费停车':'1'\
    ,u'可送外卖':'1',u'有露天位':'1',u'洋房别墅':'1',u'可办大型宴会':'1'}
character = [u'可以刷卡',u'无线上网',u'24小时营业',u'有生日优惠',u'有无烟区',u'有午市套餐'\
    ,u'有下午茶',u'供应夜宵',u'供应早餐',u'是老字号',u'有表演',u'有景观位',u'免费停车'\
    ,u'可送外卖',u'有露天位',u'洋房别墅',u'可办大型宴会']

shopid=0
cityid=0
def output(tagdict):
  try:
    if cityid==0: return
    if len(tagdict)==0: return
    if shopid==0: return
    for key in tagdict:
        if atmosphere.has_key(key):
            tagtype = u'餐厅氛围'
        elif character.has_key(key):
            tagtype = u'餐厅特色'
        else:
            tagtype = u'推荐菜'
        print "\t".join([cityid,shopid,tagtype,key.encode('utf-8'),tagdict[key]])
  finally:
    pass

for line in stdin:
  try:
    line=line.decode('utf-8')
    cityid=line.strip().split('\t')[0]
    shopid=line.strip().split('\t')[1]
    tagcounts=line.strip().replace("\n","").split('\t')[2].split('|')
    for tagcount in tagcounts:
        if len(tagcount)>0:
            tag,count=tagcount.split(',')
            tagdict[tag]=count
    output(tagdict)
  except IndexError,ex:
    pass
  except ValueError,ex:
    pass
  finally:
    tagdict={}
    shopid=0