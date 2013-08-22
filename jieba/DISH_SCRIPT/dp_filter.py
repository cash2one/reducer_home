# -*- coding: utf-8 -*-
from __future__ import division
import sys
__author__ = 'mantou'

nv_dict = set([])
dp_feeling = set([])
outfile = file("/Users/mantou/reducer_home/jieba/beijing/dp2_0815_a.txt",'w')


def loaddata():
    for line in file("nv.txt"):
        nv = line.split()[0]
        nv_dict.add(nv)
    for line in file("dp_feeling_dict.txt"):
        feeling = line.split()[0]
        dp_feeling.add(feeling)


def show(shop,shopReview):
    for dish in shopReview.keys():

        for dp in shopReview[dish]:
    #             # print dp
    #             if dp in dpFeeling:
    #                 type = 'f'
    #             else:
    #                 type = 't'
            maxScore = 0
            dp_toshow = ''
            for simple in shopReview[dish][dp]:
                score = shopReview[dish][dp][simple]

                if score > maxScore:
                    maxScore = score
                    dp_toshow = simple
    #
            if maxScore >= 1 and len(dp_toshow) < 8:
                print '\t'.join([shop, dish, dp , simple, str(score)])
                outfile.writelines('\t'.join([shop, dish, dp , simple, str(score)]))
                outfile.writelines('\n')

    #
    #                 pass
                    # print len(dp_detail)
                    # print shopid, dish, dp ,type,dp_toshow, cao[dp_toshow],str(maxScore)

                    # outfile.writelines('\t'.join([shopid, dish, dp ,type,dp_toshow, cao[dish][dp_toshow],str(maxScore)]))
                    # outfile.writelines('\n')
                # print '\t'.join([shopid, dish, dp ,type,dp_toshow, cao[dp_toshow],str(maxScore)])

def filter(filename):

    shopReview = {}
    shopBefore = None
    for line in file(filename):

        shop, dish, verb ,noun, neg, adj, dp, detail, simple = line.replace('\n','').split('\t')

        if dish.decode("utf-8") == u"没有":
            continue
        if dp in dp_feeling and len(verb+noun) == 0:
            continue
        adj = adj.decode("utf-8")
        if adj == u'有':
            continue
        if neg.decode("utf_8") == u"没有":
            simple = detail

        if shop != shopBefore:
            show(shopBefore,shopReview)
            shopReview = {}
            shopBefore = shop

        if len(verb+noun) > 0 and (verb+noun) not in nv_dict:
            # print verb+noun
            # print line
            continue
        else:
            dp = neg + dp
            if dish not in shopReview.keys():
                shopReview[dish] = {}
        #
            if not shopReview[dish].has_key(dp):
                shopReview[dish][dp] = {}
                shopReview[dish][dp][simple] = 1
            elif simple not in shopReview[dish][dp].keys():
                shopReview[dish][dp][simple] = 1
            else:
                shopReview[dish][dp][simple] += 1

        #
        #
        #     if noun != u'':
        #         cc = noun
        #     elif verb != u'':
        #         cc = verb
        #     else:
        #         cc = u' '
        #     if dish not in cao.keys():
        #         cao[dish] = {}
        #     cao[dish][detail]= cc

if __name__ == '__main__':

    try :
        filename = sys.argv[1]
    except IndexError:
        filename = "/Users/mantou/reducer_home/jieba/beijing/dp2_0815.txt"

    loaddata()
    filter(filename)


