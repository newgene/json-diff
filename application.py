#! /usr/bin/env python
#coding:utf-8


from method import diffmethod

import json
import datetime

#避免出现乱码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#如果数据量很大，可以先生成id文件，避免内存吃不消
class GeneIdFile():         
    def __init__(self, filedir):
        self.filedir = filedir
    
    #生成数据库集合id组成的文件
    def input_geneid_file(self,genedb, version):
        geneid_lst = [ele['_id'] for ele in genedb ] #genedb可以是来自数据库的,即通过读取数据库中每个集合中的文档的'_id'生成相应的id列表
                                                 #并存储在文件中   
        temp_filename = str(datetime.date.today())+"-"+version
        file_dir = self.filedir + temp_filename + ".txt"
        nf = open(file_dir,"w")
        nf.write(json.dumps(geneid_lst))
        return file_dir

    #将文件内容读出来，并返回lst
    def convert_geneid_lst(filename):
        f = open(filename)
        geneid_lst = josn.loads(f.read())
        return geneid_lst


#如果内存足够，可直接生成id的列表

def geneIdLst(genedb): 
    return [ ele['_id'] for ele in genedb ]


test11 = {"_id":1,"a":"aaa","b":"bbb","c":"ccc","d":"ddd"}
test12 = {"_id":1,"a":"aaa","b":"bbb","c":"ccc","d":"ddd1212121212"}

test21 = {"_id":2,"a":"aaa","b":"bbb","c":"ccc","d":"ddd"}
test22 = {"_id":2,"a":"aaa","b":"bbb","c":"ccc"}

test32 = {"_id":3,"c":"ccc"}

last_genedb = [test11,test21]
new_genedb = [test12,test22,test32]


        
if __name__=="__main__":
    #geneidfile = GeneIdFile("./tempfile/")
    #geneidfile.input_geneid_file(new_genedb,"new")
    
    #print geneidfile.input_geneid_file(new_genedb,"new")
    last_id = geneIdLst(last_genedb)
    new_id = geneIdLst(new_genedb)
    print last_id,new_id
