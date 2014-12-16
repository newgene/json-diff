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
        content = tornado.escape.url_unescape(content, encoding='utf-8', plus=True)
        content = content[1:-1]
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
                data_json = json.dumps(lst, indent=2)
                self.write("<pre>"+data_json+"</pre>")
            else:
                self.write("0")
        else:
            self.write("0")

