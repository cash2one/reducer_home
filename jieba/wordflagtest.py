# -*- coding: utf-8 -*-
import jieba.posseg as pseg
words = pseg.cut("我爱吃奶油草莓肉配料配菜坚果,不是不会不至于不太不那么。土豆泥比肯德基的好吃")
for w in words:
    print w.word, w.flag
words = pseg.cut("4078861	拖到现在才点评，实在抱歉。我真的十分喜欢这家店，也不知道为什么，实在是合我的口味。以至于除了他们家的PIZZA和意粉，我都不愿再尝试别家的了。当然也许是我很孤陋寡闻、不见世面的说。  每次去我都会尝试他家每月的特选色拉，从来没有失望过。我总是点老三样，色拉、肉酱意粉、那波里皇后pizza，符合我从一而终的本色，嘻嘻。小朋友去的话会给她点个儿童套餐或点个冰激凌。食材新鲜，价格合理。 服务没的说，很好。服务员往肉酱意粉上撒起芝士粉来真不是盖的，直到你叫够了，他才停手，大大地满足。你若多去一次，餐厅经理就已经记得你了，热情地跟你打招呼。 有些上瘾，以至于老想往那儿去，虽然不贵，但也架不住常去啊，我的银子啊。。。 ")
for w in words:
    print w.word, w.flag
    if w.word in [u'。']:
        print '---------'

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
print len('块钱的蛋糕核算很多')
