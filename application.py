#! /usr/bin/env python
#coding:utf-8


from method import diffmethod
from method import fileio

from dboption.mongodb import *

import json
import datetime

#避免出现乱码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

filedir = "./tempfile/"
result_filedir = "./resultfile/"

def main():

    gene_lst_19 = [ ele["_id"] for ele in db_g19.find({},{'_id':1}) ]
    gene_lst_26 = [ ele["_id"] for ele in db_g26.find({},{'_id':1}) ]
    print "2014-10-19,gene database ==>",len(gene_lst_19)
    print "2014-10-26,gene database ==>",len(gene_lst_26)


    #gene_id_file = fileio.InOutFile(filedir)
    #gene_id_file.output_file(gene_lst_19,"last")  #测试使用   
    #gene_id_file.output_file(gene_lst_26,"new")


    #比较两数据库的文档id，如果新数据库中文档id是新增加的，则该文档为新增
    
    geneid = diffmethod.OptLst(gene_lst_19, gene_lst_26)
    add_gene = geneid.addLst()              #在新集合中新增加的基因id
    print "10-26 database add new gene ==>",len(add_gene)
    
    shared_gene = geneid.shareLst()         #在新集合中原有的基因id
    print "10-26 database & 10-19 database ==>",len(shared_gene)
    
    deleted_gene = geneid.deleLst()         #在旧集合中有，但是在新集合中已经删除的基因id
    print "10-26 database had been deleted gene ==>",len(deleted_gene)

    #gene_id_file.output_file(add_gene,"add")        #测试使用
    #gene_id_file.output_file(shared_gene,"shared")
    
    gene_id_result = fileio.InOutFile(result_filedir)
    
    #将新集合中新增加的基因输出到文件中
    if add_gene:
        gene_add_lst = [ db_g26.find_one({"_id":i}) for i in add_gene]
        gene_id_result.output_file(gene_add_lst,"add")   #输出数据格式：'[{完整基因信息}],'
    
    #将新集合中已经删除的基因输出到文件中        
    if deleted_gene:
        gene_deleted_lst = [ db_g19.find_one({"_id":i}) for i in deleted_gene ]
        gene_id_result.output_file(gene_deleted_lst,"deleted")
    
    #将新集合中原有的基因中，做了部分修改的基因输出到文件中
    if shared_gene:
        gene_update_lst = []
        for i in shared_gene:
            change_gene ={}
            change_gene["_id"] = i
            
            gene_content = diffmethod.CompareDicts(db_g19.find_one({"_id":i}), db_g26.find_one({"_id":i}))
            gene_content_add = gene_content.addLst()
            gene_content_del = gene_content.deleLst()
            gene_content_share = gene_content.shareLst()
            
            if gene_content_add:
                content = [ gene_content.takeKV(k) for k in gene_content_add ]
                change_gene["add"] = content
            else:
                change_gene["add"] = ["Do not ADD new gene."]
            
            if gene_content_del:
                content = [ gene_content.takeKV(k,where=1) for k in gene_content_del ]
                change_gene["delete"] = content
            else:
                change_gene["delete"] = ["Do not DELETE gene."]
            
            if gene_content_share:
                content = []
                for k in gene_content_share:
                    update_dict = gene_content.updateDict(k)
                    if update_dict:
                        content.append(update_dict)
                if content:
                    change_gene["update"] = content
                else:
                    change_gene["update"] = ["Do not UPDATE gene value."]
            else:
                change_gene["update"] = ["Do not UPDATE gene."]

            gene_update_lst.append(change_gene)
            
            gene_id_result.output_file(gene_update_lst,"update")



if __name__=="__main__":
    main()
