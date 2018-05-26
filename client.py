"""Example of calling OrbitalViews API."""
import argparse
import requests
from six.moves import urllib
from urllib import quote
import time
from datetime import date, timedelta
import datetime

wkt_polygon = "POLYGON ((11.690633296966551 48.40835165604796, 11.689753532409668 48.40620077080685, 11.692006587982178 48.406414438973066, 11.692092418670654 48.40583041052553, 11.695032119750975 48.40611530328899, 11.695418357849121 48.40528910987836, 11.694946289062498 48.40487600814009, 11.695225238800049 48.403636682793305, 11.693959236145018 48.403351776145755, 11.693572998046875 48.40406403977236, 11.68872356414795 48.403636682793305, 11.68872356414795 48.40299564059211, 11.691019535064697 48.403138095112816, 11.69144868850708 48.401485598144106, 11.692264080047607 48.40149984403702, 11.692306995391846 48.401699286119154, 11.694366931915283 48.401656548595966, 11.694452762603758 48.40182749847331, 11.696641445159912 48.4018702358529, 11.696598529815674 48.40147135224718, 11.697134971618652 48.40149984403702, 11.697156429290771 48.401799006867, 11.697843074798584 48.40182749847331, 11.699130535125732 48.402354590311774, 11.698658466339111 48.40463384349218, 11.70046091079712 48.40496147774052, 11.700310707092285 48.40570220826134, 11.69994592666626 48.40584465520161, 11.6998815536499 48.40604408024776, 11.699044704437256 48.40654263944192, 11.69638395309448 48.40729759120356, 11.690633296966551 48.40835165604796))"
fieldname = "API_bla_CallTestMontag"
filename = "APICallTestMontag_RGB_2017-05-14.tif"

def serveImage_request(host, api_key):

    url = urllib.parse.urljoin(host, '/api/v1/image/{}'.format(
    quote(filename)))

    ''' format: rj stands for jpg. Please check the documentation for further options'''
    params = {
        'apikey': api_key,
        'format': "rj",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def list_request(host, api_key):
    
    url = urllib.parse.urljoin(host, '/api/v1/images/ls/{}'.format(
    quote(fieldname)))

    params = {
        'apikey': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def register_request(host, api_key, wkt):
    url = urllib.parse.urljoin(host, '/api/v1/register_field/')
    
    params = {
        'apikey': api_key,
        'fieldname': fieldname,
        'maptype': "rgb",
        'startdate': "2017-04-01",
        'enddate': "2017-06-01",
    }

    response = requests.post(url, params=params, json=wkt)
    response.raise_for_status()
    return response.text

def weather_request(host, api_key,lat ,lng):
    url = urllib.parse.urljoin(host, '/api/v1/weather/current')
    params = {
        'apikey': api_key,
        'lat': lat,
        'lng': lng,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def daily_weather_request(host, api_key,lat ,lng, date):
    url = urllib.parse.urljoin(host, '/api/v1/weather/daily')
    
    params = {
        'apikey': api_key,
        'lat': lat,
        'lng': lng,
        'date': date,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def hourly_weather_request(host, api_key,lat ,lng, date):
    url = urllib.parse.urljoin(host, '/api/v1/weather/hourly')
    
    params = {
        'apikey': api_key,
        'lat': lat,
        'lng': lng,
        'date': date,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def elevation_request(host, api_key, wkt):
    url = urllib.parse.urljoin(host, '/api/v1/elevation/')
    params = {
        'apikey': api_key
    }

    #wkt = {"WKTPolygon": data}
    response = requests.post(url, params=params, json=wkt)
    response.raise_for_status()
    return response.text

def main(host, api_key, lat, lng):
    '''elevation request for wkt polygon'''
    response = elevation_request(host, api_key, wkt_polygon)
    #print(response)
    
    '''get the weather data for lat,lng'''
    response = weather_request(host, api_key, lat, lng)
    #print(response)
    
    '''get the daily weather data for lat,lng'''
    _time = datetime.datetime.utcnow() + timedelta(days=-50)
    #_time = datetime.datetime(2016, 11, 15, 9, 59, 25, 608206)
    print _time
    response = daily_weather_request(host, api_key, lat, lng, _time)
    print(response)
    
    '''get hourly weather data for lat,lng'''
    #response = hourly_weather_request(host, api_key, lat, lng, _time)
    #print(response)
    
    '''register a field ...takes some minutes'''
    response = register_request(host, api_key, wkt_polygon)
    print(response)
    
    #time.sleep(40)
    '''list images for fieldname'''
    response = list_request(host, api_key)
    print(response)
    
    '''serve an image highly optimized'''
    response = serveImage_request(host, api_key)
    print(response)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'host', help='Your API host, e.g. https://api.orbitalviews.eu/')
    parser.add_argument(
        'api_key', help='Your API key.')
    parser.add_argument(
        'lat',
        help='latitude')
    parser.add_argument(
        'lng',
        help='longitude')

    args = parser.parse_args()

    main(args.host, args.api_key, args.lat, args.lng)
