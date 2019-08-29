import pandas as pd
import numpy as np
from . import tspmatrix as tsp
import random

def k_medoids(matrix, depot, k=None):
    if k == None:
        clusters = partition_around_medoids(matrix, 1)
        current_best = current_best = clusters['cost']
        for i in range(2, matrix.get_no_rows()):
            current_clusters = partition_around_medoids(matrix, i)
            if (current_best - current_clusters['cost']) > 20000:
                current_best = current_clusters['cost']
                clusters = current_clusters
            else:
                break
    else:
        clusters = partition_around_medoids(matrix, k)

    return format_clusters(clusters, matrix, depot)

def partition_around_medoids(matrix, k):
    if k == 1:
        labels = matrix.index
        medoid = labels[0]
        non_medoids = labels[1:-1]
        row = matrix.get_row(0)
        cost = 0
        for i in range(1, len(row)):
            cost += row[i]

        cluster = {
            medoid: non_medoids,
            'cost': cost
        }
        return cluster
    else:
        no_of_cities = matrix.get_no_rows()
        if k >= no_of_cities - 1:
            k = no_of_cities - 1
        medoids, non_medoids = arbitary_select(matrix, k)
        current_best = assign_to_medoids(matrix, medoids)
        used_medoids = set(medoids)

        while len(used_medoids) != no_of_cities:
            new_medoid = random_non_medoid(non_medoids)
            used_medoids.add(new_medoid)

            closer_medoid = closer_to(matrix, new_medoid, medoids)[0]

            tmp_medoids = medoids[:]
            tmp_medoids.remove(closer_medoid)
            tmp_medoids.append(new_medoid)

            tmp_non_medoids = non_medoids[:]
            tmp_non_medoids.remove(new_medoid)
            tmp_non_medoids.append(closer_medoid)
            tmp_clusters = assign_to_medoids(matrix, tmp_medoids)

            if tmp_clusters['cost'] < current_best['cost']:
                current_best = tmp_clusters
                medoids = tmp_medoids[:]
                non_medoids = tmp_non_medoids[:]

        return current_best

def random_non_medoid(non_medoids):
    n_m_i = random.randint(0, len(non_medoids) - 1)
    return non_medoids[n_m_i]

def closer_to(matrix, city, medoids):
    closest_distance = np.inf
    for m in medoids:
        distance = matrix[m][city]
        if distance < closest_distance:
            closest_city = m
            closest_distance = distance
    return closest_city, closest_distance

def arbitary_select(matrix, k):
    no_cities = matrix.get_no_rows() - 1
    non_medoids = list(matrix.index)

    medoids = []
    while len(medoids) != k:
        m_i = random.randint(0, no_cities)
        m = non_medoids[m_i]
        if not m in medoids:
            medoids.append(m)
    for m in medoids:
        non_medoids.remove(m)

    return medoids, non_medoids

def assign_to_medoids(matrix, medoids):
    clusters = {}
    cities = matrix.index
    cost = 0

    for m in medoids:
        clusters[m] = []

    for city in cities:
        if not city in medoids:
            closest_city, closest_distance = closer_to(matrix, city, medoids)
            cost += closest_distance
            clusters[closest_city].append(city)

    clusters['cost'] = cost
    return clusters

def format_clusters(clusters, matrix, depot):
    clusters.pop('cost', None)
    if len(clusters) == 1:
        cluster_list = [matrix]
    else:
        cluster_list = []
        for k in clusters:
            labels = [depot]
            if k != depot:
                labels.append(k)
            for v in clusters[k]:
                if v != depot:
                    labels.append(v)

            size = len(labels)

            if size > 1:
                cluster_data = np.matrix(np.ones((size,size)) * np.inf)
                for r_i in range(size):
                    for c_i in range(size):
                        if r_i != c_i:
                            row_label = labels[r_i]
                            col_label = labels[c_i]
                            distance = matrix[col_label][row_label]
                            cluster_data.itemset(r_i, c_i, distance)
                cluster_matrix = tsp.TspMatrix(cluster_data, labels, labels)
                cluster_list.append(cluster_matrix)

    return cluster_list
