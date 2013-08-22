# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
sys.path+=["/Library/Python/2.7/site-packages"]
import jieba
import jieba.posseg as pseg
from dpgroup import *
from xpinyin import Pinyin
p = Pinyin()

reload(sys)
sys.setdefaultencoding('utf-8')

class dp_reviewhelper:

    ODC = "OTHER DISH"

    def __init__(self):

        self.model = ['']
        self.result = {}
        self.shopDish = {}
        self.dpFeeling = set([])
        self.dpTasty = set([])
        self.dpTastyP = {}
        self.dpFeelingP = {}
        self.neg = []
        self.adj = []
        self.cao = {}
        self.nvset = set([])
        self.shopReview = {}
        self.shopid = None
        self.file = ''
        self.alldish = set([])
        self.simi = {}
        self.dishpy = {}



    def GetScore(self , dpg):
        if dpg.dp in self.dpTasty:
            return 1
        elif dpg.dp in self.dpFeeling:
            if dpg.noun != '' and  dpg.noun in self.nvset:
                return 1
            else:
                return 0
        return 0


    def LoadDictDP(self,DP_dict):
        jieba.load_userdict(DP_dict)
        for lines in file(DP_dict):
            dp, feq, flag = lines.strip().split()
            d = dp.decode("utf-8")
            if flag == 'feeling':
                self.dpFeeling.add(d)
                self.dpFeelingP[p.get_pinyin(d)] = d
            elif flag == 'tasty':
                self.dpTasty.add(d)
                self.dpTastyP[p.get_pinyin(d)] = d

    def LoadDishDict(self,DISH_DICT):
        jieba.load_userdict(DISH_DICT)
        for lines in file(DISH_DICT):
            dish, feq, flag = lines.strip().split()
            # print dish
            self.alldish.add(dish.decode("utf-8"))

    def LoadShopDish(self, SHOP_DISH):
        self.shopDish = {}
        for lines in file(SHOP_DISH):
            # print lines
            shop, dish= lines.strip().split('\t')
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

    def LoadEX(self,f):
        jieba.load_userdict(f)

    def LoadNV(self,f):
        for line in file(f):
            n = line.split()[0]
            self.nvset.add(n.decode('utf-8'))

    def LoadSIMI(self,f):
        for line in file(f):
            w = line.split()[0].decode('utf-8')
            s = line.split()[1].decode('utf-8')
            self.simi[w] = s

    def LoadModel(self):
        ' '

    def HasDish(self,shop, dish, model = '1'):
        if model == '1':
            py = p.get_pinyin(dish)

            # total match
            # if shop == None:
            #     return dish,None
            # print self.shopDish[shop]
            if not self.shopDish.has_key(shop):
                return dish,None
            if dish in self.shopDish.get(shop):
                # print dish
                return dish,dish
            if self.dishpy.has_key(py):
                return dish,self.dishpy[py]
            elif dish in self.alldish:
                for longdish in self.shopDish.get(shop):
                    if longdish.find(dish) >= 0 and len(longdish) >= 3:
                        # print dish,'------------->',longdish
                        # we can find
                        return dish,longdish
                # other dish
                return dish, None
            # go on
            return dish,None


    def PreProcessing(self, shop, review):

        # review = review.replace(u'了','').replace(u'的','').replace(u'也','')
        review = review.replace(u'～',u'').replace(u'了',u'').replace(u'也',u'').replace(u"'",u'').replace(u'"',u'').replace(u"[",u'').replace(u"；",u'')
        review = review.replace(u'~',u'').replace(u']',u'').replace(u'【',u'').replace(u'】',u'').replace(u'”',u'').replace(u"’",u'').replace(u"“",u'')

        for key in self.simi.keys():
            review = review.replace(key,self.simi[key])
        del key

        review = review.upper()
        # print shop,'\t',review
        numstop = 0;
        numunit = 0;
        current_dish = ''
        dp_queue = []

        seg_list = pseg.cut(review)
        wlist = list(seg_list)
        print shop,'\t', wlist
        current_count = 0

        dpglist = []

        for w in wlist:

            dp_queue.append(w)
            numunit += 1
            if w.word == u"。":
                numstop += 1

            if len(dp_queue) > 5:
                dp_queue.pop(0)

            dish ,logdish = self.HasDish(shop, w.word ,'1')

            if logdish is not None:
                # get one dish

                if dish != logdish:
                    # pass
                    # print dish, logdish,'***********'
                    current_dish = logdish
                else:
                    current_dish = dish
                dp_queue[:] = []
                current_count = 0
                continue


            if current_dish != '':
                # print current_dish
                current_count += 1
            else:
                current_count = 0

            if current_count >= 15:
                current_dish = ''
                current_count = 0

            if w.word in {u'店里',u'饮料',u'、',u':',u'!',u'@',u'+',u'.',u'~',u'?',u'！',u'？',u'：',u'其他',u'另外'} and current_dish != '':
                current_dish = ''
                dp_queue[:] = []
                continue

            if len(w.word) > 1:
                dp_pinyin = p.get_pinyin(w.word)
                dp = w.word
                if dp_pinyin in self.dpTastyP.keys() and current_dish != '' :
                    dp = self.dpTastyP[dp_pinyin]
                    # print dp_pinyin, dp
                elif dp_pinyin in self.dpFeelingP.keys() and current_dish != '':
                    dp = self.dpFeelingP[dp_pinyin]
                    # print dp_pinyin, dp
                w.word = dp

            if w.word in (self.dpTasty | self.dpFeeling) and current_dish != '':

                print  shop, current_dish , dp_queue,  p.get_pinyin(w.word)
                dpg = dpgroup('dp')
                dpg.setdish(current_dish)
                dpg.setshop(shop)
                dp_queue2 = dp_queue[:]
                dpg.parser(shop, dp_queue2, self.adj, self.neg, self.shopDish.get(shop))
        #
                # if dpg.noun in {u'生意',u'店面',u'服务',u'环境',u'象',u'时候',u'人'}:
                #     continue
                # elif dpg.noun in {u'有点',u'口味',u'感觉',u'味道'}:
                #     dpg.noun = u''

                # dpg.groupshow()
                self.outfile.writelines('\t'.join([dpg.shop,dpg.dish, dpg.verb ,dpg.noun, dpg.neg, dpg.adj, dpg.dp, dpg.detail, dpg.simple]))
                print '\t'.join([dpg.shop,dpg.dish, dpg.verb ,dpg.noun, dpg.neg, dpg.adj, dpg.dp, dpg.detail, dpg.simple])
                self.outfile.writelines('\n')

                dp_queue[:] = []
                # dpglist.append(dpg)
                # print  shop, current_dish , dpg.dp, dpg.adj, dpg.neg, dpg.noun, dpg.detail
        #
        return dpglist

    def ProcessDgp(self, shop, review):
        dpglist = self.PreProcessing(shop,review)
        #
        # for dpg in dpglist:
        #
        #     if self.GetScore(dpg) == 0:
        #         continue
        #
        #     current_dish = dpg.dish
        #     dp = dpg.neg + dpg.dp
        #
        #     if current_dish not in self.shopReview.keys():
        #         self.shopReview[current_dish] = {}
        #
        #     if not self.shopReview[current_dish].has_key(dp):
        #         self.shopReview[current_dish][dp] = {}
        #         self.shopReview[current_dish][dp][dpg.detail] = 1
        #     elif dpg.detail not in self.shopReview[current_dish][dp].keys():
        #         self.shopReview[current_dish][dp][dpg.detail] = 1
        #     else:
        #         self.shopReview[current_dish][dp][dpg.detail] += 1
        #
        #
        #     if dpg.noun != u'':
        #         cc = dpg.noun
        #     elif dpg.verb != u'':
        #         cc = dpg.verb
        #     else:
        #         cc = u' '
        #     if current_dish not in self.cao.keys():
        #         self.cao[current_dish] = {}
        #     self.cao[current_dish][dpg.detail]= cc
        #     #

    # def Show(self):
    #     for dish in self.shopReview.keys():
    #         # print dish
    #         for dp in self.shopReview[dish]:
    #             # print dp
    #             if dp in self.dpFeeling:
    #                 type = 'f'
    #             else:
    #                 type = 't'
    #             maxScore = 0
    #             dp_toshow = ''
    #             for dp_detail in self.shopReview[dish][dp]:
    #                 score = self.shopReview[dish][dp][dp_detail]
    #                 if score > maxScore:
    #                     maxScore = score
    #                     dp_toshow = dp_detail
    #
    #             if maxScore >= 1 and len(dp_toshow) < 8:
    #
    #                 pass
                    # print len(dp_detail)
                    # print self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)
                    # print '\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dish][dp_toshow],str(maxScore)])

                    # self.outfile.writelines('\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dish][dp_toshow],str(maxScore)]))
                    # self.outfile.writelines('\n')
                # print '\t'.join([self.shopid, dish, dp ,type,dp_toshow, self.cao[dp_toshow],str(maxScore)])


    def excute(self,review,outfile):

        self.outfile = file(outfile,'w')
        count = 0
        total = 1
        for lines in file(review):
            total +=1
        # print total

        for lines in file(review):
            count +=1
            if (count%50==0):
                print count/total

            try:
                shopid = lines.split('\t')[0].strip()
                review = lines.split('\t')[1].decode("utf-8")
            except IndexError, ex:
                continue

            if shopid.strip() == '':
                continue

            # if shopid == self.shopid:
                # self.ProcessDgp(shopid, review)

            # elif self.shopid is None:
            #     self.shopid = shopid
            #     # self.ProcessDgp(shopid, review)

            elif shopid != self.shopid:

                # self.Show()
                # self.cao = {}
                self.dishpy = {}
                for item in self.shopDish[shopid]:
                    self.dishpy[p.get_pinyin(item)]= item
                    print self.dishpy
                self.shopReview = {}
                self.shopid = shopid

            self.ProcessDgp(shopid, review)
                    # break
                    # self.PreProcessing(lines.decode("utf-8"))
                # count += 1
                # if n > 0 and count > n:
                #     break

        # self.Show()
        # self.cao = {}
        self.shopReview = {}
        self.outfile.close()

