import json
import urllib.request
import numpy as np
import pandas as pd
from ast import literal_eval
from . import tspmatrix as tsp

api_key = ''

def get_city_names(cities):
    city_names = cities.split('|')[:-1]
    return city_names

def get_formated_cities(locations):
    for i in range(len(locations)):
        locations[i] = locations[i].replace(" ", "")
    return "|".join(locations)

def np_matrix_format(rows):
    size = len(rows)
    matrix = np.matrix(np.ones((size,size)) * np.inf)
    for r_i in range(size):
        row = rows[r_i]['elements']
        for c_i in range(size):
            if r_i != c_i:
                dist = row[c_i]['distance']['value']
                matrix.itemset(r_i, c_i, dist)
    return matrix

def get_row(origin, destinations):
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?&origins={}&destinations={}&key='.format(origin,destinations)
    request_url = endpoint + api_key
    response = urllib.request.urlopen(request_url).read()
    distances = json.loads(response)
    response = urllib.request.urlopen(request_url).read()
    distances = json.loads(response)
    row = distances['rows'][0]
    return row

def get_distance_matrix(data):
    cities = data['cities'][0]
    city_names = get_city_names(cities)
    formated_city_names = get_formated_cities(city_names[:])
    rows = []
    origins = formated_city_names.split('|')
    for origin in origins:
        row = get_row(origin, formated_city_names)
        rows.append(row)

    matrix = np_matrix_format(rows)
    tsp_matrix = tsp.TspMatrix(matrix, row_labels = city_names, col_labels = city_names)

    return tsp_matrix

def format_response(directions):
    depot = (directions[0][0]).replace(" ", "")
    waypoints = []
    for i in range(1, len(directions)):
        city = directions[i][0]
        formated_city = city.replace(" ", "")
        waypoints.append(formated_city)
    response = {
        "depot": depot,
        "waypoints": waypoints
    }
    return response
