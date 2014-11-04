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

#option about db id

class GeneId():
    def __init__(self, last_lst, new_lst):
        self.last_lst = last_lst
        self.new_lst = new_lst

    def addGeneId(self):       #compare the two lists of gene id, return the id list that had been added
        add_gene_id = set(self.new_lst) - set(self.last_lst)
        return list(add_gene_id)

    def sharedGeneId(self):     #return the shared id in two lists of gene id
        shared_gene_id = set(self.new_lst) & set(self.last_lst)
        return list(shared_gene_id)

class OptLst()
    def __init__(self, lst1, lst2):
        self.lst1 = lst1
        self.lst2 = lst2
            
    def addLst(self):  
        add = set(self.lst2) - set(self.lst1)
        return add
        
    def shareLst(self):
        share = set(self.lst2) & set(self.lst1)
        return share

#compare the dictionary

class CompareDicts():
    def __init__(self, last_dict, new_dict):
        self.last_dict = last_dict
        self.last_key = [ k for k in last_dict ]
        
        self.new_dict = new_dict
        self.new_key = [ k for k in new_dict ]

    def addKey(self):    #return the key of new dictionary that had been added 
        add_key = [ ele for ele in self.new_dict if ele not in self.last_dict ]
        return add_key

    def delKey(self):    #return the key of new dictionary that had been deleted
        del_key = [ ele for ele in self.last_dict if els not in self.new_dict ]
        return del_key

    def updateKey(self):    #return the keys list of update that is in new dictionary
        add_key = self.addKey()
        shared_key = set(self.new_dict.keys()) - set(add_key)
        update_key = [ k for k in shared_key if self.new_dict[k] != self.last_dict[k] ]
        return list(update_key)
       
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
