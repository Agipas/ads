__author__ = 'vwvolodya'

import random
import time
from pprint import pprint
import os
from collections import deque


PROGRAM_NAME = 'wchain'


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
    # data = Graph.from_file(path)
    # res = data.compute_for_all()
    data = from_file(path)
    res = 0
    for word in data.itervalues():
        if word.real and not word.visited:
            max_depth = Node.search_max_depth(word)
            if max_depth > res:
                res = max_depth
    return res


class Vertex:
    def __init__(self, label, real=False):
        self.label = label
        self.outbound_edges = deque([])
        self.max_depth = 0
        self.real = real
        self.visited = False

    def get_sub_strings(self):
        string = self.label
        if len(string) <= 1:
            return set()
        char_list = list(string)
        result = list()
        for i, _ in enumerate(char_list):
            tmp = char_list[:]
            del tmp[i]
            result.append("".join(tmp))

        r = [''.join([s for i, s in enumerate(string) if i!=j]) for j in range(len(string))]

        return set(result)

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


class Graph:
    def __init__(self, vertices, edges, vertices_dict):
        self.vertices = vertices
        self.edges = edges
        self.vertices_dict = vertices_dict

    def __str__(self):
        res = ''
        for el in self.edges:
            res += str(el) + '\n'
        return res

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as input_file:

            vertices = deque(list())
            edges = deque(list())
            vertices_dict = dict()

            num_strings = int(input_file.readline())
            for i in xrange(num_strings):
                next_string = input_file.readline().strip()
                vertex = vertices_dict.get(next_string, Vertex(next_string, real=True))
                vertex.real = True
                labels = vertex.get_sub_strings()
                children = deque(list())
                edges_to_children = deque(list())
                if labels:
                    for label in labels:
                        v = vertices_dict.get(label, Vertex(label))
                        children.append(v)
                        vertices_dict[v.label] = v
                        edges_to_children.append(Edge(vertex, v))
                vertex.outbound_edges.extend(edges_to_children)

                vertices_dict[next_string] = vertex
                vertices.append(vertex)
                vertices.extend(children)

        return cls(vertices, edges, vertices_dict)

    def bfs(self, start_vertex):
        result = []

        # Initially, the queue contains only the start vertex
        # and all vertices are assumed to be not visited yet.

        max_depth = 1

        queue = deque([(start_vertex, max_depth)])

        while len(queue) > 0:
            # Remove a vertex from the queue.
            current_vertex, max_depth = queue.popleft()

            # If we've already been here, ignoring this vertex completely.
            # This condition can happen when, for example, this vertex was a neighbor of
            # two other vertices and they both added it to the queue before it was visited.

            # Otherwise, marking it as visited so that we won't analyze it anymore.

            # Getting all adjacent vertices which haven't been visited yet.
            # It's only a matter of traversing the outbound_edges list and getting end_vertex for each.
            neighbors = [(edge.end_vertex, max_depth + 1)
                         for edge in current_vertex.outbound_edges
                         if edge.end_vertex.real]

            # If we need to enforce a particular ordering on the neighbors we visit,
            # e.g., visit them in the order of increasing labels (1, 4, 6; not 4, 6, 1),
            # this would be the place to do the sorting.

            # Adding these neighbors to the queue, all at once.
            for neighbor, _ in neighbors:
                neighbor.visited = True
            queue.extend(neighbors)

        return max_depth

    def compute_for_all(self):
        m = 0
        for v in self.vertices:
            if v.real and not v.visited:
                max_depth = self.bfs(v)
                if max_depth > m:
                    m = max_depth
        return m


class Node(object):
    def __init__(self, label, real=False):
        self.label = label
        self.real = real
        self.children = None
        self.visited = False

    @classmethod
    def search_max_depth(cls, node):
        max_depth = 1
        queue = deque([(node, max_depth)])
        while len(queue) > 0:
            cur_node, max_depth = queue.popleft()
            children = [(ch, max_depth + 1) for ch in cur_node.children if ch.real]
            queue.extend(children)
            for child, _ in children:
                child.visited = True
        return max_depth


def from_file(path):
    with open(path, "r") as input_file:

        words = dict()  # {'label': node}

        num_strings = int(input_file.readline())

        for i in xrange(num_strings):
            next_string = input_file.readline().strip()
            node = words.get(next_string, Node(next_string, real=True))
            node.real = True

            words[node.label] = node
            children = deque(list())
            # get all sub_strings
            string = node.label
            labels = dict()
            if len(string) > 1:
                for i in xrange(len(string)):
                    substr = string[:i] + string[i+1:]
                    labels[substr] = None
                labels = labels.keys()
            #
            # In fact this solution is slower than the one above
            # labels = set()
            # if len(string) > 1:
            #     labels = {string[:i] + string[i+1:] for i in xrange(len(string))}

            if labels:
                for label in labels:
                    n = words.get(label, Node(label))
                    words[n.label] = n
                    children.append(n)
            node.children = children

    return words


def get_sstr(string):
    labels = set()
    if len(string) <= 1:
        return labels
    for i in range(len(string)):
        tmp = string[:i] + string[i+1:]
        labels.add(tmp)
    return labels


def get_sub_strings(string):
    if len(string) <= 1:
        return set()
    char_list = list(string)
    result = list()
    for i, _ in enumerate(char_list):
        tmp = char_list[:]
        del tmp[i]
        result.append("".join(tmp))
    return set(result)


def main():
    try:
        res = compute(PROGRAM_NAME + '.in')
        write_result(PROGRAM_NAME + '.out', res)
        pprint("Got production file")
        return
    except (IOError, OSError):
        pass
    path = "../problems/" + PROGRAM_NAME + '/testcases/'
    for _file in os.listdir(path):
        if _file.endswith(".in") or _file.endswith(".txt"):
            pprint('Reading file %s ....' % _file)
            input_path = os.path.abspath(os.path.join(path, _file))
            res = compute(input_path)
            pprint(res)


if __name__ == '__main__':
    main()
    # print( get_sstr('hello'))
    # print( get_sub_strings('hello'))
    # print( get_sstr('asdfgh'))
    # print( get_sub_strings('asdfgh'))
    # print( get_sstr('aaa'))
    # print( get_sub_strings('aaa'))
    # print( get_sstr('hsofghseouitgoseirtgsg'))
    # print( get_sub_strings('hsofghseouitgoseirtgsg'))

