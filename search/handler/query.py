#!/usr/bin/env python
#coding:utf-8

import tornado.web

from db.db import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QueryGene(tornado.web.RequestHandler):
    def post(self):
        pos_start = self.get_argument("posstart")
        pos_end = self.get_argument("posend")
        genechr = self.get_argument("genechr")
        vartype = self.get_argument("vartype")
        generef = self.get_argument("generef")
        
        query_con = {}
        
        if pos_start and pos_end:
            pos_con = {"$gte":int(pos_start), "$lte":int(pos_end)}
            query_con["pos"] = pos_con
        elif pos_start:
            query_con["pos"] = int(pos_start)
        elif pos_end:
            query_con["pos"] = int(pos_end)
        else:
            pass

        if genechr:
            query_con["chr"] = genechr

        if vartype:
            query_con["vartype"] = vartype

        if generef:
            query_con["ref"] = generef

        if query_con:
            que = db.find(query_con)
            #print list(que)
            if que.count():
                self.render("query.html", result=que)
            else:
                self.render("query.html", result=False)
        else:
            self.render("query.html", result=False)
