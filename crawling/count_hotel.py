#!/usr/bin/python
#-*- coding:utf-8 -*-
import json

with open('json/hotel_WGS84.json') as fp:
    r = json.loads(fp.read())
print len(r)
