import os
import time
from collections import deque

PROGRAM_NAME = 'govern'


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

@timeit
def read_values(path):
    # {'label': vertex, }
    vertices = dict()
    edges = []
    with open(path) as f:
        while True:
            next_line = f.readline().strip()
            if not next_line:
                break
            start, end = next_line.split()
            start_v, end_v = Vertex(start), Vertex(end)
            edge = Edge(start_v, end_v)
            edges.append(edge)
            if start not in vertices:
                vertices[start] = start_v
            vertices[start].outbound_edges.append(edge)

            if end not in vertices:
                vertices[end] = end_v

    vertices = vertices.values()
    return Graph(vertices, edges)


def compute(path):
    graph = read_values(path)
    result = get_topological_order(graph)
    return result


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
        if _file.endswith(".txt"):
            print 'Reading file %s ....' % _file
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            print 'Result: ', res
            # write_result('out.txt', res)


def get_topological_order(graph):
    return tarjan_dfs(graph, use_recursion=False)


def tarjan_dfs(graph, use_recursion=True):
    # Instead of keeping a boolean visited[] array, our visits will have 3 states.
    NOT_VISITED = 0
    VISITED = 1
    VISITED_AND_RESOLVED = 2

    topological_order = []
    topological_order_set = set()

    unvisited_vertices = set(graph.vertices)
    visited_status = {vertex.label: NOT_VISITED for vertex in graph.vertices}

    # An alternative stack-based implementation of DFS.
    # Particularly useful for Python due to its recursion limit.
    while len(unvisited_vertices) > 0:
        start_vertex = unvisited_vertices.pop()
        stack = deque([start_vertex])

        while len(stack) > 0:
            vertex = stack.pop()

            visited_status[vertex.label] = VISITED
            if vertex in unvisited_vertices:
                unvisited_vertices.remove(vertex)

            unvisited_neighbors = []
            edges = [edge.end_vertex for edge in vertex.outbound_edges]
            for neighbor in edges:
                # We came across an unresolved dependency. It means there's a cycle in the graph.
                if visited_status[neighbor.label] == VISITED:
                    raise NotDirectedAcyclicGraphError
                # Getting all unexplored dependencies of the current vertex.
                if visited_status[neighbor.label] == NOT_VISITED:
                    unvisited_neighbors.append(neighbor)

            # If there are no more dependencies to explore, it means we've satisfied all of them
            # and we can add this vertex to the result of topological ordering.
            if len(unvisited_neighbors) == 0:
                visited_status[vertex.label] = VISITED_AND_RESOLVED
                # Avoid duplicates in the output.
                if vertex not in topological_order_set:
                    topological_order.append(vertex)
                    topological_order_set.add(vertex)
            else:
                # If there's something left to explore,
                # leaving the vertex in the stack along with all its neighbors.
                stack.append(vertex)
                stack.extend(unvisited_neighbors)

    return topological_order


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
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex

    def __str__(self):
        return "%s -> %s" % (self.start_vertex.label, self.end_vertex.label)

    def __hash__(self):
        return hash(self.start_vertex + self.end_vertex)


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


if __name__ == '__main__':
    main()
