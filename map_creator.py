from __future__ import print_function
import coloring
import transit_time
import sample_positions

## input arg :: center of the map
center = (34.098,-118.2880)
sample_positions = sample_positions.sample_positions(center[0], center[1])
locs_w_time = []

## sample slice
# sample_positions = sample_positions[100:110]

def find_travel_times(center, dests):
    for dest in dests:
        travel_time_sec = transit_time.get_transit_time_sec(center, dest)
        if travel_time_sec != -1:
            locs_w_time.append((dest, travel_time_sec))
    return locs_w_time

# find the percentile in this data set for a given travel time
def time_ptile(sec, locs_w_time):
    n = len(locs_w_time)
    less = 0
    for loc_time in locs_w_time:
        if loc_time[1] <= sec:
            less += 1
    return int(less/n * 100)


# todo: calculate radius below based on the scale of the map and #sample positions for best filling
class Map(object):
    def __init__(self):
        self._points = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def __str__(self):
        # centerLat = sum(( x[0] for x in self._points )) / len(self._points)
        # centerLon = sum(( x[1] for x in self._points )) / len(self._points)
        centerLat = center[0]
        centerLon = center[1]
        markersCode = "\n".join(
            [ """new google.maps.Circle({{
                  strokeColor: '#ffffff',
                  strokeOpacity: 0.99,
                  strokeWeight: 2,
                  fillColor: '{color}',
                  fillOpacity: 0.35,
                  map: map,
                  center: new google.maps.LatLng({lat}, {lon}),
                  radius: 375
                }});""".format(lat=x[0], lon=x[1], color=x[2]) for x in self._points
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 12,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)


if __name__ == "__main__":
        map = Map()
        locs_w_time = find_travel_times(center, sample_positions)
        # print(len(sample_positions))
        for loc in locs_w_time:
            lat = loc[0][0]
            lng = loc[0][1]
            map.add_point((lat, lng, coloring.color(time_ptile(loc[1], locs_w_time))))
            # print(loc, time_ptile(loc[1], locs_w_time))

        with open("output.html", "w") as out:
             print(map, file=out)

# todo: i'd like to tie the size of the circle to the aproxDist/time (shows relative speed of travel)
