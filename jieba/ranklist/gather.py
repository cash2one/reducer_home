# -*- coding: utf-8 -*-
__author__ = 'mantou'

id  = None
count = 0
dict = {}
out = file("gout.txt",'w')
def show(shopid,dict):
    for item in dict.keys():
        print shopid,item.replace('\n',''),str(dict[item])
        # print '\t'.join([shopid,item,str(dict[item])])
        out.writelines('\t'.join([shopid,item.replace('\n',''),str(dict[item])])+'\n')


for line in file("out.txt"):

    shopid = line.split('\t')[0]
    wordlist = line.split('\t')[1:]
    # print shopid,wordlist

    if shopid == id:
        pass
    else:
        count += 1
        show(id ,dict)
        id = shopid
        # show(shopid,dict)
        dict = {}
    for w in wordlist:
        if dict.has_key(w):
            dict[w] += 1
        else:
            dict[w] = 1

    # break

out.close()