#! /usr/bin/env python
#coding:utf-8


from method import diffmethod

from dboption.mongodb import *

import json
import datetime
from bintrees import BinaryTree

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
            db_add.insert({"gene_id":i,"content":one_gene})
 
    #将新集合中已经删除的基因插入数据库        
    if deleted_gene:
        for i in deleted_gene:
            one_gene = lastdb.find_one({"_id":i})
            db_del.insert({"gene_id":i,"content":one_gene})

    #将新集合中原有的基因中，做了部分修改的基因插入数据库
    if shared_gene:
        for i in shared_gene:
            last_content = lastdb.find_one({"_id":i},{"_id":0})
            new_content = newdb.find_one({"_id":i},{"_id":0})
            
            last_tree, new_tree = BinaryTree(), BinaryTree()
            last_tree.update(last_content)
            new_tree.update(new_content)
            
            add_content = new_tree.__sub__(last_tree)
            del_content = last_tree.__sub__(new_tree)
            and_content = new_tree.__and__(last_tree)
            
            if add_content:
                db_upd.insert({"gene_id":i,"status":"add","content":dict(add_content)})
            if del_content:
                db_upd.insert({"gene_id":i,"status":"delete","content":dict(del_content)})
            if and_content:
                for k in and_content:
                    if and_content[k] != last_tree[k]:
                        db_upd.insert({"gene_id":i,"status":"update","content":{k:and_content[k]}})

def main():
    print "I am working. You can have a rest, drink tea or others. You will come back some minutes later."
    diff()
    print "ok. I finished my working. I will have a rest."


if __name__=="__main__":
    main()
