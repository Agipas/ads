import heapq
import time
import os
from pprint import pprint


PROGRAM_NAME = 'gamsrv'


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r  %2.3f seconds' % (method.__name__.upper(), te - ts)
        return result

    return timed


def write_result(path, result):
    with open(path, 'w') as f:
        if isinstance(result, list):
            for el in result:
                f.write(str(el) + '\n')
        else:
            f.write(str(result))


def compute(path):
    graph = Graph.from_file(path)
    max_dist = float('inf')
    client_labels = [v.label for v in graph.vertices if v.label in graph.client_set]
    for server in [v for v in graph.vertices if v.label not in graph.client_set]:
        distances, path_predecessors = Graph.dijkstra(graph, server)
        client_distances = [distances[k] for k in distances if k in client_labels]
        dis = max(client_distances)
        if dis < max_dist:
            max_dist = dis
    return max_dist


def main():
    try:
        res = compute(PROGRAM_NAME + '.in')
        write_result(PROGRAM_NAME + '.out', res)
        print "Got production file"
        return
    except (IOError, OSError):
        pass
    path = "../problems/" + PROGRAM_NAME + '/testcases/'
    for _file in os.listdir(path):
        if _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


class NotDirectedAcyclicGraphError(ValueError):
    pass


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return "Label: %s  " % self.label

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def __add__(self, other):
        return self.label + other.label


class Edge:
    def __init__(self, start_vertex, end_vertex, weight=None):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    def __str__(self):
        return "%s -> %s" % (self.start_vertex.label, self.end_vertex.label)

    def __hash__(self):
        return hash(self.start_vertex + self.end_vertex)


class Graph:
    def __init__(self, vertices, edges, clients):
        self.vertices = vertices
        self.edges = edges
        self.clients = clients
        self.client_set = set(clients)

    def __str__(self):
        res = ''
        for el in self.edges:
            res += str(el) + '\n'
        return res

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as input_file:
            # The first two lines define the vertex count and the edge count.
            vertex_count, edge_count = input_file.readline().split()
            vertex_count, edge_count = int(vertex_count), int(edge_count)
            clients = input_file.readline().split()
            clients = [int(c) for c in clients]

            vertices = [Vertex(index) for index in range(1, vertex_count + 1)]
            edges = []

            # The next 'edge_count' lines describe the edges: "start_vertex end_vertex weight".
            for i in xrange(edge_count):
                start_vertex, end_vertex, weight = [int(param) for param in input_file.readline().split()]

                # Adding the edge to the list of outbound edges for the start vertex.
                edge = Edge(vertices[start_vertex - 1], vertices[end_vertex - 1], weight)
                vertices[start_vertex - 1].outbound_edges.append(edge)

                # For non-directed graphs, an outbound edge is also an inbound one (0 -> 1 == 1 -> 0).
                # Therefore, we reverse the edge and add it to the other vertex.
                reverse_edge = Edge(vertices[end_vertex - 1], vertices[start_vertex - 1], weight)
                vertices[end_vertex - 1].outbound_edges.append(reverse_edge)

                edges.append(edge)
                edges.append(reverse_edge)

        return cls(vertices, edges, clients)

    @classmethod
    def dijkstra(cls, graph, start_vertex):
        # Initialization: setting all known shortest distances to infinity,
        # and the start vertex will have the shortest distance to itself equal to 0.
        INFINITY = float('inf')
        distances = {vertex.label: INFINITY for vertex in graph.vertices}
        distances[start_vertex.label] = 0

        path_predecessors = {start_vertex.label: None}

        # The heap will allow us to quickly pick an unvisited vertex with the least known distance.
        # The implementation of heapq requires us to store (key, value) tuples, so we'll store (distance, vertex) tuples.
        heap = []
        heapq.heappush(heap, (0, start_vertex))

        while len(heap) > 0:
            # Picking the vertex with the smallest known distance so far.
            distance, shortest_distance_vertex = heapq.heappop(heap)

            # For each adjacent vertex v, check if the path from the current vertex would be more efficient
            # than the one we've known before. I.e., if distance[current] + weight(current->v) < distance[v].
            for edge in shortest_distance_vertex.outbound_edges:
                neighbor_vertex = edge.end_vertex
                alternative_distance = distances[shortest_distance_vertex.label] + edge.weight

                # If we have indeed found a better path, remembering the new distance and predecessor.
                if alternative_distance < distances[neighbor_vertex.label]:
                    distances[neighbor_vertex.label] = alternative_distance
                    path_predecessors[neighbor_vertex.label] = shortest_distance_vertex.label

                    # Pushing the new distance to the heap.
                    heapq.heappush(heap, (alternative_distance, neighbor_vertex))

        return distances, path_predecessors

    @classmethod
    def reconstruct_shortest_path(cls, predecessors, start_vertex, end_vertex):
        path = [end_vertex]
        predecessor = predecessors[end_vertex]

        while predecessor is not None:
            path.insert(0, predecessor)
            predecessor = predecessors[predecessor]

        return path


if __name__ == '__main__':
    main()
