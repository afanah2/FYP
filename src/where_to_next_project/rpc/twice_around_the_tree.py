from . import tspmatrix as tsp
import numpy as np

class MinimumSpanningTree:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cities = list(matrix.columns)
        self.visited_cities = []
        self.depot = self.matrix.depot
        self.directions = []
        self.cities.remove(self.depot)
        self.visited_cities.append(self.depot)
        self.tree = {self.depot: []}


        while self.cities:
            vertex, new_neighbour = self.get_closest_vertix()
            self.tree[vertex].append(new_neighbour)
            self.tree[new_neighbour] = []
            self.cities.remove(new_neighbour)
            self.visited_cities.append(new_neighbour)

        self.sort_tree(self.depot)

    def sort_tree(self, v):
        self.directions.append(v)
        for neighbour in self.tree[v]:
            self.sort_tree(neighbour)

    def get_closest_vertix(self):
        closest_v = None
        current_best = np.inf
        for visited_v in self.visited_cities:
            for v in self.cities:
                current_distance = self.matrix[visited_v][v]
                if current_distance < current_best:
                    closest_v = (visited_v, v)
                    current_best = current_distance

        return closest_v

def get_cost(route, matrix):
    cost = 0
    for i in range(len(route) - 1):
        city_from = route[i]
        city_to = route[i+1]

        cost += matrix[city_to][city_from]

    return cost

def route_to_directions(route):
    directions = []
    for i in range(len(route) - 1):
        city_from = route[i]
        city_to = route[i+1]
        directions.append((city_from, city_to))

    return directions

def twice_around_tree(matrix):
    minimum_spanning_tree = MinimumSpanningTree(matrix)
    directions = minimum_spanning_tree.directions
    no_of_cities = len(directions)
    tmp = directions[:-1]
    tmp.reverse()
    directions.extend(tmp)

    depot = directions[0]
    best_route = None
    best_cost = np.inf
    if no_of_cities < 3:
        directions = route_to_directions(directions)
    else:
        for i in range(1, no_of_cities):

            for j in range(i+1, no_of_cities):
                current_route = [depot, directions[i], directions[j]]

                for k in range(j+1, len(directions)):
                    if not (directions[k] in current_route and directions[k] != depot):
                        current_route.append(directions[k])

                current_cost = get_cost(current_route, matrix)

                if current_cost < best_cost:
                    best_route = current_route[:]
                    best_cost = current_cost


        directions = route_to_directions(best_route)
        
    result = {
        "directions": directions,
        "cost": best_cost
    }
    return result
