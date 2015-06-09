#!/usr/bin/python
#-*- coding:utf-8 -*-
# KTM > wgs84
import json
import sys
import urllib
import random

#api_key = '73483e276e4684fb783b17ea29da761a'
api_key = '8a14206371f4c0a19545abafc6087307'
url = 'https://apis.daum.net/local/geo/transcoord?apikey='+api_key
print 'input json file name $ '
r = lambda:sys.stdin.readline()
json_file_name = str(r()).rstrip()

with open('json/'+json_file_name) as fp:
    r = json.loads(fp.read())

price_pool = [ i for i in xrange(200000,600001,20000) ]
star_pool  = [ i for i in xrange(1,6,1) ]
ret = []
for data in r:
    title = data['title']
    mapx = data['mapx']
    mapy = data['mapy']
    if json_file_name == 'hotel.json':
        price = price_pool[random.randrange(0,len(price_pool))]
        star = star_pool[random.randrange(0,len(star_pool))]

    full_url = url+'&fromCoord=KTM&y='+mapy+'&x='+mapx+'&toCoord=WGS84&output=json'
    print full_url
    source = json.loads(urllib.urlopen(full_url).read())
    if 'y' in source:
        latitude = str(source['y'])
    else:
        continue
    if 'x' in source:
        longitude = str(source['x'])
    else:
        continue
    d = {
        'title':title,
        'latitude':latitude,
        'longitude':longitude,
            }
    if json_file_name == 'hotel.json':
        print title,latitude,longitude,price,star
        d = {
            'title':title,
            'latitude':latitude,
            'longitude':longitude,
            'price':price,
            'star':star,
                }
        ret.append(d)
    else:
        print title,latitude,longitude 
        ret.append(d)
with open('json/'+json_file_name.split('.')[0]+'_WGS84.json','w') as fp:
    fp.write(json.dumps(ret))
