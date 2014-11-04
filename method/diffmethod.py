#! /usr/bin/env python
#coding:utf-8

import datetime
import json

class GeneIdLst():
    def __init__(self,gene_dict):
        self.gene_dict = gene_dict

    def geneid_lst(self):
        id_num_lst = []
        id_num_lst.append(self.gene_dict['_id'])
        return id_num_lst



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
        
    def deleLst(self):           #some elements is in lst1,but is not in lst2. Be deleted form lst2
        dele = set(self.lst1).difference(self.shareLst())
        return list(dele)

#compare the dictionary

class CompareDicts(OptLst):
    def __init__(self, last_dict, new_dict):
        self.last_dict = last_dict
        self.last_key = [ k for k in last_dict ]
        
        self.new_dict = new_dict
        self.new_key = [ k for k in new_dict ]

        OptLst.__init__(self,self.last_key,self.new_key)
    
    def takeKV(self,key,where=2):     #where=2--object is self.new_dict; where=1--object is self.last_dict
        take_dict = {}
        if where==2:
            take_dict[key] = self.new_dict[key]
        else:
            take_dict[key] = self.last_dict[key]

        return take_dict

    def updateDict(self,k):
        if self.new_dict[k] != self.last_dict[k]:
            return self.new_dict
        else:
            return [] 
       
class ResultDict():
    def __init__(self, key_list, one_dict):
        self.key_list = key_list
        self.one_dict = one_dict

    def valuesList(self):
        element_dict = {}
        values_lst = []
        for k in self.key_list:
            element_dict[k] = self.one_dict[k]
        values_lst.append(element_dict)
        return values_lst

    def resultDict(self, status):
        result_dict = {}
        result_dict[status] = self.valueList()
        return result_dict
