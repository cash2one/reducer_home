# -*- coding: utf-8 -*-
#!/bin/env python

outfile = file("mobile_update_part.txt","w")
count = 0
shopbefore = 0
tag = False
for line in file("test.txt"):
    count += 1
    shopid = line.split('\t')[0]
    if count > 20:
        if shopid != shopbefore:
            tag = True
        if tag:
            outfile.writelines(line)
    shopbefore = shopid

outfile.close()
