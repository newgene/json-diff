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
        page_size = int(self.get_argument("ps"))
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
            begin_index = (current_page - 1) * page_size
            que = db.find(query_con).skip(begin_index).limit(page_size)
            counts = que.count()
            pages = counts / page_size if counts % page_size == 0 else counts / page_size + 1
            #json_file = u"/static/jsonfile/"+file_name+u".json"
            self.render("query.html", result=que, currentpage=current_page, pages=int(pages))
        else:
            self.render("query.html", result=False)

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
            count = que.count
            if count:
                #lst = [ tornado.escape.json_encode(every) for every in que]
                #data_json = json.dumps(lst, sort_keys=True, indent=2)
                #file_name = str(datetime.datetime.now())
                #file_name = "-".join(file_name.split(' '))
                #json_file = json_dir + file_name + ".json"
                
                #os.system("rm -f "+json_dir+"*.json")
                #with open(json_file, "w") as fj:
                #    fj.write(data_json)
                self.write("1")
            
            else:
                self.write("0")
        else:
            self.write("0")
