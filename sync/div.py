# -*- coding: utf-8 -*-
#!/bin/env python

outfile = file("mobile_base_part.txt","w")
count = 0
shopbefore = 0
tag = False
for line in file("/Users/mantou/mobile_base.txt"):
    count += 1
    shopid = line.split('\t')[0]
    if count > 1210000:
        if shopid != shopbefore:
            tag = True
        if tag:
            outfile.writelines(line)
    shopbefore = shopid

outfile.close()
