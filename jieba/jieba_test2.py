# -*- coding: utf-8 -*-
# 生成推荐菜特色
import sys
import jieba
from sys import stdin
reload(sys)
sys.setdefaultencoding('utf-8')

REVIEW_FILE = sys.argv[1]
DISH_FILE = 'dish_dict_reduced.txt'
DP_FILE = 'dp.txt'
SHOP_DISH = 'shop_dish.txt'
NEGTIVE = 'negtive.txt'
jieba.load_userdict(DISH_FILE)
jieba.load_userdict(DP_FILE)
jieba.load_userdict(NEGTIVE)

dish_dict = {}
dp_dict = {}
result = {}
negtive_list = []

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

for lines in file(NEGTIVE):
    word, feq, flag = lines.strip().split()
    negtive_list.append(word.decode("utf-8"))

queue = []
aa = set()
result = {}

def process(line):

    shop,review = line.split('\t')[0],line.split('\t')[1]
    if shop not in result.keys():
        result[shop] = {}
    current_dish = ''
    seg_list = jieba.cut(review)
    wordlist = list(seg_list)
    word_before = ''
    for word in wordlist:
        if word in dish_dict[shop]:
            current_dish = word
            # print current_dish
        elif word in dp_dict and len(current_dish) > 0:
            dp = word
            if word_before in negtive_list:
                dp = word_before + word
                print dp
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

        word_before = word


def process2(sentence):

    seg_list = jieba.cut(sentence)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
    wordlist = list(seg_list)
# print type(seg_list)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
    for w in wordlist:
        queue.append(w)
    # print w
        if len(queue) >= 25:
            queue.pop(0)
            negword = queue[5]
            if negword in negtive_list:
                if negword not in aa:
                    aa.add(negword)
                    result[negword] = [tuple(queue)]
                else:
                    result[negword].append(tuple(queue))
                    # print u'菜名------' + negword
                # print str(queue[4])
                #     print '/'.join(queue)


def show(result):
    for shop in result.keys():
        for dish_item in result[shop].keys():
    # print '---------',dish_item, '---------'
            for dp_item in result[shop][dish_item].keys():
                print '\x01'.join([str(shop) , str(dish_item),str(dp_item) , str(result[shop][dish_item][dp_item])])


def showword():

    for sentence in open(REVIEW_FILE):
        process2(sentence)

    for line in result[u'不']:
        print ''.join(list(line))


def showdp():

    for line in open(REVIEW_FILE):
        process(line)

    show(result)

# showword()
showdp()
    # i += 1
    # if i > 1000 == 0:
    #     break
    # if i%100 == 0:
    #      out.write('count ' + str(i) + ' ' + str (i/count) + '%\n')
    # # if i > 5:
    # #     break

# s ='5478499	噱头大于实质，无非就是一家中式铁板烧，排队人老多老多的。每个菜都很咸，调味过度，菜量也很少。蒜香大虾，味道凑合，量少，羊排和什锦炒饭不推荐，真心没啥好吃的。六点半左右厨师都会放下手里的大勺集团跳骑马舞，这年头真心搵食不易啊，厨师还要会跳舞。'
# seg_list = jieba.cut(s)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
# process(s)