#! /usr/bin/env python
#coding:utf-8

import datetime
import json



class OptLst():
    def __init__(self, lst1, lst2):
        self.lst1 = lst1
        self.lst2 = lst2
            
    def addLst(self):  
        add = set(self.lst2).difference(set(self.lst1))
        return list(add)
        
    def shareLst(self):
        share = set(self.lst2).intersection(set(self.lst1))
        return list(share)
        
    def deleLst(self):           
        dele = set(self.lst1).difference(self.shareLst())
        return list(dele)

