#!/usr/bin/env python
#coding:utf-8

import pymongo

#连接mongodb
conn = pymongo.Connection("localhost", 27017)

#连接数据库
db = conn.genetest

#参与比较的两个数据库, newdb .vs. lastdb

lastdb = db.genedoc_mygene_20141019_efqag2hg
newdb = db.genedoc_mygene_20141026_g6svo5ct

#比较结果存储数据库

db_add = db.genedoc_add
db_del = db.genedoc_del
db_upd = db.genedoc_upd
