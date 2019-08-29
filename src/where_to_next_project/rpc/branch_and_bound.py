import numpy as np
import pandas as pd
from . import tspmatrix as tsp


class BranchAndBoundTree():
    def __init__(self, matrix, parent = None, excluded_direction = [], included_directions = [], cost = None, no_of_cities = None):
        self.matrix = reduce_matrix(matrix)
        self.parent = parent
        self.directions = included_directions
        self.sorted_directions = None
        self.current_path = None
        self.is_upper_bound = False

        if cost == None:
            self.cost = matrix.cost
        else:
            self.cost = cost

        if no_of_cities == None:
            self.no_of_cities = matrix.get_no_rows()
        else:
            self.no_of_cities = no_of_cities


        if len(self.directions) == self.no_of_cities - 2:
            self.is_upper_bound = True
            zero_pos = np.where(self.matrix == 0)
            for r_i, c_i in zip(zero_pos[0], zero_pos[1]):
                direction = (self.matrix.index[r_i], self.matrix.columns[c_i])
                self.directions.append(direction)
            self.sort_directions()



        self.left_child = None
        self.right_child = None

    def insert_left(self):
        matrix = self.matrix
        data = np.matrix(matrix)
        row_labels = list(matrix.index)
        col_labels = list(matrix.columns)
        depot = matrix.depot
        current_cost = matrix.cost
        no_of_cities = self.no_of_cities
        direction_penalty = get_penalty(matrix)

        direction = direction_penalty[0]
        r_i = direction[0]
        c_i = direction[1]
        r = row_labels.index(r_i)
        c = col_labels.index(c_i)
        data.itemset(r, c, np.inf)
        penalty = direction_penalty[1]
        current_cost += penalty

        new_matrix = tsp.TspMatrix(data, row_labels = row_labels, col_labels = col_labels, cost = current_cost, depot = depot)

        self.left_child = BranchAndBoundTree(new_matrix, parent = self, cost = current_cost, included_directions = self.directions,
        no_of_cities = no_of_cities)

    def insert_right(self):
        matrix = self.matrix
        data = np.matrix(matrix)
        row_labels = list(matrix.index)
        col_labels = list(matrix.columns)
        depot = matrix.depot
        current_cost = matrix.cost
        no_of_cities = self.no_of_cities
        directions = self.directions[:]

        direction_penalty = get_penalty(matrix)
        direction = direction_penalty[0]
        r_i = direction[0]
        c_i = direction[1]
        r = row_labels.index(r_i)
        c = col_labels.index(c_i)

        data = np.delete(data, r, 0)
        data = np.delete(data, c, 1)
        row_labels.pop(r)
        col_labels.pop(c)

        new_matrix = tsp.TspMatrix(data, row_labels = row_labels, col_labels = col_labels, cost = current_cost, depot = depot)
        directions.append(direction)

        if r_i in new_matrix.columns and c_i in new_matrix.index:
            new_matrix.at[c_i, r_i] = np.inf
        else:
            subtour = get_subtour(direction, directions)
            city_to = subtour[0][0]
            city_from = subtour[-1][1]
            new_matrix.at[city_from, city_to] = np.inf

        self.right_child = BranchAndBoundTree(new_matrix, parent = self, included_directions = directions,
        no_of_cities = self.no_of_cities)

    def back_track(self):
        if self.parent != None:
            parent = self.parent.parent
            self.parent = parent
        else:
            return('This is the root node')

    def sort_directions(self):
        self.sorted_directions = []
        depot = self.matrix.depot
        first_direction = self.get_first_direction()
        self.sorted_directions.append(first_direction)
        self.directions.remove(first_direction)
        while self.directions:
            current_direction = self.sorted_directions[-1]
            next_direcetion = get_subsuquent_direction(current_direction, self.directions)
            self.sorted_directions.append(next_direcetion)
            self.directions.remove(next_direcetion)


    def get_first_direction(self):
        depot = self.matrix.depot
        directions = self.directions
        for d in directions:
            if d[0] == depot:
                return d
        return -1

def branch_and_bound(matrix):
    current_node = BranchAndBoundTree(matrix)
    current_best = None
    while True:
        if current_node.is_upper_bound:
            if current_node.parent == None:
                break

            if current_best == None:
                current_best = current_node
            elif current_node.cost < current_best.cost:
                current_best = current_node

            elif current_node.cost > current_node.parent.cost:
                path = current_node.parent.current_path
                if path == 'r':
                    if current_node.parent.left_child == None:
                        current_node.parent.insert_left()
                    if current_node.cost > current_node.parent.left_child.cost:
                        current_node.parent.current_path = 'l'
                        current_node = current_node.parent.left_child
                    else:
                        current_node.back_track()
                elif path == 'l':
                    if current_node.parent.right_child == None:
                        current_node.parent.insert_right()
                    if current_node.cost > current_node.parent.right_child.cost:
                        current_node.parent.current_path = 'r'
                        current_node = current_node.parent.right_child
                    else:
                        current_node.back_track()
            else:
                current_node.back_track()
        else:
            if current_best != None and current_node.cost > current_best.cost:
                current_node = current_best
                current_node.back_track()
                continue


            current_node.insert_right()
            if current_node.right_child.cost > current_node.cost:
                current_node.insert_left()
                if current_node.right_child.cost <= current_node.left_child.cost:
                    current_node.current_path = 'r'
                    current_node = current_node.right_child
                else:
                    current_node.current_path = 'l'
                    current_node = current_node.left_child
            else:
                current_node.current_path = 'r'
                current_node = current_node.right_child

    result = {
        "directions": current_node.sorted_directions,
        "cost": current_node.cost
    }
    return result


def get_row_pen(row, c_i):
    tmp_row = np.matrix(row)
    tmp_row[0, c_i] = np.NaN
    return np.nanmin(tmp_row)

def get_col_pen(col, r_i):
    tmp_col = np.matrix(col)
    tmp_col[0,r_i] = np.NaN
    return np.nanmin(tmp_col)


def get_penalty(matrix):
    penalty_dic = {}
    row_labels = matrix.index
    col_labels = matrix.columns
    zero_pos = np.where(matrix == 0)

    for r_i, c_i in zip(zero_pos[0], zero_pos[1]):
        row = matrix.get_row(r_i)
        col = matrix.get_col(c_i)
        row_penalty = get_row_pen(row, c_i)
        col_penalty = get_col_pen(col, r_i)
        current_penalty = row_penalty + col_penalty
        penalty_dic[(row_labels[r_i], col_labels[c_i])] = current_penalty

    maximum_cost_direction = max(penalty_dic, key=penalty_dic.get)
    return (maximum_cost_direction, penalty_dic[maximum_cost_direction])

def reduce_matrix(matrix):
    matrix.sub_row_min()
    matrix.sub_col_min()

    return matrix

def get_subsuquent_direction(current_direction, directions):
    city_to = current_direction[1]
    for direction in directions:
        city_from = direction[0]
        if city_from == city_to:
            return direction
    return -1

def get_previous_direction(current_direction, directions):
    city_to = current_direction[0]
    for direction in directions:
        city_from = direction[1]
        if city_from == city_to:
            return direction
    return -1

def get_subtour(current_direction, directions):
    subtour = [current_direction]
    while True:
        subsuquent_direction = get_subsuquent_direction(current_direction, directions)
        if subsuquent_direction != -1:
            subtour.append(subsuquent_direction)
            current_direction = subsuquent_direction
        else:
            break

    while True:
        current_direction = subtour[0]
        previous_direction = get_previous_direction(current_direction, directions)
        if previous_direction != -1:
            subtour.insert(0, previous_direction)
        else:
            break

    return subtour
