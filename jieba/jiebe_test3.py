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
# DISH_FILE = 'sub_dish_reducered.txt'
DP_FILE = 'dp.txt'
SHOP_DISH = 'shop_dish.txt'
# SHOP_DISH = 'shop_dish_sub.txt'
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

shopReview = {}
out = file('log','w')

for lines in file(ADJ):
    adj, feq, flag = lines.strip().split()
    adj_list.append(adj.decode("utf-8"))


for lines in file(SHOP_DISH):
    shop, dish= lines.strip().split()
    if dish_dict.has_key(shop):
        dish_dict[shop].append(dish.decode("utf-8"))
    else:
        dish_dict[shop] = [dish.decode("utf-8")]

for lines in file(DP_FILE):
    dp, feq, flag = lines.strip().split()
    dp_list.append(dp.decode("utf-8"))

for lines in file(NEGTIVE):
    word, feq, flag = lines.strip().split()
    negtive_list.append(word.decode("utf-8"))


queue = []
aa = set()
result = {}

class shopIter:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.data = []
        self.shopid = None
        self.last = []

    def getOneReview(self):

        res = self.data
        for line in self.file:
            try:
                shopid, reviewbody = line.replace('\n','').split('\t')
            except ValueError as e:
                # print 'split error'
                pass
            else:
                if shopid == self.shopid:
                    self.data.append((shopid,reviewbody))
                elif self.shopid is None:
                    self.shopid = shopid
                    self.data.append((shopid,reviewbody))
                else:
                    res = self.data
                    self.data = [(shopid,reviewbody)]
                    self.shopid = shopid
                    break

        if res != self.last:
            self.last = res
            for l in res:
                yield l
        else:
            yield StopIteration()


class dpgroup:

    def __init__(self , dp):
        self.dish = ''
        self.shop = ''
        self.dp = dp
        self.adj = ''
        self.noun = ''
        self.neg = ''
        self.detail = ''

    def setshop(self, shop):
        self.shop = shop

    def setdish(self, dish):
        self.dish = dish

    def setadj(self,adj):
        self.adj = adj

    def setnoun(self,noun):
        self.noun = noun

    def setneg(self,neg):
        self.neg = neg

    def parser(self,shop,l):


        self.dp = l.pop().word

        idx = len(l)
        lword = [w.word for w in l]

        for w in list(reversed(l)):

            if w.word in adj_list:
                self.setadj(w.word)
                # self.adj = w.word
                idx = l.index(w)
                continue
            elif w.word in negtive_list:
                self.setneg(w.word)
                # self.neg = w.word
                idx = l.index(w)
                continue
            elif w.flag in ['n','nr'] and (w.word not in dish_dict[shop]):
                # self.noun = w.flag
                self.setnoun(w.word)
                idx = l.index(w)
                continue
            elif w.word == u'比':
                # idx = lword.index(w.word)
                idx = l.index(w)
                break
            else:
                break

        # print idx
        # print '/'.join([ w for w in lword[idx:]]) + '/' + self.dp
        self.detail = ''.join([w for w in lword[idx:]])+self.dp
        # print self.detail+'----'+'/'.join([self.shop,self.dish, self.noun, self.neg, self.adj, self.dp])

    def groupshow(self):
        print 'parser:' + '/'.join([self.shop,self.dish, self.noun, self.neg, self.adj, self.dp])

def preprocessing(line):

    shop,review = line.split('\t')[0],line.split('\t')[1]
    review = review.replace(u'了','').replace(u'的','').replace(u'也','')
    # print shop,'\t',review
    current_dish = ''
    high_dp = []
    seg_list = pseg.cut(review)
    wlist = list(seg_list)
    # print shop,'\t', wlist
    current_count = 0
    dpglist = []

    for w in wlist:
        high_dp.append(w)
        if len(high_dp) > 5:
            high_dp.pop(0)
        if w.word in dish_dict[shop]:
            current_dish = w.word
            # print current_dish

        if current_dish != '':
            current_count += 1
        else:
            current_count = 0

        if current_count >= 10:
            current_dish = ''
            current_count = 0

        if w.word in [u'。',u':',u'!',u'@',u'+',u'.',u'~',u'?',u'！',u'？',u'：',u' '] and current_dish != '':
            current_dish = ''
            high_dp[:] = []
        if w.word in dp_list and current_dish != '':
            # print  shop, current_dish , high_dp

            dpg = dpgroup('dp')
            dpg.setdish(current_dish)
            dpg.setshop(shop)
            dpg.parser(shop, high_dp)

            if dpg.noun in [u'店面',u'服务',u'环境',u'时候',u'人']:
                continue
            # dpg.groupshow()
            dpglist.append(dpg)
            # print  shop, current_dish , dpg.dp, dpg.adj, dpg.neg, dpg.noun

    return dpglist

def processdpg(line,result,shopReview):

    shop,review = line.split('\t')[0],line.split('\t')[1]
    if shop not in result.keys():
        result[shop] = {}
    dpglist = preprocessing(line)

    for dpg in dpglist:

        current_dish = dpg.dish
        # dp_extend = dpg.noun + dpg.neg + dpg.adj + dpg.dp
        dp = dpg.neg + dpg.dp
        dp_extend = dpg.detail
        # if current_dish == u'红豆糕':
        #     print '-'.join([current_dish,dp,dp_extend])
        if not shopReview.has_key(dp):
            shopReview[dp] = {}
            shopReview[dp][dp_extend] = 1
        elif dp_extend not in shopReview[dp].keys():
            shopReview[dp][dp_extend] = 1
        else:
            shopReview[dp][dp_extend] += 1

        # if len(dp_extend) > len(dp) and result[shop][dp]

        if current_dish not in result[shop].keys():
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
    return result, shopReview


# def process(line):
#
#     shop,review = line.split('\t')[0],line.split('\t')[1]
#     if shop not in result.keys():
#         result[shop] = {}
#     current_dish = ''
#     review = preprocessing(line)
#     seg_list = pseg.cut(review)
#     wlist = list(seg_list)
#
#     w_before = ''
#     for w in wlist:
#         if w.word in ['。',';']:
#             pass
#             current_dish = ''
#         elif w.word in dish_dict[shop]:
#             current_dish = w.word
#
#         elif w.word in dp_list and len(current_dish) > 0:
#             dp = w.word
#             if w_before.word in negtive_list or (w_before.flag == 'n' and w_before.word not in dish_dict[shop]):
#                 dp = w_before.word + w.word
#                 # print '/'.join([current_dish,w_before.word,w_before.flag,w.word,w.flag])
#             # print word
#             if current_dish not in result[shop].keys():
#                 # result[current_dish] = set([word])
#                 result[shop][current_dish] = {}
#                 result[shop][current_dish][dp] = 1
#             else:
#                 try:
#                     if dp in result[shop][current_dish].keys():
#                         result[shop][current_dish][dp] += 1
#                     else:
#                         result[shop][current_dish][dp] = 1
#                 except AttributeError, ex:
#                     print 'err:',current_dish, result[shop][current_dish], dp
#
#             # print 'log:',shop,current_dish, dp
#
#         w_before = w

def show(result,shopReview):
    # print ' '.join(shopReview.keys())
    # for dp in shopReview.keys():
        # for dp_detail in shopReview[dp]:
            # print ' '.join([dp_detail,str(shopReview[dp][dp_detail])])
    # print ' '.join([shopReview[w] for w in shopReview.keys()])
    for shop in result.keys():
        for dish_item in result[shop].keys():
            # print '---------',dish_item, '---------'
            for dp_item in result[shop][dish_item].keys():

                dp_detal = dp_item
                score = result[shop][dish_item][dp_item]

                for dd in shopReview[dp_item].keys():
                    if shopReview[dp_item][dd] <= 1:
                        continue
                    if score < shopReview[dp_item][dd]*len(dd):
                        score = shopReview[dp_item][dd]*len(dd)
                        # print dd , shopReview[dp_item][dd],score
                        dp_detal = dd
                        # print dp_detal
                if score > 1 and dp_detal != u'好':
                    print ' '.join([str(shop) , str(dish_item),str(dp_detal) , str(score)])

count = 0
for lines in open(REVIEW_FILE):
    count += 1
# print count

def showdp():


    iter = shopIter(REVIEW_FILE)
    end = True
    shopnum = 0
    i = 0

    while end:
        shopnum += 1
        result = {}
        shopReview = {}
        for l in iter.getOneReview():
            # print l
            ll = list(l)
            if len(ll) == 0:
                end = False
                break
            line = '\t'.join(ll)

            shop = line.split('\t')[0]

            line = line.upper()
            # print i
            i += 1
            # if shop != '1945402':
            #      break
            result, shopReview = processdpg(line.decode("utf-8"),result,shopReview)
        # i += 1
        #     if i > 50:
        #         break
            if i%100 == 0:
                out.write('count ' + str(i) + ' ' + str (i/count) + '%\n')

        # print shopReview
        # print '------'
        show(result,shopReview)

        # if shopnum >= 3:
        #     break
        result = {}
        shopReview = {}




showdp()
out.close()