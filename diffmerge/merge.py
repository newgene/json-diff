#! /usr/bin/env python
#coding:utf-8

from method import diffmethod

from dboption.mongodb import *

import time
import json_tools

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#lastdb,diffdb参数
#一种情况是导入数据库merge
#另外一种情况是直接连接数据库导入到新的数据
#注意，有一个新的genediff_jobs表，根据这个表从genenchanges表中导入新的内容。

def merge(lastdb, diffdb):
    """
    lastdb: the old gene database
    diffdb: the database that is the update/newly add/remove parts new gene database relativality old database
    """
    merge = diffdb.find()
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
    
    lastdb = db.genedoc_mygene_20141019_efqag2hg
    diffdb = db.genechange      #genechange是存储变更的数据的collection

    merge(lastdb, diffdb)
    
    print "ok. I have finished my work."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
