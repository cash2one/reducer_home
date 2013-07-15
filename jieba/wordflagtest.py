# -*- coding: utf-8 -*-
import jieba.posseg as pseg
words = pseg.cut("我爱吃奶油草莓肉配料配菜坚果,不是不会不至于不太不那么。；")
for w in words:
    print w.word, w.flag
words = pseg.cut("我爱吃奶油草莓肉配料配菜坚果,不是不会不至于不太不那么。有点甜很特别好吃非常棒超爱超级不错太老")
for w in words:
    print w.word, w.flag

adj_list = [u'很', u'太', u'特别', u'非常']
def preprocessing(review):

    seg_list = pseg.cut(review)
    wlist = list(seg_list)
    print '/'.join([w.word for w in wlist])
    for w in wlist:
        if w.word in adj_list and w.flag == 'd':

            print w.word, w.flag
            review = review.replace(w.word, ' ')
            print review
    return review

print preprocessing(u"我爱吃奶油草莓肉配料配菜坚果,不是不会不至于不太不那么。有点甜很特别好吃非常棒超爱超级不错太老")