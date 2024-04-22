# from or_tools.travelling_salesman_problem import optimize_routes
from distance_api.distance_matrix import create_distance_matrix
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

    # def optimize_routes_tsp(self,):
    #     results = optimize_routes(self.distance_matrix, self.depot)
    #     return results

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
