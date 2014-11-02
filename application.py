#! /usr/bin/env python
#coding:utf-8


from method import diffmethod
from method import fileio

import json
import datetime

#避免出现乱码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#如果内存足够，可直接生成id的列表

def geneIdLst(genedb): 
    return [ ele['_id'] for ele in genedb ]


test11 = {"_id":1,"a":"aaa","b":"bbb","c":"ccc","d":"ddd"}
test12 = {"_id":1,"a":"aaa","b":"bbb","c":"ccc","d":"ddd1212121212"}

test21 = {"_id":2,"a":"aaa","b":"bbb","c":"ccc","d":"ddd"}
test22 = {"_id":2,"a":"aaa","b":"bbb","c":"ccc"}

test32 = {"_id":3,"c":"ccc"}
test42 = {"_id":4,"c":"ccc"}

last_genedb = [test11,test21]
new_genedb = [test12,test22,test32, test42]

def main():
    last_id = geneIdLst(last_genedb)    #新旧数据的id
    new_id = geneIdLst(new_genedb)
    print "last_id:",last_id
    print "new_id:",new_id

    #比较两数据库的文档id，如果新数据库中文档id是新增加的，则该文档为新增
    geneid = diffmethod.GeneId(last_id, new_id)
    add_gene = geneid.addGeneId()               #新增id列表
    shared_gene = geneid.sharedGeneId()         #公有id列表
    print "add_gene:",add_gene
    print "shared gene:",shared_gene
    
    #将add_gene中的dictionary保存到add文件中
    if add_gene:
        file_dir_name = './resultfile/'+str(datetime.date.today())+"-add.txt"
        fi = open(file_dir_name,"wa")
        for i in add_gene:
            for ele in new_genedb:
                if ele['_id'] == i:
                    content = json.dumps(ele)
                    print content
                    fi.write(content)
                   
        fi.close()

            
        
if __name__=="__main__":
    #geneidfile = GeneIdFile("./tempfile/")
    #geneidfile.input_geneid_file(new_genedb,"new")
    
    #print geneidfile.input_geneid_file(new_genedb,"new")
    main()
