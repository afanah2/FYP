from django.test import TestCase
import pytest
import numpy as np
import rpc.tspmatrix as tsp
import rpc.branch_and_bound as b_n_b



@pytest.fixture
def tree():
    data = np.matrix(
    [[np.inf,10,8,9,7]
    ,[10,np.inf,10,5,6]
    ,[8,10,np.inf,8,9]
    ,[9,5,8,np.inf,6]
    ,[7,6,9,6,np.inf]])

    cities = ['a', 'b', 'c', 'd', 'e']

    test_matrix = tsp.TspMatrix(data, row_labels = cities, col_labels = cities)
    test_tree = b_n_b.BranchAndBoundTree(test_matrix)

    return test_tree

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


def test__init__(tree, matrix):
    is_valid_matrix = True
    is_valid_parent = True
    is_valid_directions = True
    is_valid_current_path = True
    is_valid_sorted_directions = True
    is_valid_upper_bound = True
    is_valid_left_child = True
    is_valid_right_child = True



    if np.array_equal(tree.matrix, matrix):
        is_valid_matrix = False

    if tree.parent != None:
        is_valid_parent = False

    if tree.directions != [] or len(tree.directions) > 0:
        is_valid_directions = False

    if tree.sorted_directions != None:
        is_valid_sorted_directions = False

    if tree.current_path == 'l' or tree.current_path == 'r':
        is_valid_current_path = False

    if tree.is_upper_bound == True:
        is_valid_upper_bound = False

    if tree.right_child != None:
        is_valid_right_child = False

    if tree.left_child != None:
        is_valid_left_child = False

    assert(
        is_valid_matrix and is_valid_parent and is_valid_directions and
        is_valid_sorted_directions and is_valid_upper_bound and is_valid_right_child and
        is_valid_left_child
        )

def test_insert_right(tree, matrix):
    is_valid_insertion = True
    row_removed = True
    col_removed = True
    updated_cost = True
    depot_unchanged = True


    tree.insert_right()
    right_child = tree.right_child


    if right_child == None:
        is_valid_insertion = False

    if right_child.matrix.get_no_rows() != matrix.get_no_rows() - 1:
        row_removed = False

    if right_child.matrix.get_no_cols() != matrix.get_no_cols() -1:
        col_removed = False

    if right_child.cost == right_child.parent.cost:
        updated_cost = False

    if right_child.matrix.depot != right_child.parent.matrix.depot:
        depot_unchanged = False

    assert( is_valid_insertion and row_removed and col_removed and updated_cost
    and depot_unchanged)

def test_insert_left(tree, matrix):
    is_valid_insertion = True
    added_inf = True
    updated_cost = True
    depot_unchanged = True


    tree.insert_left()
    left_child = tree.left_child


    if left_child == None:
        is_valid_insertion = False

    if len(np.where(left_child.matrix == np.inf)[0]) != len(np.where(left_child.parent.matrix == np.inf)[0]) + 1:
        added_inf = False

    if left_child.cost == left_child.parent.cost:
        updated_cost = False

    if left_child.matrix.depot != left_child.parent.matrix.depot:
        depot_unchanged = False

    assert( is_valid_insertion and added_inf and updated_cost and depot_unchanged)


def test_insert_right(tree, matrix):
    is_valid_insertion = True
    row_removed = True
    col_removed = True
    updated_cost = True
    depot_unchanged = True


    tree.insert_right()
    right_child = tree.right_child


    if right_child == None:
        is_valid_insertion = False

    if right_child.matrix.get_no_rows() != matrix.get_no_rows() - 1:
        row_removed = False

    if right_child.matrix.get_no_cols() != matrix.get_no_cols() -1:
        col_removed = False

    if right_child.cost == right_child.parent.cost:
        updated_cost = False

    if right_child.matrix.depot != right_child.parent.matrix.depot:
        depot_unchanged = False

    assert( is_valid_insertion and row_removed and col_removed and updated_cost
    and depot_unchanged)

def test_back_track(tree):
    valid_back_track = True
    root = tree.parent

    tree.insert_right()
    tree.insert_left()
    right_child = tree.right_child
    left_child = tree.left_child

    left_child.back_track()
    right_child.back_track()

    if right_child.parent != root or left_child.parent != root:
        valid_back_track = False

    assert valid_back_track


def test_sorted_directions(tree): #1-3-5-2-4-1
    sorted_correctly = True
    test_directions = [('a','c') ,('b','d'), ('e','b'), ('c','e'), ('d','a')]
    tree.directions = test_directions
    tree.sort_directions()

    if tree.sorted_directions != [('a','c'),('c','e'),('e','b'),('b','d'),('d','a')]:
        sorted_correctly = False

    assert sorted_correctly

def test_get_first_direction(tree):
    correct_first_direction = True
    test_directions = [('b','d'), ('e','b'), ('a','c'), ('c','e'), ('d','a')]
    tree.directions = test_directions

    if tree.get_first_direction() != ('a','c'):
        correct_first_direction = False

    tree.matrix.depot = 'd'
    if tree.get_first_direction() != ('d','a'):
        correct_first_direction = False

    tree.matrix.depot = 'z'
    if tree.get_first_direction() != -1:
        correct_first_direction = False

    assert correct_first_direction

def test_reduce_matrix(matrix):
    reduced_correctly = True

    m = np.matrix(
    [[np.inf,3,0,2,0]
    ,[5,np.inf,4,0,1]
    ,[0,2,np.inf,0,1]
    ,[4,0,2,np.inf,1]
    ,[1,0,2,0,np.inf]])

    reduced_matrix = b_n_b.reduce_matrix(matrix)

    if not np.array_equal(reduced_matrix, m):
        reduced_correctly = False

    assert reduced_correctly

def test_get_row_pen():
    r1 = np.matrix([[np.inf,3,0,2,0]])
    r2 = np.matrix([[5,np.inf,4,0,1]])
    r3 = np.matrix([[0,2,np.inf,0,1]])
    r4 = np.matrix([[4,0,2,np.inf,1]])
    r5 = np.matrix([[1,0,2,0,np.inf]])

    b1 = True
    b2 = True
    b3 = True
    b4 = True
    b5 = True

    if not(b_n_b.get_row_pen(r1, 2) == 0 or b_n_b.get_row_pen(r1, 4) == 0):
        b1 = False
    if not(b_n_b.get_row_pen(r2, 3) == 1):
        b2 = False
    if not(b_n_b.get_row_pen(r3, 0) == 0 or b_n_b.get_row_pen(r3, 3) == 0):
        b3 = False
    if not(b_n_b.get_row_pen(r4, 1) == 1):
        b4 = False
    if not(b_n_b.get_row_pen(r5, 1) == 0 or b_n_b.get_row_pen(r5, 3) == 0):
        b5 = False

    assert b1 and b2 and b3 and b4 and b5

def test_get_col_pen(matrix):
    reduced_matrix = b_n_b.reduce_matrix(matrix)
    c1 = matrix.get_col(0)
    c2 = matrix.get_col(1)
    c3 = matrix.get_col(2)
    c4 = matrix.get_col(3)
    c5 = matrix.get_col(4)


    b1 = True
    b2 = True
    b3 = True
    b4 = True
    b5 = True

    r1 = np.matrix([[np.inf,3,0,2,0]])
    r2 = np.matrix([[5,np.inf,4,0,1]])
    r3 = np.matrix([[0,2,np.inf,0,1]])
    r4 = np.matrix([[4,0,2,np.inf,1]])
    r5 = np.matrix([[1,0,2,0,np.inf]])

    if not(b_n_b.get_col_pen(c1, 2) == 1):
        b1 = False
    if not(b_n_b.get_col_pen(c2, 3) == 0 or b_n_b.get_col_pen(c2, 4) == 0):
        b2 = False
    if not(b_n_b.get_col_pen(c3, 0) == 2):
        b3 = False
    if not(b_n_b.get_col_pen(c4, 1) == 0 or b_n_b.get_col_pen(c4, 2) == 0 or
    b_n_b.get_row_pen(c4, 4) == 0):
        b4 = False
    if not(b_n_b.get_row_pen(c5, 0) == 1):
        b5 = False

    assert b1 and b2 and b3 and b4 and b5

def test_get_penalty(matrix):
    correct_penalty = True
    reduced_matrix = b_n_b.reduce_matrix(matrix)
    penalty = b_n_b.get_penalty(reduced_matrix)
    direction = penalty[0]
    cost = penalty[1]


    if cost != 2 or direction != ('a','c'):
        correct_penalty = False

    assert correct_penalty

def test_get_subsuquent_direction():
    correct_direction_lookup = True
    test_directions = [('a','c') ,('b','d'), ('e','b'), ('c','e'), ('d','a')]

    d1 = test_directions[0]
    d2 = test_directions[1]
    d3 = test_directions[2]
    d4 = test_directions[3]
    d5 = test_directions[4]
    d6 = ('y','z')

    if b_n_b.get_subsuquent_direction(d1,test_directions) != ('c','e'):
        correct_direction_lookup = False
    if b_n_b.get_subsuquent_direction(d2,test_directions) != ('d','a'):
        correct_direction_lookup = False
    if b_n_b.get_subsuquent_direction(d3,test_directions) != ('b','d'):
        correct_direction_lookup = False
    if b_n_b.get_subsuquent_direction(d4,test_directions) != ('e','b'):
        correct_direction_lookup = False
    if b_n_b.get_subsuquent_direction(d5,test_directions) != ('a','c'):
        correct_direction_lookup = False
    if b_n_b.get_subsuquent_direction(d6,test_directions) != -1:
        correct_direction_lookup = False

    assert correct_direction_lookup

def test_get_previous_direction():
    correct_direction_lookup = True
    test_directions = [('a','c') ,('b','d'), ('e','b'), ('c','e'), ('d','a')]

    d1 = test_directions[0]
    d2 = test_directions[1]
    d3 = test_directions[2]
    d4 = test_directions[3]
    d5 = test_directions[4]
    d6 = ('y','z')

    if b_n_b.get_previous_direction(d1,test_directions) != ('d','a'):
        correct_direction_lookup = False
    if b_n_b.get_previous_direction(d2,test_directions) != ('e','b'):
        correct_direction_lookup = False
    if b_n_b.get_previous_direction(d3,test_directions) != ('c','e'):
        correct_direction_lookup = False
    if b_n_b.get_previous_direction(d4,test_directions) != ('a','c'):
        correct_direction_lookup = False
    if b_n_b.get_previous_direction(d5,test_directions) != ('b', 'd'):
        correct_direction_lookup = False
    if b_n_b.get_previous_direction(d6,test_directions) != -1:
        correct_direction_lookup = False

    assert correct_direction_lookup

def test_branch_and_bound(matrix):
    valid_b_n_b_result = True
    result = b_n_b.branch_and_bound(matrix)
    directions = result['directions']
    cost = result['cost']

    optimal_route = [('a','c') ,('c','d'), ('d','b'), ('b','e'),('e','a')]
    optimal_cost = 34.0

    if cost != optimal_cost or directions != optimal_route:
        valid_b_n_b_result = False

    assert valid_b_n_b_result
