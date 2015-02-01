#!/usr/bin/env python
# coding=utf-8

from anno import *
from sqlite import *

def main():
    url = "http://bioconductor.org/packages/3.0/data/annotation/"
    db_dir = "/home/qw/Documents/Newgene/json-diff/annotationdata/db/"
    
    log_file = "/home/qw/Documents/Newgene/json-diff/log.csv"
    """
    scratch the data from webpage(url) and download the *.gz files.
    all the files is .db
    unzip all of the *.gz
    """
    scratch = ScratchData(url, db_dir)
    scratch.unzipFile()
    
    """
    store the sqlite into a csv file.
    write log file.
    """
    store_sql = StoreSqlite(download_url=url,db_directory=db_dir,store_dir= db_dir)
    store_sql.writeLog(log_file)

if __name__ == "__main__":
    main()
