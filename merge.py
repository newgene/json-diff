#! /usr/bin/env python
#coding:utf-8

from method import diffmethod

from dboption.mongodb import *

import time
import json_tools

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def merge():
    merge = db_change.find()
    for gene in merge:
        if gene["stat"] == "add":
            lastdb.insert(gene["value"])
        elif gene["stat"] == "remove":
            lastdb.remove({"_id":gene["gene_id"]})
        elif gene["stat"] == "replace":
            last_gene = lastdb.find_one({"_id":gene["gene_id"]})
            new_gene = json_tools.patch(last_gene, gene["value"])
            lastdb.update({"_id":gene["gene_id"]}, new_gene)
        else:
            print "There is not new gene."

def main():
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am merge the new genes to old gene database."
    merge()
    print "ok."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
