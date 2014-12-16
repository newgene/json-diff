#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.index import IndexHandler
from handler.index import SearchHandler

url=[
    (r'/', IndexHandler),
    (r'/search', SearchHandler),
    ]
