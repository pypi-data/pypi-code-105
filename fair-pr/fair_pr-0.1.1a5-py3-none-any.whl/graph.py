""" File contains all the graph structures.

TODO: Check alternative structs to use to escalate for big data.

Options:
    - Check compatibility with networkx library https://networkx.org/
    - Sparse matrix representation?
    - How to implement adjecency list?
"""


class _Node():
    def __init__(self):
        self.__in_neighbors = set()
        self.__out_neighbors = set()
        self.__attribute = ""  # TODO: Generalise for more than one attributes.

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

    @property
    def attribute(self):
        return self.__attribute

    @attribute.setter
    def attribute(self, attribute_value):
        self.__attribute = attribute_value

    def add_in_neighbor(self, node: int):
        self.__in_neighbors.add(node)

    def add_out_neighbor(self, node: int):
        self.__out_neighbors.add(node)


class Graph():
    """ The main graph class.

    Currently we represent the graph with a form of adjacency list
    implemented with a dictionary.

    The networks in the fair PageRank project are graphs with
    attributes on their nodes. In the simplest occasion this attribute
    is binary and represents a sensitive characteristic of an individual.
    """
    def __init__(self, edge_file: str, attributes_file: str):
        """
        Args:
            edge_file:
            attributes_file:
        
        Example:
        """

        # TODO: Add discription of dictionary.
        self.__graph = dict()

        # Read Edge file. 
        edges = open(edge_file).readlines()

        # Init dict for nodes.
        for edge in edges:
            s, t = edge.split()
            s, t = int(s), int(t)

            if s not in self.__graph:
                self.__graph[s] = _Node()
            
            if t not in self.__graph:
                self.__graph[t] = _Node()
        
            self.add_out_neighbor(to_node=s, neighbor=t)
            self.add_in_neighbor(to_node=t, neighbor=s)

    @property
    def nodes(self):
        """ Returns the nodes of the graph.
        i.e. the keys of our dict, our graph representation structure.
        """
        return self.__graph.keys()

    def out_neighbors(self, node: int):
        return self.__graph[node].out_neighbors

    def in_neighbors(self, node: int):
        return self.__graph[node].in_neighbors

    def out_degree(self, node: int):
        return self.__graph[node].out_degree

    def in_degree(self, node: int):
        return self.__graph[node].in_degree

    def add_in_neighbor(self, to_node: int, neighbor: int):
        self.__graph[to_node].add_in_neighbor(neighbor)

    def add_out_neighbor(self, to_node: int, neighbor: int):
        self.__graph[to_node].add_out_neighbor(neighbor)
