#! /usr/bin/env python
#coding:utf-8

from dboption.mongodb import *

import datetime
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def exportdb(dbname, collection, tofile):
    exportdb = "mongoexport -d " + dbname + " -c " + collection + " -o " +tofile
    os.system(exportdb)
    print "ok."


if __name__=="__main__":
    dbname = 'genetest'
    collection = 'newdb'
    tofile = './file/new.json'
    exportdb(dbname, collection, tofile)
