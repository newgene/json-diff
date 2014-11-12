#! /usr/bin/env python
#coding:utf-8


from method import diffmethod

from dboption.mongodb import *

import json
import datetime
import time

#避免出现乱码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def diff():

    gene_last = [ ele["_id"] for ele in lastdb.find({},{'_id':1}) ]
    gene_new = [ ele["_id"] for ele in newdb.find({},{'_id':1}) ]

    #比较两数据库的文档id，如果新数据库中文档id是新增加的，则该文档为新增
    
    geneid = diffmethod.OptLst(gene_last, gene_new)
    
    add_gene = geneid.addLst()              #在新集合中新增加的基因id
    shared_gene = geneid.shareLst()         #在新集合中原有的基因id
    deleted_gene = geneid.deleLst()         #在旧集合中有，但是在新集合中已经删除的基因id

    #将新集合中新增加的基因插入数据库
    if add_gene:
        for i in add_gene:
            one_gene = newdb.find_one({"_id":i})
            db_change.insert({"gene_id":i,"changes":[{"stat":"add","content":one_gene}],"lastdb":last_date,"newdb":new_date})
 
    #将新集合中已经删除的基因插入数据库        
    if deleted_gene:
        for i in deleted_gene:
            one_gene = lastdb.find_one({"_id":i})
            db_change.insert({"gene_id":i,"changes":[{"stat":"delete"}],"lastdb":last_date,"newdb":new_date})

    #将新集合中原有的基因中，做了部分修改的基因插入数据库
    if shared_gene:
        for i in shared_gene:
            last_content = lastdb.find_one({"_id":i},{"_id":0})
            new_content = newdb.find_one({"_id":i},{"_id":0})

            add_element = dict([ (k,v) for k,v in new_content.iteritems() if not any(k in dd for dd in last_content) ])
            del_element = dict([ (k,v) for k,v in last_content.iteritems() if any(k in dd for dd in new_content) ])
            upd_element = dict([ (k,v) for k,v in new_content.iteritems() if any(k in dd for dd in last_content) and last_content.get(k)!=v ])
            changes_value = []
            if add_element:
                add_element["stat"] = "u_add"       #有更新的基因中增加了基因的key-value
                changes_value.append(add_element)
            if del_element:
                del_element['stat'] = "u_del"       #有更新的基因中删除了基因的key-value
                changes_value.append(del_element)
            if upd_element:
                upd_element['stat'] = 'u_upd'       #有更新的基因中修改了基因的key-value
                changes_value.append(upd_element)
            
            if changes_value: 
                db_change.insert({"gene_id":i, "changes":changes_value, "lastdb":last_date, "newdb":new_date })


def main():
    print "I am working. You can have a rest, drink tea or others. You will come back some minutes later."
    diff()
    print "ok. I finished my working. I will have a rest."


if __name__=="__main__":
    start = time.clock()
    main()
    print "I have spent time:"
    print (time.clock() - start)
