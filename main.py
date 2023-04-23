import numpy as np
from pyvis.network import Network
import copy


class Graph():
    def __init__(self, n, random=False):
        self.n = n
        if random:
            self.random_matrix()
        else:
            self.m = np.zeros((self.n, self.n), int)

    def random_matrix(self):
        self.m = np.triu(np.random.randint(0, 2, (self.n, self.n)), 1)
        self.m += self.m.transpose()

    def __check_input_nodes(self, node1: int, node2: int):
        if node1 == node2:
            raise ValueError("Nodes must be different")
        if node1 > self.n - 1 or node2 > self.n - 1:
            raise ValueError("Node indexes must be within a graph range")

    def add_edge(self, node1: int, node2: int):
        "Adds an edge between two nodes (index starts from 0)"
        self.__check_input_nodes(node1, node2)

        self.m[node1][node2] = 1
        self.m[node2][node1] = 1

    def del_edge(self, node1: int, node2: int):
        "Deletes an edge between two nodes (index starts from 0)"
        self.__check_input_nodes(node1, node2)

        self.m[node1][node2] = 0
        self.m[node2][node1] = 0

    def has_edge(self, node1: int, node2: int):
        "Returns `True` when an edge exists"
        self.__check_input_nodes(node1, node2)

        if self.m[node1][node2] == 1:
            return True
        else:
            return False

    def print_matrix(self):
        print(self.m)

    def show_graph(self, walk=[]):
        net = Network(height=950)
        net.set_options("""const options = {
        "edges": {
            "width": 2
        },
        "physics": {
            "forceAtlas2Based": {
            "gravitationalConstant": -129,
            "springLength": 225
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
        }
        }""")

        for i in range(self.n):
            net.add_node(i, label=str(i+1))

        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.m[i][j] != 0:
                    net.add_edge(i, j)

        for i in range(len(walk)-1):
            net.add_edge(walk[i], walk[i+1], color='red')

        net.show("graph.html", notebook=False)

    def copy(self):
        return copy.copy(self)


def input_graph(n):
    e = int(input("Enter number of edges: "))
    graph = Graph(n)

    print("Enter the nodes the edge is between (two nodes each line)")
    for i in range(e):
        u, v = map(int, input().split())
        while (u == v):
            print("Nodes must be different. Enter again.")
            u, v = map(int, input().split())
        while (u > n or v > n):
            print("Node indexes must be within a graph range. Enter again.")
            u, v = map(int, input().split())
        while (graph.has_edge(u-1, v-1)):
            print("This edge is already entered. Continue with the other edges.")
            u, v = map(int, input().split())

        graph.add_edge(u-1, v-1)
    return graph


def find_walk(input_graph: Graph, start: int, end: int):
    "Finds a walk between two nodes using Tarry's Algorithm. Indices start from 0"
    graph = input_graph.copy()
    walk = []
    pos = [0 for _ in range(0, graph.n)]
    curr_node = start

    while curr_node != end:
        has_incidence = False
        for i in range(pos[curr_node], graph.n):
            if curr_node != i and graph.has_edge(curr_node, i):
                walk.append(curr_node)
                pos[curr_node] = i
                graph.del_edge(curr_node, i)
                curr_node = i
                has_incidence = True
                break
        if not has_incidence:
            if len(walk) == 0:
                print("Unable to find a walk")
                return []
            curr_node = walk.pop()
    walk.append(curr_node)
    return walk


if __name__ == '__main__':
    n = int(input("Enter number of nodes: "))
    graph = None

    if (input("Manual or random graph? [m/r] ") == 'm'):
        graph = input_graph(n)
    else:
        graph = Graph(n, random=True)

    graph.print_matrix()
    graph.show_graph()

    print("Enter start and end nodes: ")
    start, end = map(int, input().split())
    while (start == end):
        print("Nodes must be different. Enter again.")
        start, end = map(int, input().split())
    while (start > n or end > n):
        print("Node indexes must be within a graph range. Enter again.")
        start, end = map(int, input().split())

    walk = find_walk(graph, start-1, end-1)
    graph.show_graph(walk)
    walk = list(map(lambda x: x+1, walk))
    print("Walk: ", walk)
