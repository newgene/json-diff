#!/usr/bin/env python
# coding=utf-8

import os
from os.path import isdir, join

import sqlite3 as lite
import sys

import csv

from setting import *

class StoreSqlite(object):
    """
    Read the data from the files with '.sqlite' as their extension.
    store the columns of probe_id, gene_id of the probes table into the file with '.csv' as its extension.
    """
    def __init__(self, ex_dir=EXTRACTED_DIR, csv_dir=CSVFILES_DIR, log=LOG): 
        self.ex_dir = ex_dir
        self.csv_dir = csv_dir
        self.log = log

    def listSqliteName(self):
        """
        get the name of '.csv' file.
        """
        #lstdir = self.unzipFile()
        lstdir = os.listdir(self.ex_dir)
        sqlites_dir = [ d for d in lstdir if isdir(join(self.db_dir,d)) ]
        all_sql_dir = [self.db_dir + d + "/inst/extdata" for d in sqlites_dir]
        sqlites_name = [listdir(dir) for dir in all_sql_dir]
        n = len(all_sql_dir) if len(all_sql_dir)==len(sqlites_name) else len(all_sql_dir)
        dir_file = [all_sql_dir[i]+'/'+sqlites_name[i][0] for i in range(n)]

        return dir_file


    def storeSqlite(self):
        """
        write the data into '.csv' file.
        """
        #sqlites_lst = self.listSqliteName()
        dbdir_lst = os.listdir(self.ex_dir)
        sqlite_dirs = [self.ex_dir+'/'+dbdir+'/inst/extdata' for dbdir in dbdir_lst]
        sqlite_lstfiles = [os.listdir(one_dir) for one_dir in sqlite_dirs]
        for one_lst in sqlite_lstfiles:
            if len(one_lst)>1:
                sqlite_lstfiles.remove(one_lst)
                for i in one_lst:
                    if "sqlite" in i:
                        dirname = i.split(".")[0]
                        sqlite_dirs.remove(self.ex_dir+'/'+dirname+'.db/inst/extdata')
        
        sqlite_files = [ element[0] for element in sqlite_lstfiles ]
        
        sqlite_path = map(lambda x,y: x+'/'+y, sqlite_dirs,sqlite_files)
        
        log_lst = []

        print "writing data into csv file..."

        noprobes = []
        for sqlite in sqlite_path:
            
            con = lite.connect(sqlite)
            cur = con.cursor()
            try:
                cur.execute("select probe_id,gene_id from probes")
            except:
                noprobes.append(sqlite)
        return noprobes
"""
            try:
                con = lite.connect(sqlite)
                cur = con.cursor()
                cur.execute("select probe_id,gene_id from probes")

                sqlite_name = sqlite.split("/")[-1]
                newdb_file = sqlite_name.split(".")[0] + ".csv"
                dir_newdb_file = self.csv_dir + newdb_file

                db_log = {}
                row_number = 0
                with open(dir_newdb_file, 'wb') as csv_file:
                    writer = csv.writer(csv_file, delimiter='\t')
                    writer.writerow(("probe_id","gene_id"))
                    rows = cur.fetchall()
                    for row in rows:
                        if bool(row[1]) is True:
                            writer.writerow(row)
                            row_number += 1

                db_log['package'] = newdb_file
                db_log['rows'] = row_number
                log_lst.append(db_log)

            except lite.Error, e:
                print sqlite
                print "Error %s:" % e.args[0]
                sys.exit(1)

        return log_lst
"""
#    def writeLogs(self, logfile):
#        """
#        write logs into the file.
#        """

 #       packages = self.usefulTable()
 #       rows_number = self.storeSqlite()

 #       with open(logfile, "wb") as csv_f:
 #           writer = csv.writer(csv_f, delimiter='\t')
 #           writer.writerow(("package","rows","title"))
 #           for line in packages:
 #               for element in rows_number:
 #                   if element['package'].split('.')[0] == line['package'].split('.')[0]:
 #                       writer.writerow((line['package'],element['rows'],line['title']))

 #       print "The work had been finished."
