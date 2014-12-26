#!/usr/bin/env python
#coding:utf-8

import tornado.web
import json

from db.db import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        http_url = self.request.uri
        if http_url == '/':
            self.render("index.html",searched=0)
        else:
            self.render("index.html",searched=1)
    
    def post(self):
        content = self.get_argument("data")
        content = tornado.escape.json_decode(content)

        page_size = content["pagesize"]
        current_page = content["nowpage"]
        display_format = content["format"]
        by_sort = content["bysort"]

        query_con = query_condition(content)
        
        sort_con = tuple([by_sort,1]) 
        
        return_data = {}

        if query_con:
            begin_index = (int(current_page) - 1) * int(page_size)
            que = db.find(query_con,{"_id":0}).sort([sort_con]).skip(begin_index).limit(int(page_size))
            return_data['value'] = list(que)
            if display_format =="table":
                counts = que.count()
                pages = int(counts) / int(page_size) if int(counts) % int(page_size) == 0 else int(counts) / int(page_size) + 1
                return_data['counts'] = int(counts)
                return_data['pages'] = int(pages)
                return_data['currentpage'] = int(current_page)
                data_json = json.dumps(return_data)
                self.write(data_json)
            elif display_format == "json":
                #lst = [ every for every in que]
                #print lst
                data_json = json.dumps(return_data['value'], indent=2)
                self.write(data_json)
                #data_json = json.dumps(list(que), indent=2)
                #print data_json
                #self.set_header("Content-Type", "application/json; charset=UTF-8")
                #self.write(data_json)
            else:
                self.write("0")
        else:
            self.write("0")


def query_condition(content):
    query_con = {}
    posstart = content['posstart']
    posend = content['posend']
    vartype = content['vartype']

    if posstart !="-1" and posend!='-1':
        pos_con = {"$gte":int(posstart), "$lte":int(posend)}
        query_con["pos"] = pos_con
    elif posstart !='-1':
        query_con['pos'] = int(posstart)
    elif posend !='-1':
        query_con['pos'] = int(posend)
    else:
        pass

    query_con['chr'] = content['chr']

    if vartype !='-1':
        query_con['vartype'] = vartype

    return query_con
