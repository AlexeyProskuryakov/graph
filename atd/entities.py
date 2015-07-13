from collections import defaultdict
import json

__author__ = 'alesha'


class Vertex:
    def __init__(self, key):
        self.id = key
        self.data = {}

    def get_id(self):
        return self.id

    def get_data(self):
        return self.data

    def __repr__(self):
        return 'Vertex: %s| %s' % (self.id, self.data)


class ColoredMixin(object):
    def __init__(self, color):
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


class ParentedMixin(object):
    def __init__(self, parent=None):
        self.parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, x):
        self._parent = x


class DistancedMixin(object):
    def __init__(self, distance=-1):
        self.distance = distance

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value


class TreeVertex(Vertex, ColoredMixin, ParentedMixin, DistancedMixin):
    def __init__(self, key, parent=None, distance=-1, color='white', graph=None):
        super().__init__(key)
        self.color = color
        self.parent = parent
        self.distance = distance
        self.graph = graph

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, x):
        self._graph = x

    def __repr__(self):
        return "\tTreeVertex: %s {color: %s, parent: %s, distance: %s}" % (
            self.id, self.color, self.parent, self.distance)


class Graph(object):
    def __init__(self, vertex_farm=None):
        self.vertex_list = {}
        self.edge_list = defaultdict(list)
        self.indexes = defaultdict(list)
        self.vertex_farm = vertex_farm or Vertex

    def add_vertex(self, key):
        new_vertex = self.vertex_farm(key)
        self.vertex_list[key] = new_vertex
        return new_vertex

    def add_index(self, i_name, element=None, elements=None):
        if element or elements:
            self.indexes[i_name].extend(elements or [element] if element else [])
        else:
            raise IndexError('give me element or elements')

    def get_vertex(self, vertex_id):
        return self.vertex_list.get(vertex_id)

    def add_edge(self, f, t, cost=0):
        if f not in self.vertex_list:
            self.add_vertex(f)
        if t not in self.vertex_list:
            self.add_vertex(t)

        self.edge_list[f].append({'dest': t, 'cost': cost})

    def get_vertices_names(self):
        return self.vertex_list.keys()

    def get_vertex_weight(self, v_name):
        return len(self.edge_list[v_name])

    def get_vertex_neighbors(self, v_name):
        return list(map(lambda x: self.vertex_list.get(x['dest']),
                        self.edge_list[v_name]))

    def __contains__(self, n):
        return n in self.vertex_list

    def __iter__(self):
        return iter(self.vertex_list.values())

    def __repr__(self):
        return "%s vertices\n%s edges\n..." % (len(self.edge_list), len(self.vertex_list))


class BFS_Graph(Graph):
    index_key = lambda x, y: '%s-%s>' % (x, y)

    class Queue(object):
        def __init__(self):
            self.items = []

        def size(self):
            return len(self.items)

        def enqueue(self, item):
            self.items.insert(0, item)

        def dequeue(self):
            return self.items.pop()

        def __repr__(self):
            return '%s\n(%s)' % (' > '.join(self.items), len(self.items))

    def __init__(self, parent=None):
        super().__init__()

        if parent:
            self.vertex_list = parent.vertex_list
            self.edge_list = parent.edge_list

    def add_vertex(self, key):
        vertex = TreeVertex(key=key)
        self.vertex_list[key] = vertex
        return vertex

    def compile(self, center_point):
        start_vertex = self.get_vertex(center_point)
        self.last_parent = start_vertex

        vertQueue = BFS_Graph.Queue()
        start_vertex.distance = 0
        start_vertex.color = 'gray'
        vertQueue.enqueue(start_vertex)

        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            for nbr in self.get_vertex_neighbors(currentVert.id):
                if ('white' == nbr.color):
                    nbr.color = 'gray'
                    nbr.distance = currentVert.distance + 1
                    nbr.parent = currentVert
                    vertQueue.enqueue(nbr)

            currentVert.color = 'black'
            self.add_index(BFS_Graph.index_key(start_vertex.id, currentVert.distance), currentVert)

        self.compiled = True
        return vertQueue

    def get_path(self, destination_vertex_id):
        dest_v = self.vertex_list.get(destination_vertex_id)
        result = [dest_v]
        dist = dest_v.distance

        while dist > 0:
            dest_v = self.vertex_list.get(dest_v.parent.id)
            result.append(dest_v)
            dist = dest_v.distance

        return list(reversed(result))

    def get_at_dist(self, from_vertex, distance):
        return self.indexes.get(BFS_Graph.index_key(from_vertex, distance), [])


class DFS_Graph(Graph):
    class DFS_Vertex(Vertex, ColoredMixin):
        def __init__(self, key, color):
            super().__init__(key)
            self.color = color

        def __repr__(self):
            return '%s; color: [%s]' % (self.id, self.color)

    def __init__(self, parent=None):
        super().__init__()

        if parent:
            self.vertex_list = parent.vertex_list
            self.edge_list = parent.edge_list

    def add_vertex(self, key):
        if key not in self.vertex_list:
            self.vertex_list[key] = DFS_Graph.DFS_Vertex(key, 'white')
        else:
            print('this vertex already exist! : %s \n%s' % (key, self.vertex_list[key]))

    def _tour(self, n, path, u, limit):
        u.color = 'gray'
        path.append(u)
        if n < limit:
            nbrList = self.get_vertex_neighbors(u.id)
            i = 0
            done = False
            while i < len(nbrList) and not done:
                if nbrList[i].color == 'white':
                    done = self._tour(n + 1, path, nbrList[i], limit)
                i = i + 1
            if not done:  # prepare to backtrack
                path.pop()
                u.color = 'white'
        else:
            done = True

        return done

    def compile(self, start_point_name, clear=False):
        path = []
        if clear:
            for v in self.vertex_list.values():
                v.color = 'white'

        start_point = self.vertex_list.get(start_point_name)
        if start_point:
            self._tour(0, path, start_point, len(self.vertex_list) - 1)
        return path