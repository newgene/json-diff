#! /usr/bin/env python
#coding:utf-8

from dboption.mongodb import *

import datetime
import os
import os.path

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def exportdb(dbname, collection, dir_filename):
    """
    dbname: 数据库名称
    collection: 所要导出的collection名称
    dir_filename: 导出的collection存储的文件名，含目录，例如：./file/change.json
    """

    exportdb = "mongoexport -d " + dbname + " -c " + collection + " -o " + dir_filename
    os.system(exportdb)
    
    filename = os.path.basename(dir_filename)
    filename_bef = filename.split(".")[0]
    dirpath = os.path.dirname(filename)

    targzip = "tar -zcvf " + dirpath + "/" + filename_bef + ".tar.gz " + filename
    os.system(targzip)

    print "ok."


if __name__=="__main__":
    dbname = 'genetest'
    collection = 'newdb'
    filename = './file/new.json'
    exportdb(dbname, collection, filename)
