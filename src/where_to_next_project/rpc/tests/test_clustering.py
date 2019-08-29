from django.test import TestCase
import pytest
import numpy as np
import rpc.tspmatrix as tsp
import rpc.clustering as clustering



@pytest.fixture
def matrix():
    data = np.matrix(
    [[np.inf, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
    [29,  np.inf, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
    [82, 55,  np.inf, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
    [46, 46, 68,  np.inf, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
    [68, 42, 46, 82,  np.inf, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
    [52, 43, 55, 15, 74,  np.inf, 61, 23, 55, 31, 33, 37, 51, 29, 59],
    [72, 43, 23, 72, 23, 61,  np.inf, 42, 23, 31, 77, 37, 51, 46, 33],
    [42, 23, 43, 31, 52, 23, 42,  np.inf, 33, 15, 37, 33, 33, 31, 37],
    [51, 23, 41, 62, 21, 55, 23, 33,  np.inf, 29, 62, 46, 29, 51, 11],
    [55, 31, 29, 42, 46, 31, 31, 15, 29,  np.inf, 51, 21, 41, 23, 37],
    [29, 41, 79, 21, 82, 33, 77, 37, 62, 51,  np.inf, 65, 42, 59, 61],
    [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65,  np.inf, 61, 11, 55],
    [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61,  np.inf, 62, 23],
    [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62,  np.inf, 59],
    [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59,  np.inf]])

    cities = ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15']

    test_matrix = tsp.TspMatrix(data, row_labels = cities, col_labels = cities)

    return test_matrix

def test_arbitary_select(matrix):
    correct_no_medoids = True
    distinct_medoids = True
    distinct_medoids_non_medoids = True
    k=7
    medoids, non_medoids = clustering.arbitary_select(matrix, k)

    if len(medoids) != 7:
        correct_no_medoids == False

    distinct_medoids = set(medoids)
    if len(medoids) != len(distinct_medoids):
        distinct_medoids = False

    for n_m in non_medoids:
        if n_m in medoids:
            distinct_medoids_non_medoids = False

    assert correct_no_medoids and distinct_medoids and distinct_medoids_non_medoids

def test_assign_to_medoids(matrix):
    assigned_to_predefined_m = True
    test_medoids = cities = ['c1','c2','c3','c13','c14','c15']
    clusters = clustering.assign_to_medoids(matrix, test_medoids)

    for k in clusters:
        if not k in test_medoids and k != 'cost':
            assigned_to_predefined_m = False
            break

    assert assigned_to_predefined_m

def test_closer_to(matrix):
    valid_closer_to = True
    cities = ['c1','c2','c3','c13','c14','c15']
    closest_cities = ['c13','c13','c12','c2', 'c12', 'c9']
    medoids =['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15']

    for i in range(len(cities)):
        closest_c, distance = clustering.closer_to(matrix, cities[i], medoids)
        if closest_c != closest_cities[i]:
            valid_closer_to = False

    assert valid_closer_to

def test_random_non_medoid():
    is_valid_non_medoid = True
    test_non_medoids = cities = ['c1','c2','c3','c13','c14','c15']

    for i in range(5):
        random_non_medoid = clustering.random_non_medoid(test_non_medoids)
        if not random_non_medoid in test_non_medoids:
            is_valid_non_medoid = False
            break

    assert is_valid_non_medoid

def test_partition_around_medoids(matrix):
    is_valid_clusters = True

    for k in range(1,7):
        clusters = clustering.partition_around_medoids(matrix, k)
        if len(clusters) - 1 != k:
            is_valid_clusters = False
            break

    assert is_valid_clusters

def test_k_medoids(matrix):
    valid_no_clusters = True
    distinct_clusters = True
    all_contain_depot = True

    depot = 'c1'
    k = 2
    clusters = clustering.k_medoids(matrix, depot= depot, k = 2)
    if len(clusters) != k:
        valid_no_clusters = False

    for i in range(len(clusters)):
        c = clusters[i]
        c_cities = c.index
        if c_cities[0] != depot:
            all_contain_depot = False
        for j in range(i, len(clusters)):
            tmp_cluster = clusters[j]
            for city in c_cities:
                if city != depot and city in tmp_cluster.index:
                    distinct_clusters = False
