#! /usr/bin/env python
#coding:utf-8

from dboption.mongodb import *

from method import diffmethod

import datetime
import os
import os.path

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def exportdb(collection, filename, condition=None):
    """
    collection: 所要导出的collection, 格式 collection=db.genechanges, db在./dboption/mongodb.py中设置
    condition: 设置导出条件，比如导出{"timestamp":"2014-11-2 10:10:10"}，此条件必是类似格式
               如果不赋值，意味着将整个collection导出
    filename: 导出的collection存储的文件名（含扩展名）
              导出之后的结果文件，存在当前目录中
    """
    db_collection = diffmethod.collection_name(collection)
    dbname = db_collection["dbname"]
    collection_name = db_collection["collection"]
    
    db.temp.remove()
    if condition:
        temp_doc = collection.find(condition)
        db.temp.insert(temp_doc)
    if db.temp.count():
        collection_name = "temp"
    
    exportdb = "mongoexport -d " + dbname + " -c " + collection_name + " -o " + filename
    print exportdb
    os.system(exportdb)
    
    filename_bef = filename.split(".")[0]

    targzip = "tar -zcvf " + filename_bef + ".tar.gz " + filename
    os.system(targzip)

    print "ok."


if __name__=="__main__":
    collection = db.genechanges
    filename = 'genechange.json'
    #exportdb( collection, filename, {"timestamp" : "2014-12-04 21:33:44.577447"} )
    exportdb( collection, filename )
