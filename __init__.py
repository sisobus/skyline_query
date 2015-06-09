# -*- coding:utf-8 -*-
import math
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dongja777:1212@localhost/MP'
def calculateDistance(lat1, long1, lat2, long2):
    lat1 = float(lat1)
    long1 = float(long1)
    lat2 = float(lat2)
    long2 = float(long2)
    R = 6371
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * R

class Hotel_information(db.Model):
    __tablename__ = 'hotel_information'
    hotel_id = db.Column(db.Integer, primary_key = True)
    hotel_name = db.Column(db.String(45))
    hotel_latitude = db.Column(db.Float)
    hotel_longitude = db.Column(db.Float)
    hotel_price = db.Column(db.Integer)
    hotel_star = db.Column(db.Integer)

class Beach_information(db.Model):
    __tablename__ = 'beach_information'
    beach_id = db.Column(db.Integer, primary_key = True)
    beach_name = db.Column(db.String(45))
    beach_latitude = db.Column(db.Float)
    beach_longitude = db.Column(db.Float)

# menu - 0 : 가격, 거리
# menu - 1 : 별점, 가격
# menu - 2 : 별점, 거리
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.id = 0
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id
    def __lt__(self,other):
        if self.x == other.x:
            return self.y > other.y
        return self.x < other.x
def ccw(A, B, C):
    """Tests whether the turn formed by A, B, and C is ccw"""
    return (B.x - A.x) * (C.y - A.y) > (B.y - A.y) * (C.x - A.x)
def intersect(a1, b1, a2, b2):
    """Returns True if line segments a1b1 and a2b2 intersect."""
    return ccw(a1, b1, a2) != ccw(a1, b1, b2) and ccw(a2, b2, a1) != ccw(a2, b2, b1)


@app.route("/skyline_query/<string:latitude>/<string:longitude>/<string:range_distance>/<string:query_type>",methods=['GET'])
def skyline_query(latitude,longitude,range_distance,query_type):
    if request.method == 'GET':
        latitude = float(latitude)
        longitude = float(longitude)
        range_distance = float(range_distance)
        menu = int(query_type)

        query = 'select *  from hotel_information'
        hotels_tmp = Hotel_information.query.from_statement(query).all()
        hotels = []
        for hotel in hotels_tmp:
            dist = calculateDistance(hotel.hotel_latitude,hotel.hotel_longitude,latitude,longitude)
            if dist <= range_distance:
                hotels.append(hotel)
        points = []
        if menu == 0:
            i = 0
            for hotel in hotels:
                dist = calculateDistance(hotel.hotel_latitude,hotel.hotel_longitude,latitude,longitude)
                p = Point(float(hotel.hotel_price),float(dist),int(i))
                i = i + 1
                points.append(p)
        elif menu == 1:
            i = 0
            for hotel in hotels:
                dist = calculateDistance(hotel.hotel_latitude,hotel.hotel_longitude,latitude,longitude)
                p = Point(float(hotel.hotel_star),float(hotel.hotel_price),int(i))
                i = i + 1
                points.append(p)
        elif menu == 2:
            i = 0
            for hotel in hotels:
                dist = calculateDistance(hotel.hotel_latitude,hotel.hotel_longitude,latitude,longitude)
                p = Point(float(hotel.hotel_star),float(dist),int(i))
                i = i + 1
                points.append(p)

        points.sort()
        result_of_skyline = []
        result_of_skyline.append(points[0].id)
        prev_y = points[0].y
        for i in xrange(1,len(points)):
            if prev_y >= points[i].y:
                result_of_skyline.append(points[i].id)
                prev_y = points[i].y

        result_of_hotel = []
        for point in result_of_skyline:
            result_of_hotel.append(hotels[point])

        json_results = []
        for hotel in result_of_hotel:
            d = {
                'id': hotel.hotel_id,
                'hotel_name':hotel.hotel_name,
                'hotel_latitude':hotel.hotel_latitude,
                'hotel_longitude':hotel.hotel_longitude,
                'hotel_price':hotel.hotel_price,
                'hotel_star':hotel.hotel_star,
                }
            json_results.append(d)
        return jsonify(result=json_results)

if __name__ == "__main__":
    app.run(host='163.239.23.231',debug=True)
