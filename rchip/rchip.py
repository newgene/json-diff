#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

def rchip(sqlite, txtfile):      #silte: database name, xxx.sqlite, txtfile: restore result
    try:
        con = lite.connect(sqlite)
        cur = con.cursor()
        cur.execute("select * from probes")
        #con.commit()
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    with open(txtfile, 'aw') as resultfile:
        resultfile.write("probe_id\tgene_id\n")
        rows = cur.fetchall()
        for row in rows:
            row_str = str(row[0]) + "\t" + str(row[1]) + "\n"
            resultfile.write(row_str)

if __name__ == "__main__":
    sqlite = 'hgu95av2.sqlite'
    txtfile = "hresult.txt"
    rchip(sqlite, txtfile)
