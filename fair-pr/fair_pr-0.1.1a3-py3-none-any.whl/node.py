""" Node represantation of a directed graph
"""


class Node():
    def __init__(self, id):
        self.__in_neighbors = set()
        self.__out_neighbors = set()
    
    def add_in_nieghbor(self, node_id):
        self.__in_neighbors.add(node_id)
    
    def add_out_nieghbor(self, node_id):
        self.__out_neighbors.add(node_id)

    @property
    def in_neighbors(self):
        return self.__in_neighbors

    @property
    def out_neighbors(self):
        return self.__out_neighbors

    @property
    def in_degree(self):
        return len(self.__in_neighbors)

    @property
    def out_degree(self):
        return len(self.__out_neighbors)
