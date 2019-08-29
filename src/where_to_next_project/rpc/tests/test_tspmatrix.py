from django.test import TestCase
import pytest
import numpy as np
import rpc.tspmatrix as tsp


@pytest.fixture
def matrix():
    data = np.matrix(
    [[np.inf,10,8,9,7]
    ,[10,np.inf,10,5,6]
    ,[8,10,np.inf,8,9]
    ,[9,5,8,np.inf,6]
    ,[7,6,9,6,np.inf]])

    cities = ['a', 'b', 'c', 'd', 'e']

    test_matrix = tsp.TspMatrix(data, row_labels = cities, col_labels = cities)

    return test_matrix

def test___init__(matrix):
    is_valid_matrix = True
    is_valid_row_labels = True
    is_valid_col_labels = True
    is_valid_depot = True
    m = np.matrix(
    [[np.inf,10,8,9,7]
    ,[10,np.inf,10,5,6]
    ,[8,10,np.inf,8,9]
    ,[9,5,8,np.inf,6]
    ,[7,6,9,6,np.inf]])

    for r_i in range(len(m)):
        for c_i in range(len(m)):
            if m.item((r_i, c_i)) != matrix.iloc[c_i][r_i]:
                is_valid_matrix = False
                break

    citiy_names = ['a', 'b', 'c', 'd', 'e']
    row_labels = matrix.index
    col_labels = matrix.columns

    for i in range(len(citiy_names)):
        if row_labels[i] != citiy_names[i]:
            is_valid_row_labels = False
            break
        elif col_labels[i] != citiy_names[i]:
            is_valid_col_labels = False
            break

    if matrix.depot != 'a':
        is_valid_depot = False


    assert is_valid_matrix and is_valid_col_labels and is_valid_row_labels and is_valid_depot

def test_get_no_rows(matrix):
    assert matrix.get_no_rows() == 5

def test_get_no_cols(matrix):
    assert matrix.get_no_cols() == 5

def test_get_row(matrix):
    r0 = np.matrix([[np.inf,10,8,9,7]])
    r1 = np.matrix([[10,np.inf,10,5,6]])
    r2 = np.matrix([[8,10,np.inf,8,9]])
    r3 = np.matrix([[9,5,8,np.inf,6]])
    r4 = np.matrix([[7,6,9,6,np.inf]])

    b0 = np.array_equal(r0, np.matrix(matrix.get_row(0)))
    b1 = np.array_equal(r1, np.matrix(matrix.get_row(1)))
    b2 = np.array_equal(r2, np.matrix(matrix.get_row(2)))
    b3 = np.array_equal(r3, np.matrix(matrix.get_row(3)))
    b4 = np.array_equal(r4, np.matrix(matrix.get_row(4)))

    assert b0 and b1 and b2 and b3 and b4

def test_get_col(matrix):

    c0 = np.matrix([[np.inf,10,8,9,7]])
    c1 = np.matrix([[10,np.inf,10,5,6]])
    c2 = np.matrix([[8,10,np.inf,8,9]])
    c3 = np.matrix([[9,5,8,np.inf,6]])
    c4 = np.matrix([[7,6,9,6,np.inf]])

    b0 = np.array_equal(c0, np.matrix(matrix.get_col(0)))
    b1 = np.array_equal(c1, np.matrix(matrix.get_col(1)))
    b2 = np.array_equal(c2, np.matrix(matrix.get_col(2)))
    b3 = np.array_equal(c3, np.matrix(matrix.get_col(3)))
    b4 = np.array_equal(c4, np.matrix(matrix.get_col(4)))

    assert b0 and b1 and b2 and b3 and b4

def test_sub_row_min(matrix):
    data = np.matrix(
    [[np.inf,3,1,2,0]
    ,[5,np.inf,5,0,1]
    ,[0,2,np.inf,0,1]
    ,[4,0,3,np.inf,1]
    ,[1,0,3,0,np.inf]])

    citiy_names = ['a', 'b', 'c', 'd', 'e']

    m = tsp.TspMatrix(data, citiy_names, citiy_names)
    matrix.sub_row_min()

    assert np.array_equal(m, matrix)

def test_sub_col_min(matrix):
    data = np.matrix(
    [[np.inf,5,0,4,1]
    ,[3,np.inf,2,0,0]
    ,[1,5,np.inf,3,3]
    ,[2,0,0,np.inf,0]
    ,[0,1,1,1,np.inf]])

    citiy_names = ['a', 'b', 'c', 'd', 'e']

    m = tsp.TspMatrix(data, citiy_names, citiy_names)
    matrix.sub_col_min()

    assert np.array_equal(m, matrix)
