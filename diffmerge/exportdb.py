#! /usr/bin/env python
#coding:utf-8

from dboption.mongodb import *

import datetime
import os
import os.path

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def exportdb(dbname, collection, filename):
    """
    dbname: 数据库名称
    collection: 所要导出的collection名称
    filename: 导出的collection存储的文件名
    导出之后的结果文件，存在当前目录中
    """

    exportdb = "mongoexport -d " + dbname + " -c " + collection + " -o " + filename
    os.system(exportdb)
    
    filename_bef = filename.split(".")[0]

    targzip = "tar -zcvf " + filename_bef + ".tar.gz " + filename
    os.system(targzip)

    print "ok."


if __name__=="__main__":
    dbname = 'genetest'
    collection = 'genechange'
    filename = 'genechange.json'
    exportdb(dbname, collection, filename)
