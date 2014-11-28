#! /usr/bin/env python
#coding:utf-8

import datetime
import json
import json_tools

from itertools import izip

class OptLst():
    """
    Compute two lists
    """
    def __init__(self, lst1, lst2):
        self.lst1 = lst1
        self.lst2 = lst2
            
    def addLst(self):           #return to the list with elements in list2 but not in list1
        add = set(self.lst2).difference(set(self.lst1))
        return list(add)
        
    def shareLst(self):         #return to the list with elements common to list2 and list1
        share = set(self.lst2).intersection(set(self.lst1))
        return list(share)
        
    def deleLst(self):           ##return to the list with elements in list1 but not in list2, that is, the elements deleted from list2
        dele = set(self.lst1).difference(self.shareLst())
        return list(dele)


class DiffJson():
    '''
    Compare two dictionaries
    '''
    def __init__(self, old_dict, new_dict): 
        self.old = old_dict
        self.new = new_dict
    
    def diffDict(self):         #compare two dictionaries and return to the result in the form of a list
        diff = json_tools.diff(self.old, self.new)
        return diff

    '''
    #for example:
    >>> a={"a":1,"b":{"bb":22},"c":3}
    >>> b={"b":{"bb":44},"c":9,"d":00}
    >>> json_tools.diff(a,b)
    [{'prev': 1, 'remove': '/a'}, {'prev': 3, 'value': 9, 'replace': '/c'}, {'prev': 22, 'value': 44, 'replace': '/b/bb'}, {'add': '/d', 'value': 0}]

    '''

    def makeDict(self, key_lst, value):     #build the dictionary based on the elements in the list, then get the changed dictionary.
        di = value
        for ele in key_lst:
            lst = [ ele, di ]
            i = iter(lst)
            di = dict(izip(i,i))
        return di

    def formatDict(self, di_dict, stat):    #format the result
        result = {}
        result['stat'] = stat
        result['value'] = di_dict
        return result


    def changesValue(self, diff_lst):       #get the changed value--a list
        changes_value = []
        for ele in diff_lst:
            if "remove" in ele and ele['remove']:
                value = ele['prev']
                k = ele['remove'].split('/')
                k.remove('')
                key_lst = k[::-1]
                key_lst = k
                di = self.makeDict(key_lst,value)
                result = self.formatDict(di, "u_remove")
                changes_value.append(result)
            if "replace" in ele and ele['replace']:
                value2 = ele['value']
                k2 = ele['replace']
                k2 = k2.split('/')
                k2.remove('')
                key_lst2 = k2[::-1]
                di2 = self.makeDict(key_lst2,value2)
                result = self.formatDict(di2, "u_replace")
                changes_value.append(result)
            if "add" in ele and ele['add']:
                value3 = ele['value']
                k3 = ele['add']
                k3 = k3.split('/')
                k3.remove('')
                key_lst3 = k3[::-1]
                di3 = self.makeDict(key_lst3,value3)
                result = self.formatDict(di3, "u_add")
                changes_value.append(result)
        return changes_value





