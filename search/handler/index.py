#!/usr/bin/env python
#coding:utf-8

import tornado.web

from db.db import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        lst = "welcome you." 
        self.render("index.html", info=lst)

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        search_con = self.get_arguments("con")[0]
        content = tornado.escape.json_decode(search_con)

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
            if k=="vartype":
                v = v.lower()
            if k=="ref":
                v = v.upper()
            if k!="style":
                query_con[k] = v

        
        if query_con:
            que = db.find(query_con)
            if que.count():
                if content["style"]=="table":
                    self.render("query.html", result=que)
                elif content["style"]=="json":
                    self.render("search.html", result=que)
                else:
                    self.render("query.html", result=False)
            else:
                self.render("query.html", result=False)
        else:
            self.render("query.html", result=False)

