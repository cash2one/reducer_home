# -*- coding: utf-8 -*-
# __author__ = 'mantou'
from __future__ import division
import sys
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')



dish_dict = "../DISH_SCRIPT/dish_dict_reduced.txt"
feeing_dict = "../DISH_SCRIPT/dp_feeling_dict.txt"
tasty_dict = "../DISH_SCRIPT/dp_tasty_dict.txt"
ranklist_dict = "ranklist_dict.txt"

jieba.load_userdict(dish_dict)
jieba.load_userdict(feeing_dict)
jieba.load_userdict(tasty_dict)
jieba.load_userdict(ranklist_dict)

out = file("out2.txt",'w')

count = 0
for line in file("ranklist_review.txt"):
    if len(line.strip()) == 0:
        continue
    count +=1
total = count
count = 0
dict = {}
def show(shopid,dict):
    for item in dict.keys():
        print shopid,item.replace('\n',''),str(dict[item])
        # print '\t'.join([shopid,item,str(dict[item])])
        out.writelines('\t'.join([shopid,item,str(dict[item])])+'\n')


for line in file("ranklist_review.txt"):
    # print line
    if len(line.strip()) == 0:
        continue
    # l = line.split('\t')
    # print l[0]
    # print l[1]
    shopid = line.split('\t')[2]
    reviewbody = line.split('\t')[5].replace('\n','').decode('utf-8')
    seg_list = jieba.cut_for_search(reviewbody)

    if shopid == id:
        pass
    else:
        # count += 1
        show(id,dict)
        id = shopid
        # show(shopid,dict)
        dict = {}
    for w in seg_list:
        if dict.has_key(w):
            dict[w] += 1
        else:
            dict[w] = 1
    # out.write(shopid + '\t'+ '\t'.join(seg_list)+ '\n')
    count += 1
    # if count > 2:
    #     break
    if count % 1000 == 0:
        print count / total

out.close()




