import googlemaps
import urllib.request
import json
# import sys
gmaps = googlemaps.Client(key='AIzaSyD8Yd1htLtFUvu5xbRKcBL1ME2lOwrNSzI')

def google_nearest_road(loc, loc2=0):
    """
    loc: lat,lng - no spaces
    return: depending on whether you pass a second location will return one or two
    sets of lat,lng corresponding to neares street location
    """
    GOOGLE_API_KEY = "AIzaSyD8Yd1htLtFUvu5xbRKcBL1ME2lOwrNSzI"
    goog_road_add1 = 'https://roads.googleapis.com/v1/nearestRoads?points='

    loc_segment =  str(loc[0]) + ',' + str(loc[1])
    goog_road_add2 = '&key=' + GOOGLE_API_KEY
    requestStr = goog_road_add1 + loc_segment + goog_road_add2
    response = urllib.request.urlopen(requestStr).read().decode('utf-8')
    json_response = json.loads(response)
    road_loc = json_response['snappedPoints'][0]['location']
    lat, lng = road_loc['latitude'], road_loc['longitude']
    return [lat,lng]

def get_transit_time_sec(orig, dest):
    try:
        directions_result = gmaps.directions(orig, dest, mode="transit")
        transit_time_sec = directions_result[0]['legs'][0]['duration']['value']
        return transit_time_sec
    except:
        try:
            dest = google_nearest_road(dest)
            directions_result = gmaps.directions(orig, dest, mode="transit")
            transit_time_sec = directions_result[0]['legs'][0]['duration']['value']
            return transit_time_sec
        except:
            # print("{0} on line {1}".format(sys.exc_info(), sys.exc_info()[2].tb_lineno))
            return -1

