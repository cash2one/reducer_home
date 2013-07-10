# -*- coding: utf-8 -*-
# 生成推荐菜特色
import sys
import jieba
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')


DISH_FILE = 'dish_dict_reduced.txt'
DP_FILE = 'dp.txt'
SHOP_DISH = 'shop_dish.txt'
jieba.load_userdict(DISH_FILE)
jieba.load_userdict(DP_FILE)

# print 'load dictionary OK'

dish_dict = {}
dp_dict = {}
result = {}

for lines in file(SHOP_DISH):
    # print lines.strip().split()
    shop, dish= lines.strip().split()
    if dish_dict.has_key(shop):
        dish_dict[shop].append(dish.decode("utf-8"))
    else:
        dish_dict[shop] = []

for lines in file(DP_FILE):
    # print lines.strip().split()
    dp, feq, flag = lines.strip().split()
    # print dp
    dp_dict[dp.decode("utf-8")] = feq


# print 'processing'



def process(line):

    shop,review = line.split('\t')[0],line.split('\t')[1]
    if shop not in result.keys():
        result[shop] = {}
    current_dish = ''
    seg_list = jieba.cut(review)
    wordlist = list(seg_list)
    for word in wordlist:
        if word in dish_dict[shop]:
            current_dish = word
            # print current_dish
        elif word in dp_dict and len(current_dish) > 0:
            # print word
            if current_dish not in result[shop].keys():
                # result[current_dish] = set([word])
                result[shop][current_dish] = {}
                result[shop][current_dish][word] = 1
            else:
                try:
                    if word in result[shop][current_dish].keys():
                        result[shop][current_dish][word] += 1
                    else:
                        result[shop][current_dish][word] = 1
                except AttributeError, ex:
                    print 'err:',current_dish, result[shop][current_dish], word


# count = 0;
# for lines in open('review_2904247.txt'):
#     count += 1
# print 'total',count

i = 0.0
for line in stdin:
    process(line)
    i += 1
    # if i%100 == 0:
        # print 'count ' + str(i)
    # if i > 5:
    #     break

# print result
for shop in result.keys():
    for dish_item in result[shop].keys():
    # print '---------',dish_item, '---------'
        for dp_item in result[shop][dish_item].keys():
            print shop , dish_item, dp_item , result[shop][dish_item][dp_item]
