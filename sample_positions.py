import math
## sampling locations on the grid given a starting lat/lng
## adding in scaling factor so that future versions can dynamically select the size of the overall sampling space
## initial samling grid: 40mi x 40mi

## approx conversions
km_per_deg_lat = 110.574
def km_per_deg_lng(lat):
    return 111.320 * math.cos(math.radians(lat))
mi_per_km = 0.621371


def sample_positions(lat, lng, scale=1, sample_density=1):
    # top left of sample position grid
    km_offset = 6 * scale * 1/mi_per_km
    deg_offset_west_edge = km_offset * 1/km_per_deg_lng(lat)
    west_edge = lng - deg_offset_west_edge
    deg_offset_north_edge = km_offset * 1/km_per_deg_lat
    north_edge = lat + deg_offset_north_edge
    top_left = north_edge, west_edge


    # from here we can easily define every sampling position in our grid.
    # again we include a scale factor for sampling density for later expansion if desired
    sample_per_dimension = 25 * sample_density
    step_size_deg_lat = 2 * abs(abs(lat)-abs(north_edge)) / sample_per_dimension
    step_size_deg_lng = 2 * abs(abs(lng)-abs(west_edge)) / sample_per_dimension

    sample_positions = [] # sample_positions :: List[Tuple]
    for x in range(sample_per_dimension):
        for y in range(sample_per_dimension):
            sample_positions.append((north_edge - step_size_deg_lat*y, west_edge + step_size_deg_lat*x))

    return sample_positions

#print(sample_positions(38.392, -122.671))
#determined to be pertty good fill at current circle size - 1050m : 16samp_per_dim, 12km_offset

