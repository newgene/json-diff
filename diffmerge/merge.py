#! /usr/bin/env python
#coding:utf-8

from method import diffmethod

from dboption.mongodb import *

import time
import json_tools
import jsonpatch

import json_delta

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#lastdb,diffdb参数
#一种情况是导入数据库merge
#另外一种情况是直接连接数据库导入到新的数据
#注意，有一个新的genediff_jobs表，根据这个表从genenchanges表中导入新的内容。

def merge(lastdb, newdb, diffdb):
    """
    lastdb: the old gene database
    newdb: the new gene database
    diffdb: the database that is the update/newly add/remove parts new gene database relativality old database
    """
    #merge = diffdb.find()
    merge_id = [ ele["_id"] for ele in diffdb.find({},{'_id':1}) ]
    not_merged = []
    for i in merge_id:
        gene = diffdb.find_one({"_id":i})
        if gene["stat"] == "add":
            lastdb.insert(gene["value"])
        if gene["stat"] == "remove":
            lastdb.remove({"_id":gene["gene_id"]})
        if gene["stat"] == "replace":
            last_gene = lastdb.find_one({"_id":gene["gene_id"]})
            patch_lst = gene["value"]
            if patch_lst:
                try:
                    new_gene = jsonpatch.apply_patch(last_gene, patch_lst, in_place=True)
                    lastdb.update({"_id":gene["gene_id"]}, new_gene)
                except:
                    not_merged.append(gene["gene_id"])
    print not_merged

def main():
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am merge the new genes to old gene database."
    
    lastdb = db.genedoc_mygene_20141019_efqag2hg
    newdb = db.genedoc_mygene_20141026_g6svo5ct
    diffdb = db.genechanges      #genechange是存储变更的数据的collection

    merge(lastdb, newdb, diffdb)
    
    print "ok. I have finished my work."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
