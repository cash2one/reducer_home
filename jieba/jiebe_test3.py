# -*- coding: utf-8 -*-
# 生成推荐菜特色
import sys
import jieba
from sys import stdin
import jieba.posseg as pseg


reload(sys)
sys.setdefaultencoding('utf-8')

REVIEW_FILE = sys.argv[1]
DISH_FILE = 'dish_dict_reduced.txt'
DP_FILE = 'dp.txt'
SHOP_DISH = 'shop_dish.txt'
NEGTIVE = 'negtive.txt'
ADJ = 'adj.txt'


jieba.load_userdict(ADJ)
jieba.load_userdict(DISH_FILE)
jieba.load_userdict(DP_FILE)
jieba.load_userdict(NEGTIVE)


dish_dict = {}
dp_list = []
result = {}
negtive_list = []
adj_list = []


for lines in file(ADJ):
    adj, feq, flag = lines.strip().split()
    adj_list.append(adj.decode("utf-8"))


for lines in file(SHOP_DISH):
    shop, dish= lines.strip().split()
    if dish_dict.has_key(shop):
        dish_dict[shop].append(dish.decode("utf-8"))
    else:
        dish_dict[shop] = []

for lines in file(DP_FILE):
    dp, feq, flag = lines.strip().split()
    dp_list.append(dp.decode("utf-8"))

for lines in file(NEGTIVE):
    word, feq, flag = lines.strip().split()
    negtive_list.append(word.decode("utf-8"))


queue = []
aa = set()
result = {}


def preprocessing(review):

    seg_list = pseg.cut(review)
    wlist = list(seg_list)
    for w in wlist:
        if w.word in adj_list:
            # print w.word, w.flag
            review = review.replace(w.word, ' ')
    print review
    # print '/'.join([w.word for w in wlist])
    return review

def process(line):

    shop,review = line.split('\t')[0],line.split('\t')[1]
    if shop not in result.keys():
        result[shop] = {}
    current_dish = ''
    review = preprocessing(review)
    seg_list = pseg.cut(review)
    wlist = list(seg_list)

    w_before = ''
    for w in wlist:
        if w.word in ['。',';']:
            pass
            current_dish = ''
        elif w.word in dish_dict[shop]:
            current_dish = w.word

        elif w.word in dp_list and len(current_dish) > 0:
            dp = w.word
            if w_before.word in negtive_list or (w_before.flag == 'n' and w_before.word not in dish_dict[shop]):
                dp = w_before.word + w.word
                print '/'.join([current_dish,w_before.word,w_before.flag,w.word,w.flag])
            # print word
            if current_dish not in result[shop].keys():
                # result[current_dish] = set([word])
                result[shop][current_dish] = {}
                result[shop][current_dish][dp] = 1
            else:
                try:
                    if dp in result[shop][current_dish].keys():
                        result[shop][current_dish][dp] += 1
                    else:
                        result[shop][current_dish][dp] = 1
                except AttributeError, ex:
                    print 'err:',current_dish, result[shop][current_dish], dp

            # print 'log:',shop,current_dish, dp

        w_before = w

def show(result):
    for shop in result.keys():
        for dish_item in result[shop].keys():
            print '---------',dish_item, '---------'
            for dp_item in result[shop][dish_item].keys():
                print '\x01'.join([str(shop) , str(dish_item),str(dp_item) , str(result[shop][dish_item][dp_item])])

def showdp():

    i = 0
    for line in open(REVIEW_FILE):
        shop = line.split('\t')[0]
        process(line)
        i += 1
        if i > 100:
            break
    show(result)

showdp()