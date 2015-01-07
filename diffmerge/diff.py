#! /usr/bin/env python 
#coding:utf-8

from method import diffmethod

from dboption.mongodb import *

import time
import datetime
import jsonpatch

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.setrecursionlimit(3500)

def diff(lastdb, newdb, ttime, ignore=None):
    
    """
    find the difference between the two JSONs.
    lastdb: old collection
    newdb: new collection
    ignore: the neglected first level key of json in comparison, default is None, or like igore=['timetamp',]
    """
    if isinstance(ttime,str):
        timestamp = ttime.split(".")[0]
    else:
        timestamp = str(ttime).split(".")[0]

    
    gene_last = [ ele["_id"] for ele in lastdb.find({},{'_id':1}) ]
    gene_new = [ ele["_id"] for ele in newdb.find({},{'_id':1}) ]
    
    gene_last_count = len(list(gene_last))
    gene_new_count = len(list(gene_new))

    #将操作信息记录日志中
    oldname = diffmethod.collection_name(lastdb)
    newname = diffmethod.collection_name(newdb)
    gene_last_name = oldname["collection"]
    gene_new_name = newname["collection"]
    if ignore:
        db_logs.insert({"olddb":{"name":gene_last_name, "count":gene_last_count}, 
                        "newdb":{"name":gene_new_name, "count":gene_new_count},
                        "timestamp":timestamp,
                        "extra_parameters":ignore
                        })
    else:
        db_logs.insert({"olddb":{"name":gene_last_name, "count":gene_last_count}, 
                        "newdb":{"name":gene_new_name, "count":gene_new_count},
                        "timestamp":timestamp,
                        })


    geneid = diffmethod.OptLst(gene_last, gene_new)
    
    add_gene = geneid.addLst()              #the list consisting of the IDs in the new collection different from the IDs in the old one
    shared_gene = geneid.shareLst()         #the list consisting of the IDs in the new collection same as the IDs in the old one
    deleted_gene = geneid.deleLst()         #the list consisting of the IDs in the old collection but not in the new collection

    #insert the new values into the database.
    if add_gene:
        have_a_rest = 0
        add_count = len(add_gene)
        for i in add_gene:
            one_gene = newdb.find_one( {"_id":i} )
            db_change.insert( {"gene_id":i, "stat":"add", "value":one_gene, "timestamp":timestamp} )
            have_a_rest +=1
            if have_a_rest == 200:
                time.sleep(1)
                have_a_rest = 0
    else:
        add_count = 0

    #store the deleted IDs        
    if deleted_gene:
        have_a_rest = 0
        remove_count = len(deleted_gene)
        for i in deleted_gene:
            one_gene = lastdb.find_one( {"_id":i} )
            db_change.insert( {"gene_id":i, "stat":"remove", "timestamp":timestamp} )
            have_a_rest +=1
            if have_a_rest == 200:
                time.sleep(1)
                have_a_rest = 0
    else:
        remove_count = 0

    #store the records in which the values have been changed
    if shared_gene:
        have_a_rest = 0
        replace_count = 0
        if ignore:      #判断是否有忽略判断，如果有则生成一个忽略的dictionary
            ign_dict = dict( (el, 0) for el in ignore )
        else:
            ign_dict = {}
        
        for i in shared_gene:
            if ign_dict:
                last_content = lastdb.find_one( {"_id":i}, ign_dict )
                new_content = newdb.find_one( {"_id":i}, ign_dict )
            else:
                last_content = lastdb.find_one( {"_id":i} )
                new_content = newdb.find_one( {"_id":i} )
            
            if cmp(last_content, new_content) !=0:
                patch = jsonpatch.JsonPatch.from_diff(last_content, new_content)
                diff_lst = list(patch)
                db_change.insert( {"gene_id":i, "stat":"replace", "value":diff_lst, "timestamp":timestamp} )
                replace_count +=1
                have_a_rest +=1
                if have_a_rest == 200:
                    time.sleep(1)
                    have_a_rest = 0

    else:
        replace_count = 0
    
    #保存日志信息
    total = replace_count + remove_count + add_count
    stat = {"remove":remove_count, "add":add_count, "replace":replace_count, "total":total}
    db_logs.update({"timestamp":timestamp},{"$set":{"stat":stat}})


def main():
    
    print ">>>Hi, I am Qiwei. Welcome to my website: www.itdiffer.com<<<"
    print "I am working like a horse. You may have a rest and I will send you the result after a while."

    lastdb = db.genedoc_mygene_20141019_efqag2hg
    newdb = db.genedoc_mygene_20141026_g6svo5ct
    #lastdb = db.part_old
    #newdb = db.part_new
    atime = str(datetime.datetime.today())    
    
    diff(lastdb, newdb, atime)

    print "ok."


if __name__=="__main__":
    start = time.clock()
    
    main()

    print "The time I have spent is:"
    print (time.clock() - start)
