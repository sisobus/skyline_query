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
with open('json/hotel_WGS84.json','r') as fp:
    r = json.loads(fp.read())
for hotel in r:
    with connect.cursor() as cursor:
        sql = 'insert into `hotel_information` (`hotel_name`,`hotel_latitude`,`hotel_longitude`,`hotel_price`,`hotel_star`) values (%s,%s,%s,%s,%s)'
        print sql
        print type(hotel['price'])
        cursor.execute(sql,(hotel['title'],hotel['latitude'],hotel['longitude'],hotel['price'],hotel['star']))
    connect.commit()

