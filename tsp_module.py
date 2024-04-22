# from or_tools.travelling_salesman_problem import optimize_routes
from distance_api.distance_matrix import create_distance_matrix
import itertools

# from constants import api_key
# api_key = "AIzaSyCL7xCEoletemwK_sqTHWDxtlhiCSm11jA"    # version 1

api_key = "AIzaSyCClqphqiwXh6dpBkS6Aau86BNNn4y9v4w" #latest
# api_key = "AIzaSyD3XsmFnWqu-Bxa9Pi49C1avaAvi23ibXo" # Daniyal's

class RoutingOptimizer:
    def __init__(self,addresses = [],depot= 0, api_key = api_key):
        self.addresses = addresses
        self.depot = depot
        self.api_key = api_key
        self.distance_matrix = None

    def add_address(self,address):
        # Enter addresses
        self.addresses.append(address)

    def remove_address(self,address):
        self.addresses.remove(address)

    def create_distance_matrix(self):
        self.distance_matrix = create_distance_matrix(self.addresses, self.api_key)


    # helper function for brute force
    def calculate_distance(self, city1, city2):
    # Assuming city1 and city2 are tuples of (x, y) coordinates
        return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5

    # helper function for brute force
    def total_distance(self, path, distances):
        total = 0
        for i in range(len(path) - 1):
            total += distances[path[i]][path[i+1]]
        total += distances[path[-1]][path[0]]
        return total

    # brute force function - TSP
    def brute_force_tsp(self, distance_matrix):
        num_cities = len(distance_matrix)
        cities = range(num_cities)
        shortest_path = None
        shortest_distance = float('inf')

        for perm in itertools.permutations(cities):
            distance = self.total_distance(perm, distance_matrix)
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = perm

        return shortest_path, shortest_distance


routing = RoutingOptimizer()
# routing.add_address('Berlin+Germany')
routing.add_address('Munich+Germany')
routing.add_address('Hamburg+Germany')
routing.add_address('Saarland+Germany')
# routing.add_address('Delhi+India')


# routing.add_address('Delhi+India')
print(routing.addresses)
routing.create_distance_matrix()
print(routing.distance_matrix)


shortest_path, shortest_distance = routing.brute_force_tsp(routing.distance_matrix)
print("Shortest path:", shortest_path)
print("Shortest distance:", shortest_distance)
print("hey")
