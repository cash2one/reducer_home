#encoding=utf-8
import jieba
jieba.load_userdict('dish_dict_reduced.txt')

jieba.load_userdict('dp.txt')
import jieba.posseg as pseg
from collections import deque


dic = {}
dps = {}
for lines in file('dish_dict_reduced.txt'):
    # print lines.strip().split()
    dish, feq, flag = lines.strip().split()
    dic[dish.decode("utf-8")] = feq

for lines in file('dp.txt'):
    # print lines.strip().split()
    dp, feq, flag = lines.strip().split()
    dps[dish.decode("utf-8")] = feq

def process(sentence):

    words = pseg.cut(sentence)
    dishlist = []
    result = {}
    dishStack = []
    vf = False
    tmpw = jieba.posseg.pair('','')
    for w in words:
        if dic.has_key(w.word):
            # print '----'
            dishlist.append(w.word)
            dishCurrent = w.word
            dishStack.append(w.word)
        if w.flag == 'a':
            tmp = w.word
            vf = True
        # elif w.flag in ['v', 'nz'] and tmpw.flag == 'd':
        #     tmp = w.word
        #     # tmp = tmpw.word + w.word
        #     vf = True
        else:
            vf = False

        if vf:
            vf = False
            while len(dishStack) > 0:
                dishCurrent = dishStack.pop()
                if dishStack not in result.keys():
                    result[dishCurrent] = tmp
        # if len(w.word) >= 1:
        #     print w.word, w.flag
        tmpw = w


    print ' '.join(dishlist)
    for item in result.keys():
        print item,result[item]

# for sentence in open('dianping.txt'):
#     process(sentence)

queue = []
aa = set()
result = {}
def process2(sentence):

    seg_list = jieba.cut(sentence)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
    wordlist = list(seg_list)
# print type(seg_list)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
# seg_list.next()
# seg_list.next()
    for  w in wordlist:
        queue.append(w)
    # print w
        if len(queue) >= 20:
            queue.pop(0)
            dishname = queue[3]
            if dic.has_key(dishname):
                if dishname not in aa:
                    aa.add(dishname)
                    result[dishname] = [tuple(queue)]
                else:
                    result[dishname].append(tuple(queue))
                    # print u'菜名------' + dishname
                # print str(queue[4])
                #     print '/'.join(queue)

for sentence in open('review_2904247.txt'):
    process2(sentence)


for line in result[u'意面']:
    print '/'.join(list(line))




#
# seg_list = jieba.cut("预约的中午自助，没想到中午也那么多人。\\\
# 银鳕鱼真是太好吃了！！\\\
# 刺身类的话，都还挺新鲜的~ \\\
# 漏单的情况多少会有，有时候是相近的桌点了一样的东西送错，但是相比别的自助情况算是好很多的啦（哎，最后都没吃上鹅肝= =）\\\
# 这里唯一的甜品是个奶冻，吃了一堆海鲜很腻的时候解腻很好哦~", cut_all=False)
# print "Default Mode:", "/ ".join(seg_list)  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print ", ".join(seg_list)
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print ", ".join(seg_list)