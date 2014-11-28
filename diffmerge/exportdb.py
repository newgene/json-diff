#! /usr/bin/env python
#coding:utf-8

from dboption.mongodb import *

import datetime
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def exportdb(dbname, collection, filename):
    exportdb = "mongoexport -d " + dbname + " -c " + collection + " -o ./file/" +filename + ".json"
    os.system(exportdb)
    targzip = "tar -zcvf ./file/" + filename + ".tar.gz ./file/"+filename + ".json"
    os.system(targzip)
    print "ok."


if __name__=="__main__":
    dbname = 'genetest'
    collection = 'newdb'
    filename = 'new'
    exportdb(dbname, collection, filename)
