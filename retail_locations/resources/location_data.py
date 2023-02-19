from retail_locations.resources import get_resource
from math import cos, asin, sqrt


def zip_codes():
    '''A list of known US Zip Codes'''
    return get_resource('zip_codes.json')


def us_states():
    '''A list of US states, with lat & lon'''
    return get_resource('us_states.json')


def us_states_names():
    return [value['state'].upper() for value in us_states()]


def us_states_abbreviations():
    return [value['abbreviation'] for value in us_states()]


def get_zipcode_coordinates(zip_code):

    all_zip_codes = zip_codes()

    zip_code = [item for item in all_zip_codes if item['zipcode'] == zip_code]
    if zip_code:
        return zip_code[0]
    return {}


def get_zipcode_from_coordinates(lat, lon):
    all_zipcode_distances = []
    zipcodes = zip_codes()

    for zip_code in zipcodes:
        zipcode_distance = distance(lat, lon, zip_code['latitude'], zip_code['longitude'])
        all_zipcode_distances.append({
            'zipcode': zip_code['zipcode'],
            'distance': zipcode_distance
        })

    return min(all_zipcode_distances, key=lambda x: x['distance'])['zipcode']


def zipcode_grid(radius):
    '''Returns a variable-radius grid of zipcodes. Radius in kilometers.'''
    all_zipcodes = zip_codes()
    zipcode_grid = []

    while all_zipcodes:
        testzip = all_zipcodes.pop()
        all_zipcodes = [zipcode for zipcode in all_zipcodes if distance(testzip['latitude'], testzip['longitude'], zipcode['latitude'], zipcode['longitude']) > radius]
        zipcode_grid.append(testzip)

    return zipcode_grid


def distance(lat, lng, other_lat, other_lng):
    # Returns distance in kilometers
    lat, lng, other_lat, other_lng = map(float, (lat, lng, other_lat, other_lng))

    p = 0.017453292519943295
    a = 0.5 - cos((other_lat - lat) * p) / 2 + cos(lat * p) * cos(other_lat * p) * (1 - cos((other_lng - lng) * p)) / 2
    return 12742 * asin(sqrt(a))
