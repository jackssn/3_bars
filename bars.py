import json
import os
import requests
from math import radians, cos, sin, asin, sqrt



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def load_data(filepath):
    if not os.path.exists(filepath):
        url = 'http://api.data.mos.ru/v1/datasets/1796/rows?&$orderby=Number'
        r = requests.get(url)
        return r.json()
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


def get_biggest_bar(data):
    seats_count = [d['Cells']['SeatsCount'] for d in data]
    max_seats = max(seats_count)
    biggest_bar_id = seats_count.index(max_seats)
    return data[biggest_bar_id]


def get_smallest_bar(data):
    seats_count = [d['Cells']['SeatsCount'] for d in data]
    min_seats = min(seats_count)
    smallest_bar_id = seats_count.index(min_seats)
    return data[smallest_bar_id]


def get_closest_bar(data, longitude, latitude):
    gps_all_bars = [d['Cells']['geoData']['coordinates'][::-1] for d in data]
    differences = [haversine(longitude, latitude, gps[0], gps[1]) for gps in gps_all_bars]
    closest_bar_id = differences.index(min(differences))
    return data[closest_bar_id]

if __name__ == '__main__':
    filepath = input('Type full path to json-file or press Enter to download the data from api:\n')
    while 1:
        try:
            longitude = float(input('Type your longitude: '))
            latitude = float(input('Type your latitude: '))
            if latitude and longitude:
                break
        except ValueError:
            print('Incorrect gps coordinates. Try again')

    data = load_data(filepath)

    biggest_bar = get_biggest_bar(data)
    smallest_bar = get_smallest_bar(data)
    closest_bar = get_closest_bar(data, longitude, latitude)


    print('The biggest bar in Moscow has %s number. You can look at that pub here: \
http://data.mos.ru/opendata/7710881420-bary/row/%s' % (biggest_bar['Number'], biggest_bar['Cells']['global_id']))

    print('The smallest bar in Moscow has %s number. You can look at that pub here: \
http://data.mos.ru/opendata/7710881420-bary/row/%s' % (smallest_bar['Number'],smallest_bar['Cells']['global_id']))

    print('The closest bar in Moscow has %s number. You can look at that pub here: \
http://data.mos.ru/opendata/7710881420-bary/row/%s' % (closest_bar['Number'], closest_bar['Cells']['global_id']))