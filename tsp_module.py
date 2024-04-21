from distance_api.distance_matrix import create_distance_matrix
from constants import api_key
# api_key = "1"

class RoutingOptimizer:
    def __init__(self,addresses = [],depot= 0, api_key = api_key):
        self.addresses = addresses
        self.depot = depot
        self.api_key = api_key
        self.distance_matrix = None

    def add_address(self,address):
        self.addresses.append(address)

    def remove_address(self,address):
        self.addresses.remove(address)

    def create_distance_matrix(self):
            self.distance_matrix = create_distance_matrix(self.addresses, self.api_key)

    # def optimize_routes_tsp(self,):
    #     results = optimize_routes(self.distance_matrix, self.depot)
    #     return results

routing = RoutingOptimizer()
routing.add_address('Munich+Germany')
routing.add_address('Dresden+Germany')
routing.add_address('Saarland+Germany')
routing.add_address('Sluttgart+Germany')
routing.addresses
routing.create_distance_matrix()

print("hey")