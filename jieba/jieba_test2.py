
import jieba.posseg as pseg

for line in open('review_2904247.txt'):

    words =  pseg.cut(line)
    for w in words:
        print w.word, w.flag