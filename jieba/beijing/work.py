# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
sys.path+=["/Library/Python/2.7/site-packages"]
sys.path.append("/Users/mantou/reducer_home/jieba/DISH_SCRIPT")

from dp_reviewhelper import *

def main(filename,outfile):

    dp_test = dp_reviewhelper()
    dp_test.LoadDishDict('/Users/mantou/reducer_home/jieba/beijing/dish_dict_reduced.txt')
    dp_test.LoadDictDP('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/dp_tasty_dict.txt')
    dp_test.LoadDictDP('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/dp_feeling_dict.txt')
    dp_test.LoadAdj('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/adj.txt')
    dp_test.LoadNeg('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/negtive.txt')
    dp_test.LoadEX('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/daye.txt')
    dp_test.LoadSIMI('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/simi.txt')
    dp_test.LoadShopDish('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/shop_dish2.txt')
    dp_test.LoadNV('/Users/mantou/reducer_home/jieba/DISH_SCRIPT/nv.txt')
    dp_test.excute(filename,outfile)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        outfile = sys.argv[2]
    except IndexError:
        filename = 'review_508715.txt'
        outfile = 'r_python.txt'
    main(filename,outfile)