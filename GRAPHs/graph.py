import collections as coll


class Vertex(object):
    def __init__(self, label, outbound=None):
        self.label = label
        assert isinstance(outbound, coll.Iterable)
        self.outbound = outbound or list()

    def __str__(self):
        return 'Vertex ' + str(self.label)

    def __hash__(self):
        return hash(self.label)


class Edge(object):
    def __init__(self, from_vertex, to_vertex, weight=None):
        self.weight = weight
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex

    def __str__(self):
        return "%s -> %s" %(self.from_vertex, self.to_vertex)


class Graph(object):
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices or list()
        self.edges = edges or list()

    def from_file(self, path):
        """
        reads in format:
         3 -- number of vertices
         3 -- number of edges
         0 1 -- edge between 0 and 1
         1 2 -- edge between 1 and 2
         0 2 -- edge between 0 and 2
        """
        vertices = list()
        edges = list()
        with open(path) as f:
            vertex_count = int(f.readline())
            edge_count = int(f.readline())
            for i in xrange(vertex_count):
                vertices.append(Vertex(i))
            for i in xrange(edge_count):
                start, end = [int(i) for i in f.readline().split()]
                start, end = Vertex(start), Vertex(end)
                assert isinstance(end, int)
                edges.append(Edge(start, end))
                vertices[vertices.index(start)].outbound.append()
