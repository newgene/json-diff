#! /usr/bin/env python
#coding:utf-8


from method import diffmethod

from dboption.mongodb import *

import json
import datetime
import time
import json_tools

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



def main():
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am working like a horse. You may have a rest and I will send you the result after a while."
    diff()
    print "ok."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
