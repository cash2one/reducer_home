#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'mantou'

dict = {}
i = 0

for line in file(sys.argv[1]):
    word = line.split('\t')[1]
    if word not in dict.keys():
        dict[word] = i
        i+=1
print len(dict.keys())