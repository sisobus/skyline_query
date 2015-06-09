#!/usr/bin/python
#-*- coding:utf-8 -*-
import pymysql.cursors
import json

connect = pymysql.connect(host='localhost',
        user='dongja777',
        passwd='1212',
        db='MP',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )
with open('json/beach_WGS84.json','r') as fp:
    r = json.loads(fp.read())
for beach in r:
    with connect.cursor() as cursor:
        sql = 'insert into `beach_information` (`beach_name`,`beach_latitude`,`beach_longitude`) values (%s,%s,%s)'
        print sql
        cursor.execute(sql,(beach['title'],beach['latitude'],beach['longitude']))
    connect.commit()
