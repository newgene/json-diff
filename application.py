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
    gene_id_file = fileio.InOutFile(filedir)
    gene_id_result = fileio.InOutFile(result_filedir)

    gene_lst_19 = [ ele["_id"] for ele in db_g19.find({},{'_id':1}) ]
    gene_lst_26 = [ ele["_id"] for ele in db_g26.find({},{'_id':1}) ]
    
    gene_id_file.output_file(gene_lst_19,"last")  #测试使用   
    gene_id_file.output_file(gene_lst_26,"new")


    #比较两数据库的文档id，如果新数据库中文档id是新增加的，则该文档为新增
    geneid = diffmethod.GeneId(gene_lst_19, gene_lst_26)
    add_gene = geneid.addGeneId()               #新增id列表
    shared_gene = geneid.sharedGeneId()         #公有id列表

    gene_id_file.output_file(add_gene,"add")        #测试使用
    gene_id_file.output_file(shared_gene,"shared")
    
    #将add_gene中的dictionary保存到add文件中
    if add_gene:
        content = {}
        for i in add_gene:
            gene_con = [ele for ele in db_g26.find({"_id":i}) ]
            content[i] = gene_con
        gene_id_result.output_file(content,"add")   #输出数据，新增加的基因
            
        
if __name__=="__main__":
    main()
