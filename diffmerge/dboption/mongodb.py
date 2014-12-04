#!/usr/bin/env python
#coding:utf-8

import pymongo

#避免出现乱码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#连接mongodb
conn = pymongo.Connection("localhost", 27017)

#连接数据库
db = conn.genetest

#参与比较的两个数据库, newdb .vs. lastdb

#lastdb = db.genedoc_mygene_20141019_efqag2hg
#newdb = db.genedoc_mygene_20141026_g6svo5ct

#比较结果存储数据库

db_change = db.genechanges

#日志库.说明：genechanges和diffjoblogs中都有key为"timestamp"的key/value
db_logs = db.diffjoblogs
