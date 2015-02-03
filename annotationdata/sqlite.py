#!/usr/bin/env python
# coding=utf-8

import os

import sqlite3 as lite

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

    def storeSqlite(self):
        """
        write the data into '.csv' file.
        """
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
        
        makeDir(self.csv_dir)

        noprobes = []
        for sqlite in sqlite_path:
            
            con = lite.connect(sqlite)
            cur = con.cursor()
            try:
                cur.execute("select probe_id,gene_id from probes")
                
                sqlite_name = sqlite.split("/")[-1]
                newdb_file = sqlite_name.split(".")[0] + ".csv"
                dir_newdb_file = self.csv_dir + '/' + newdb_file
                
                db_log = {}     # store every sqlite information: name, how many rows.
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

            except:
                noprobes.append(sqlite.split('/')[-1].split('.')[0])
        
        # write log file
        with open("tmplog.csv", 'rb') as input, open(self.log, 'wb') as output:
            reader = csv.reader(input, delimiter='\t')
            writer = csv.writer(output, delimiter='\t')
            writer.writerow(('package','rows','title'))
            for tmp_row in reader:
                package_name = tmp_row[0].split('.')[0]
                if package_name in noprobes:
                    writer.writerow(('*'+package_name+'*', "NOT DO IT.", tmp_row[1]))
                else:
                    for row_dict in log_lst:
                        if tmp_row[0].split('.')[0] == row_dict['package'].split('.')[0]:
                            writer.writerow((row_dict['package'],row_dict['rows'],tmp_row[1]))
        os.remove("tmplog.csv")

        print "the data(csv files) have been stored in ", self.csv_dir
        print "the log file is log.csv, it is in the same directory as this program." 

