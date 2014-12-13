#!/usr/bin/env python
#coding:utf-8

import tornado.web

from db.db import *

import json
import datetime
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QueryGene(tornado.web.RequestHandler):
    def post(self):
        content = self.get_argument("data")
        content = tornado.escape.json_decode(content)
    
        query_con = {}

        if "posstart" in content and "posend" in content:
            pos_con = {"$gte":int(content['posstart']), "$lte":int(content['posend'])}
            query_con["pos"] = pos_con
            del content["posstart"]
            del content["posend"]
        elif "posstart" in content:
            query_con['pos'] = int(content['posstart'])
            del content["posstart"]
        elif "posend" in content:
            query_con['pos'] = int(content['posend'])
            del content["posend"]
        else:
            pass

        for k,v in content.items():
            if k=="ref":
                v = v.upper()
            query_con[str(k)] = str(v)

        if query_con:
            que = db.find(query_con,{"_id":0})
            if que.count():
                lst = [ every for every in que]
                data_json = json.dumps(lst, sort_keys=True, indent=2)
                file_name = str(datetime.datetime.now())
                file_name = "-".join(file_name.split(' '))
                json_file = json_dir + file_name + ".json"
                
                os.system("rm -f "+json_dir+"*.json")
                with open(json_file, "w") as fj:
                    fj.write(data_json)
                self.write(file_name)
            
            else:
                self.write("0")
        else:
            self.write("0")

