#!/usr/bin/env python
#coding:utf-8

import tornado.web
import json
import urllib

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


class SearchHandler(tornado.web.RequestHandler):
    #def post(self):
    def get(self):
        content = self.get_argument("data")
        content = tornado.escape.json_decode(content)
        
        
        data_web = "http://myvariant.info/v1/"
        query_con = query_condition(content)
        query_url = data_web + query_con

        print query_url

        response = urllib.urlopen(query_url)
        response_text = response.read()
        result = tornado.escape.json_decode(response_text)
        result_hits = result['hits']
        counts = result['total']

        return_data = {}

        if counts:
            search_value = [ line['wellderly'] for line in result_hits ]
            #counts = len(search_value)
            print counts
            
            nowpage = int(content['nowpage'])
            page_size = int(content['pagesize'])
            pages = counts / page_size if counts % page_size == 0 else counts / page_size + 1

            return_data['value'] = search_value
            return_data['counts'] = counts
            return_data['pages'] = pages
            return_data['currentpage'] = nowpage 
            
            display_format = content['format']
            return_data['format'] = display_format

            if display_format == "table":
                data_json = json.dumps(return_data)
                self.write(data_json)
            elif display_format == "json":
                data_json = json.dumps(return_data['value'], indent=2)
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(data_json)
            else:
                self.write("0")
        else:
            self.write("0")


def query_condition(content):
    
    q = "query?q=_exists_:wellderly"
    
    gene = content['gene']
    gene_chr = content['chr']
    posstart = content['posstart']
    posend = content['posend']
    vartype = content['vartype']
    
    nowpage = str(int(content['nowpage'])-1)
    pagesize = content['pagesize']

    if gene != '-1':
        q += " AND wellderly.gene:" + gene
    
    if gene_chr != '-1':
        q += " AND wellderly.chr:" + gene_chr

    if posstart !="-1" and posend!='-1':
        q += " AND wellderly.pos:[" + posstart + " TO " + posend +"]"
    elif posstart !='-1':
        q += " AND wellderly.pos:" + posstart
    elif posend !='-1':
        q += " AND wellderly.pos:" + posend
    else:
        pass

    if vartype != '-1':
        q += " AND wellderly.vartype:" + vartype
    
    q += "&fields=wellderly&from=" + nowpage +"&size=" + pagesize
    
    return q 

def query_page(nowpage, pagesize):
    q_page = "&fields=wellderly&from=" + nowpage +"&size=" + pagesize
    return q_page
    
