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
        search_con = self.get_arguments("q")[0]
        file_name = self.get_argument("j")
        current_page = int(self.get_argument("p"))
        
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
            if k=="ref":
                v = v.upper()
            query_con[k] = v

        
        if query_con:
            page_size = 10
            begin_index = (current_page - 1) * page_size
            que = db.find(query_con).skip(begin_index).limit(page_size)
            counts = que.count()
            pages = counts / page_size if counts % page_size == 0 else counts / page_size + 1
            json_file = u"/static/jsonfile/"+file_name+u".json"
            self.render("query.html", result=que, json=json_file, currentpage=current_page, pages=int(pages))
        else:
            self.render("query.html", result=False)

