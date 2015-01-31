#!/usr/bin/env python
# coding=utf-8

from anno import *
from sqlite import *

def main():
    url = "http://bioconductor.org/packages/3.0/data/annotation/"
    db_dir = "/home/qw/Documents/Newgene/json-diff/annotationdata/db/"
    log_file = "/home/qw/Documents/Newgene/json-diff/log.csv"
    #scratch = ScratchData(3, url, db_dir)
    #scratch.writeLogs(log_file)
    #scratch.writeLogs("log.txt")
    #scratch.downloadPackage("/home/qw/Documents/Newgene/json-diff/annotationdata/db/")
    store_sql = StoreSqlite(version = 3, download_url=url,db_directory=db_dir,store_dir= db_dir)
    #sqlites_dir = store_sql.storeSqlite()
    #store_sql.writeLogs(log_file)
    store_sql.listSqliteName()
    #print sqlites_dir

if __name__ == "__main__":
    main()
