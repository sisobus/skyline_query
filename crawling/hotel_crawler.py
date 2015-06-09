#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import json
import urllib
import feedparser
import random

base_url = 'http://openapi.naver.com/search?'
key = 'f2f2be9e7b97d7bf586fce2917d25603'
target = 'local'
query = '해운대호텔'
display = '10'
start = '1'

with open('json/hotel.json','r') as fp:
    ret = json.loads(fp.read())
for st in xrange(1,5000,10):
    print st
    start = str(st)
    full_url = base_url + 'key=' + key + '&target=' + target + '&query=' + query + '&display=' + display + '&start=' + start
    source = feedparser.parse(full_url)
    if len(source['items']) == 0:
        print 'end'
        break

    for item in source['items']:
        d = {
            'title': item['title'],
            'mapx' : item['mapx'],
            'mapy' : item['mapy'],
                }
        ret.append(d)

with open('json/hotel.json','w') as fp:
    fp.write(json.dumps(ret))
