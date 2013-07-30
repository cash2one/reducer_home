# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
sys.path+=["/Library/Python/2.7/site-packages"]
import jieba
import jieba.posseg as pseg
from dpgroup import *

reload(sys)
sys.setdefaultencoding('utf-8')

class dp_reviewhelper:

    def __init__(self):

        self.model = ['']
        self.result = {}
        self.shopDish = {}
        self.dpFeeling = set([])
        self.dpTasty = set([])
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
                self.dpFeeling.add(dp.decode("utf-8"))
            elif flag == 'tasty':
                self.dpTasty.add(dp.decode("utf-8"))

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


    def PreProcessing(self, shop, review):

        # review = review.replace(u'了','').replace(u'的','').replace(u'也','')
        review = review.replace(u'了','').replace(u'也','')
        # print shop,'\t',review
        numstop = 0;
        numunit = 0;
        current_dish = ''
        dp_queue = []

        seg_list = pseg.cut(review)
        wlist = list(seg_list)
        # print shop,'\t', wlist
        current_count = 0

        dpglist = []

        for w in wlist:

            dp_queue.append(w)
            numunit += 1
            if w.word == u"。":
                numstop += 1

            if len(dp_queue) > 6:
                dp_queue.pop(0)

            # dish , logdish = self.HasDish(shop, w.word ,'1')

            if w.word in self.alldish:
                current_dish = w.word
                dp_queue[:] = []

            # if logdish is not None:
            #     if dish != logdish:
            #         pass
            #         # print dish, logdish,'***********'
            #     current_dish = logdish
            #     current_count = 0
            #     # print current_dish

            if current_dish != '':
                # print current_dish
                current_count += 1
            else:
                current_count = 0

            if current_count >= 5:
                current_dish = ''
                current_count = 0

            if w.word in set([u',',u'，',u'。',u':',u'!',u'@',u'+',u'.',u'~',u'?',u'！',u'？',u'：',u' ',u'不过',u'其他',u'另外']) and current_dish != '':
                current_dish = ''
                dp_queue[:] = []

            if w.word in (self.dpFeeling) and current_dish != '':
                # print  shop, current_dish , dp_queue

                dpg = dpgroup('dp')
                dpg.setdish(current_dish)
                dpg.setshop(shop)
                dpg.parser(shop, dp_queue, self.adj, self.neg, self.alldish)
        # #
        #         if dpg.noun in set([u'生意',u'店面',u'服务',u'环境',u'时候',u'人']):
        #             continue
        #         elif dpg.noun in set([u'有点',u'口味',u'感觉',u'味道']):
        #             dpg.noun = u''
        #         dpg.groupshow()
                dpglist.append(dpg)
                # print  shop, current_dish , dpg.dp, dpg.adj, dpg.neg, dpg.noun, dpg.detail
        #
        return dpglist

    def ProcessDgp(self, shop, review):

        dpglist = self.PreProcessing(shop,review)

        for dpg in dpglist:

            # if self.GetScore(dpg) == 0:
            #     continue

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


            # if dpg.noun != u'':
            #     cc = dpg.noun
            # elif dpg.verb != u'':
            #     cc = dpg.verb
            # else:
            #     cc = u' '
            # if current_dish not in self.cao.keys():
            #     self.cao[current_dish] = {}
            # self.cao[current_dish][dpg.detail]= cc
            #

    def Show(self):
        for dish in self.shopReview.keys():
            # print dish
            for dp in self.shopReview[dish]:
                # print dp
                maxScore = 0
                dp_toshow = ''
                for dp_detail in self.shopReview[dish][dp]:
                    score = self.shopReview[dish][dp][dp_detail]
                    if score > maxScore:
                        maxScore = score
                        dp_toshow = dp_detail

                if maxScore >= 1 and len(dp_toshow) < 7:
                    # print len(dp_detail)
                    # print self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)
                    print '\t'.join([self.shopid, dish, dp ,dp_toshow,str(maxScore)])

                    self.outfile.writelines('\t'.join([self.shopid, dish, dp ,dp_toshow, str(maxScore)]))
                    self.outfile.writelines('\n')
                # print '\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)])


    def excute(self,review,outfile):

        self.outfile = file(outfile,'w')
        count = 0
        total = 1
        for lines in file(review):
            total +=1
        print total

        for lines in file(review):
            count +=1
            if (count%100==0):
                print count/total

            try:
                shopid = lines.split('\t')[0]
                review = lines.split('\t')[1].decode("utf-8")
            except IndexError, ex:
                continue

            if shopid.strip() == '':
                continue

            if shopid == self.shopid:
                self.ProcessDgp(shopid, review)

            elif self.shopid is None:
                self.shopid = shopid
                self.ProcessDgp(shopid, review)

            elif shopid != self.shopid:

                self.Show()
                self.cao = {}
                self.shopReview = {}
                self.shopid = shopid
                self.ProcessDgp(shopid, review)
                    # break
                    # self.PreProcessing(lines.decode("utf-8"))
                # count += 1
                # if n > 0 and count > n:
                #     break

        self.Show()
        self.cao = {}
        self.shopReview = {}
        self.outfile.close()

def main(filenam,outfile):

    dp_test = dp_reviewhelper()
    dp_test.LoadDishDict('atmos_dict.txt')
    dp_test.LoadDictDP('dp_feeling_dict.txt')
    dp_test.LoadAdj('adj.txt')
    dp_test.LoadNeg('negtive.txt')

    dp_test.excute(filenam,outfile)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        outfile = sys.argv[2]
    except IndexError:
        filename = 'review_sub_hot.txt'
        outfile = 'r_python.txt'
    main(filename,outfile)
# dp_test.show()
