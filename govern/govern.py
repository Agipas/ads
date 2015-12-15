import os
import time
from GRAPHs.graphs.topological_sorting.python import tarjan

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
            start_v, end_v = tarjan.Vertex(start), tarjan.Vertex(end)
            edge = tarjan.Edge(start_v, end_v)
            edges.append(edge)
            if start not in vertices:
                vertices[start] = start_v
            vertices[start].outbound_edges.append(edge)

            if end not in vertices:
                vertices[end] = end_v

    vertices = vertices.values()
    return tarjan.Graph(vertices, edges)


@timeit
def compute(path):
    graph = read_values(path)
    result = tarjan.get_topological_order(graph)
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


if __name__ == '__main__':
    main()
