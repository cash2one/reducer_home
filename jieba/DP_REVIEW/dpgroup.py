# -*- coding: utf-8 -*-
import sys

class dpgroup:

    def __init__(self , dp):
        self.dish = ''
        self.shop = ''
        self.dp = dp
        self.adj = ''
        self.noun = ''
        self.neg = ''
        self.detail = ''
        self.verb = ''

    def setshop(self, shop):
        self.shop = shop

    def setVerb(self, verb):
        self.verb = verb

    def setdish(self, dish):
        self.dish = dish

    def setadj(self,adj):
        self.adj = adj

    def setnoun(self,noun):
        self.noun = noun

    def setneg(self,neg):
        self.neg = neg

    def parser(self,shop,l,adj_list, negtive_list, dish_list):


        self.dp = l.pop().word

        idx = len(l)
        lword = [w.word for w in l]
        # n , adj , dp
        for w in list(reversed(l)):

            if w.word in adj_list:
                self.setadj(w.word)
                # self.adj = w.word
                idx = l.index(w)
                continue
            elif w.word in negtive_list:
                self.setneg(w.word)
                # self.neg = w.word
                idx = l.index(w)
                continue
            elif w.flag in ['n','nr'] and (w.word not in dish_list):
                # self.noun = w.flag
                self.setnoun(w.word)
                idx = l.index(w)
                continue

            elif w.flag == 'v' and w.word not in [u'是']:
                # print w.word
                try:
                    if l[l.index(w)+1].word in [u'的',u'得',u'地']:
                        self.setVerb(w.word)
                        idx = l.index(w)
                        break
                except IndexError,ex:
                    break

            elif w.word == u'比':
                # idx = lword.index(w.word)
                idx = l.index(w)
                break
            elif w.word in dish_list + [u',',u'.',u'，',u'。',u':',u'!',u'@',u'+',u'.',u'~',u'?',u'！',u'？',u'：',u' ',u'其他',u'另外']:
                break
            else:
                continue

        # print idx
        # print '/'.join([ w for w in lword[idx:]]) + '/' + self.dp
        self.detail = ''.join([w for w in lword[idx:]]) + self.dp
        # if len(self.detail) > 7:
        #     self.detail = self.neg + self.dp
        # if self.verb == '':
        #     self.detail = self.detail.replace(u'的',u' ').strip()
        # print self.detail+'----'+'/'.join([self.shop,self.dish, self.noun, self.neg, self.adj, self.dp])

    def groupshow(self):
        print 'parser:' + '/'.join([self.shop,self.dish, self.verb ,self.noun, self.neg, self.adj, self.dp])

