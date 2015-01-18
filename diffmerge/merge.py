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

def merge(lastdb, newdb, diffdb, rest=200):
    """
    lastdb: the old gene database
    newdb: the new gene database
    diffdb: the database that is the update/newly add/remove parts new gene database relativality old database
    """
    #merge = diffdb.find()
    #merge_id = [ ele["gene_id"] for ele in diffdb.find() ]
    stat_add_id = [ele["gene_id"] for ele in diffdb.find({"stat":"add"})]
    stat_remove_id = [ele["gene_id"] for ele in diffdb.find({"stat":"remove"})]
    stat_replace_id = [ele["gene_id"] for ele in diffdb.find({"stat":"replace"})]
    
    merge_num = 0

    if stat_add_id:
        have_a_rest = 0
        for i in stat_add_id:
            gene = diffdb.find_one({"gene_id":i})
            lastdb.insert(gene['value'])
            merge_num += 1
            have_a_rest += 1
            if have_a_rest == rest:
                time.sleep(1)
                have_a_rest = 0

    if stat_remove_id:
        have_a_rest = 0
        for i in stat_remove_id:
            lastdb.remove({"_id":i})
            merge_num += 1
            have_a_rest += 1
            if have_a_rest == rest:
                time.sleep(1)
                have_a_rest = 0

    not_merged = []
    if stat_replace_id:
        have_a_rest = 0
        for i in stat_replace_id:
            last_gene = lastdb.find_one({"_id":i})
            patch_lst = gene["value"]
            if patch_lst:
                try:
                    new_gene = jsonpatch.apply_patch(last_gene, patch_lst, in_place=True)
                    lastdb.update({"_id":i}, new_gene)
                    merge_num += 1
                    have_a_rest += 1
                    if have_a_rest == rest:
                        time.sleep(1)
                        have_a_rest = 0
                except:
                    not_merged.append(i)

    if not_merged:
        have_a_rest = 0
        for i in not_merged:
            new_gene = newdb.find_one({"_id":i})
            lastdb.update({"_id":i}, new_gene)
            merge_num += 1
            have_a_rest += 1
            if have_a_rest == rest:
                time.sleep(1)
                have_a_rest = 0
    
    print merge_num

def main():
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am merge the new genes to old gene database."
    
    lastdb = db.genedoc_mygene_20141019_efqag2hg
    newdb = db.genedoc_mygene_20141026_g6svo5ct
    #lastdb = db.part_old
    #newdb = db.part_new
    diffdb = db.genechanges      #genechange是存储变更的数据的collection

    merge(lastdb, newdb, diffdb, 200)
    
    print "ok. I have finished my work."


if __name__=="__main__":
    start = time.clock()
    main()
    print "The time I have spent is:"
    print (time.clock() - start)
