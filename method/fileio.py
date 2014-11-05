#!/usr/bin/env python
#coding:utf-8

import datetime
import json

from dboption.mongodb import *

class InOutFile():
    def __init__(self, filedir):
        self.filedir = filedir

    def output_file(self, content, version):     #version:'add','change' or 'new','last'
        filename = str(datetime.date.today()) + "-" + version
        file_dir_name = self.filedir + filename + ".txt"
        try:
            nf = open(file_dir_name,"wa")
            nf.write(json.dumps(content))
        finally:
            nf.close()

    def input_file(self,file_dir_name):
        try:
            f = open(file_dir_name)
            content = json.loads(f.read())
        finally:
            f.close()
        return content

class SaveDb():
    def __init__(self, docname):
        self.docname = docname

    def insertDb(self, content, key):
        if content:
            self.docname.insert({key:content})
