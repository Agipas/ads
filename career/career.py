import heapq
import string
import random
import time
import os
from pprint import pprint
from collections import OrderedDict


PROGRAM_NAME = 'career'


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
    graph, bottom_vertices = Graph.from_file(path)
    start = graph.vertices[0]
    # primive greedy algo
    distances, path_predecessors = Graph.dijkstra(graph, start)
    last = distances.values()
    if bottom_vertices:
        last = distances.values()[-len(bottom_vertices):]
    return max(last) + start.weight


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
        if _file.endswith(".in"): # or _file.endswith(".in"):
            print 'Reading file %s ....' % _file
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


class NotDirectedAcyclicGraphError(ValueError):
    pass


class Vertex:
    def __init__(self, weight, label=None):
        self.label = label or ''.join([random.choice(string.ascii_uppercase) for _ in xrange(8)])
        self.outbound_edges = []
        self.weight = weight

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
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def __str__(self):
        res = ''
        for el in self.edges:
            res += str(el) + '\n'
        return res

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as input_file:
            # The first two lines define the vertex count and the edge count.
            levels = int(input_file.readline())
            vertices = []
            edges = []
            top = [Vertex(int(input_file.readline()))]
            vertices.extend(top)
            pointer = top
            next_vertices = None
            for level in xrange(levels - 1):
                weights = input_file.readline().split()
                next_vertices = [Vertex(int(k)) for k in weights]
                for index in xrange(len(pointer)):
                    den1 = next_vertices[index]
                    den2 = next_vertices[index + 1]
                    one = Edge(pointer[index], den1, den1.weight)
                    two = Edge(pointer[index], den2, den2.weight)
                    pointer[index].outbound_edges = [one, two]
                    edges.append(one)
                    edges.append(two)
                pointer = next_vertices
                vertices.extend(next_vertices)

        return cls(vertices, edges), next_vertices

    @classmethod
    def dijkstra(cls, graph, start_vertex):
        # Initialization: setting all known shortest distances to infinity,
        # and the start vertex will have the shortest distance to itself equal to 0.
        INFINITY = -float('inf')
        distances = OrderedDict((vertex.label, INFINITY) for vertex in graph.vertices)
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
                if alternative_distance > distances[neighbor_vertex.label]:
                    distances[neighbor_vertex.label] = alternative_distance
                    path_predecessors[neighbor_vertex.label] = shortest_distance_vertex

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

