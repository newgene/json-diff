#!/usr/bin/env python
#coding:utf-8

import pymongo

conn = pymongo.Connection("localhost", 27017)

db = conn.genetest

#>>> db = conn.genetest
print db.collection_names()
#[u'system.indexes', u'genedoc_mygene_20141026_g6svo5ct', u'genedoc_mygene_20141019_efqag2hg']

db_g19 = db.genedoc_mygene_20141019_efqag2hg
db_g26 = db.genedoc_mygene_20141026_g6svo5ct
