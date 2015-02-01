#!/usr/bin/env python
# coding=utf-8

from anno import *
from sqlite import *

def main():

    url = "http://bioconductor.org/packages/3.0/data/annotation"   # the webpage of Bioconductor3.0
    db_dir = "/home/qw/Documents/Newgene/json-diff/annotationdata/db/"  # the directory of packages and csv files

    log_file = "/home/qw/Documents/Newgene/json-diff/log.csv"  # log file

    """
    get the data from webpage(url) and download the *.gz files.
    the extension all the packages is '.db'.
    """
    scratch = ScratchData(url, db_dir)
    scratch.unzipFile()  # extract '.gz' files

    store_sql = StoreSqlite(download_url=url,db_directory=db_dir,store_dir= db_dir)
    store_sql.storeSqlite()     # write data into '.csv' files
    store_sql.writeLog(log_file)    # write log file

if __name__ == "__main__":
    main()
