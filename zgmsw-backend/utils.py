# -*- coding: utf-8 -*-
#coding=utf-8

def uuidgen():
    import uuid
    return str(uuid.uuid4())

def hashgen(s):
    import hashlib
    return hashlib.sha224(s).hexdigest()

import math 
x_pi = math.pi * 3000.0 / 180.0

def autOfChina(lat, lon):
        if lon < 72.004 or lon > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False
   
def transformLat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret

def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def delta(lat, lon):
    #Krasovsky 1940
    #
    # a = 6378245.0, 1/f = 298.3
    # b = a * (1 - f)
    # ee = (a^2 - b^2) / a^2
    a = 6378245.0 #  a: 卫星椭球坐标投影到平面地图坐标系的投影因子。
    ee = 0.00669342162296594323 #  ee: 椭球的偏心率。
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)
    return (dLat, dLon)
     
#WGS-84 to GCJ-02
def gcj_encrypt(wgsLat, wgsLon):
    if outOfChina(wgsLat, wgsLon):
        return (wgsLat, wgsLon)
 
    dLat, dLon = delta(wgsLat, wgsLon)
    return (wgsLat + dLat, wgsLon + dLon)

#GCJ-02 to WGS-84
def gcj_decrypt(gcjLat, gcjLon):
    if outOfChina(gcjLat, gcjLon):
        return (gcjLat, gcjLon)
         
    dLat, dLon = delta(gcjLat, gcjLon)
    return (gcjLat - dLat, gcjLon - dLon)


#GCJ-02 to BD-09
def bd_encrypt(gcjLat, gcjLon):
    x = gcjLon, y = gcjLat 
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    bdLon = z * math.cos(theta) + 0.0065 
    bdLat = z * math.sin(theta) + 0.006
    return (bdLat, bdLon)
 
#BD-09 to GCJ-02
def bd_decrypt(bdLat, bdLon):
    x = bdLon - 0.0065
    y = bdLat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gcjLon = z * math.cos(theta) 
    gcjLat = z * math.sin(theta)
    return (gcjLat, gcjLon)

def distance(latA, lonA, latB, lonB):
    if not latA or not lonA or not latB or not lonB:
        return None

    earthR = 6371000.
    x = math.cos(latA * math.pi / 180.) * math.cos(latB * math.pi / 180.) * math.cos((lonA - lonB) * math.pi / 180)
    y = math.sin(latA * math.pi / 180.) * math.sin(latB * math.pi / 180.)
    s = x + y

    if s > 1: 
        s = 1
    if s < -1: 
        s = -1

    alpha = math.acos(s)
    distance = alpha * earthR
    return distance
