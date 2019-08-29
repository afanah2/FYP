from django.shortcuts import render
from jsonrpc import jsonrpc_method
from . import util, tspmatrix
from . import branch_and_bound as b_n_b
from . import clustering
from . import twice_around_the_tree as tat

@jsonrpc_method('rpc.branch_and_bound')
def branch_and_bound(request, data):
    print('remote procedure called')
    distance_matrix = util.get_distance_matrix(data)

    if data['driver_availability'][0] == 'restricted':
        k = float(data['no_of_drivers'][0])
    else:
        k = None
    depot = distance_matrix.depot
    clusters = clustering.k_medoids(distance_matrix, depot, k)
    response = []

    for c in clusters:
        result = b_n_b.branch_and_bound(c)
        formated_response = util.format_response(result['directions'])
        response.append(formated_response)

    return response

@jsonrpc_method('rpc.twice_around_the_tree')
def twice_around_tree(request, data):
    distance_matrix = util.get_distance_matrix(data)
    print(data['no_of_drivers'][0])

    if data['driver_availability'][0] == 'restricted':
        k = float(data['no_of_drivers'][0])
    else:
        k = None

    print('----------------->', k)

    depot = distance_matrix.depot
    clusters = clustering.k_medoids(distance_matrix, depot, k)
    response = []

    for c in clusters:
        result = tat.twice_around_tree(c)
        formated_response = util.format_response(result['directions'])
        response.append(formated_response)

    return response
