# -*- coding: utf-8 -*-
import os
import jieba
import jieba.posseg as pseg
from dpgroup import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class dp_reviewhelper:

    def __init__(self):

        self.model = ['']
        self.result = {}
        self.shopDish = {}
        self.dpFeeling = []
        self.dpTasty = []
        self.neg = []
        self.adj = []
        self.cao = {}
        self.shopReview = {}
        self.shopid = None
        self.file = ''
        self.alldish = set([u'ma'])


    def GetScore(self , dpg):
        if dpg.dp in self.dpTasty:
            return 1
        elif dpg.dp in self.dpFeeling:
            if dpg.noun != '' or dpg.noun != '':
                return 1
        return 0


    def LoadDictDP(self,DP_dict):
        jieba.load_userdict(DP_dict)
        for lines in file(DP_dict):
            dp, feq, flag = lines.strip().split()
            if flag == 'feeling':
                self.dpFeeling.append(dp.decode("utf-8"))
            elif flag == 'tasty':
                self.dpTasty.append(dp.decode("utf-8"))

    def LoadDishDict(self,DISH_DICT):
        jieba.load_userdict(DISH_DICT)
        for lines in file(DISH_DICT):
            dish, feq, flag = lines.strip().split()
            # print dish
            self.alldish.add(dish.decode("utf-8"))


    def LoadShopDish(self, SHOP_DISH):
        self.shopDish = {}
        for lines in file(SHOP_DISH):
            shop, dish= lines.strip().split()
            if self.shopDish.has_key(shop):
                self.shopDish[shop].append(dish.decode("utf-8"))
            else:
                self.shopDish[shop] = [dish.decode("utf-8")]

    def LoadNeg(self, Neg):
        jieba.load_userdict(Neg)
        for lines in file(Neg):
            word, feq, flag = lines.strip().split()
            self.neg.append(word.decode("utf-8"))

    def LoadAdj(self, ADJ):
        jieba.load_userdict(ADJ)
        for lines in file(ADJ):
            adj, feq, flag = lines.strip().split()
            self.adj.append(adj.decode("utf-8"))

    def LoadModel(self):
        ' '

    def HasDish(self,shop, dish, model = '1'):
        if model == '1':
            # total match
            if dish in self.shopDish[shop]:
                # print dish
                return dish,dish
            elif dish in self.alldish:
                for longdish in self.shopDish[shop]:
                    if longdish.find(dish) >= 0 and len(longdish) >= 5:
                        # print dish,'------------->',longdish
                        return dish,longdish
            return dish,None




    def PreProcessing(self, body):


        shop,review = body.strip().split('\t')[0],body.strip().split('\t')[1]

        dishs = self.shopDish[shop]

        # review = review.replace(u'了','').replace(u'的','').replace(u'也','')
        review = review.replace(u'了','').replace(u'也','')
        # print shop,'\t',review

        current_dish = ''
        dp_queue = []

        seg_list = pseg.cut(review)
        wlist = list(seg_list)
        # print shop,'\t', wlist
        current_count = 0

        dpglist = []

        for w in wlist:
            dp_queue.append(w)
            if len(dp_queue) > 5:
                dp_queue.pop(0)

            dish , logdish = self.HasDish(shop, w.word ,'1')

            if logdish is not None:
                if dish != logdish:
                    pass
                    # print dish, logdish,'***********'
                current_dish = logdish
                current_count = 0
                # print current_dish

            if current_dish != '':
                # print current_dish
                current_count += 1
            else:
                current_count = 0

            if current_count >= 10:
                current_dish = ''
                current_count = 0

            if w.word in [u':',u'!',u'@',u'+',u'.',u'~',u'?',u'！',u'？',u'：',u' ',u'其他',u'另外'] and current_dish != '':
                current_dish = ''
                dp_queue[:] = []

            if w.word in (self.dpTasty + self.dpFeeling) and current_dish != '':
                # print  shop, current_dish , dp_queue

                dpg = dpgroup('dp')
                dpg.setdish(current_dish)
                dpg.setshop(shop)
                dpg.parser(shop, dp_queue, self.adj, self.neg, self.shopDish[shop])
        #
                if dpg.noun in [u'口味',u'感觉',u'味道',u'生意',u'店面',u'服务',u'环境',u'时候',u'人']:
                    continue
                # dpg.groupshow()
                dpglist.append(dpg)
                print  shop, current_dish , dpg.dp, dpg.adj, dpg.neg, dpg.noun, dpg.detail
        #
        return dpglist

    def ProcessDgp(self, line):

        try:
            shop,review = line.strip().split('\t')[0],line.strip().split('\t')[1]
        except IndexError, ex:
            return

        if shop not in self.result.keys():
            self.result[shop] = {}

        dpglist = self.PreProcessing(line)

        for dpg in dpglist:

            if self.GetScore(dpg) == 0:
                continue

            current_dish = dpg.dish
            dp = dpg.neg + dpg.dp

            if current_dish not in self.shopReview.keys():
                self.shopReview[current_dish] = {}

            if not self.shopReview[current_dish].has_key(dp):
                self.shopReview[current_dish][dp] = {}
                self.shopReview[current_dish][dp][dpg.detail] = 1
            elif dpg.detail not in self.shopReview[current_dish][dp].keys():
                self.shopReview[current_dish][dp][dpg.detail] = 1
            else:
                self.shopReview[current_dish][dp][dpg.detail] += 1


            if dpg.noun != u'':
                cc = dpg.noun
            elif dpg.verb != u'':
                cc = dpg.verb
            else:
                cc = u' '
            self.cao[dpg.detail]= cc
            #

    def Show(self):
        for dish in self.shopReview.keys():
            # print dish
            for dp in self.shopReview[dish]:
                # print dp
                if dp in self.dpFeeling:
                    type = 'f'
                else:
                    type = 't'
                maxScore = 0
                dp_toshow = ''
                for dp_detail in self.shopReview[dish][dp]:
                    score = self.shopReview[dish][dp][dp_detail]
                    if score > maxScore:
                        maxScore = score
                        dp_toshow = dp_detail

                if maxScore >= 1 and len(dp_detail) < 8:
                    # print self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)
                    print '\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)])
                # print '\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)])


    def excute(self,review,n = 0):

        count = 0

        for lines in file(review):

            try:
                shopid = lines.split('\t')[0]
            except IndexError, ex:
                continue

            if shopid.strip() == '':
                continue

            if shopid == self.shopid:
                self.ProcessDgp(lines.decode("utf-8"))

            elif self.shopid is None:
                self.shopid = shopid
                self.ProcessDgp(lines.decode("utf-8"))

            elif shopid != self.shopid:

                self.Show()
                self.cao = {}
                self.shopReview = {}
                self.shopid = shopid
                self.ProcessDgp(lines.decode("utf-8"))
                    # break
                    # self.PreProcessing(lines.decode("utf-8"))
                # count += 1
                # if n > 0 and count > n:
                #     break

        self.Show()
        self.cao = {}
        self.shopReview = {}


def main(filenam):

    dp_test = dp_reviewhelper()
    dp_test.LoadDishDict('dish_dict_reduced.txt')
    dp_test.LoadShopDish('shop_dish.txt')
    dp_test.LoadDictDP('dish_dict_reduced.txt')
    dp_test.LoadDictDP('dp_tasty_dict.txt')
    dp_test.LoadDictDP('dp_feeling_dict.txt')
    dp_test.LoadAdj('adj.txt')
    dp_test.LoadNeg('negtive.txt')

    dp_test.excute(filenam)

if __name__ == '__main__':

    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'review_2873341_sub.txt'
    main(filename)
# dp_test.show()
