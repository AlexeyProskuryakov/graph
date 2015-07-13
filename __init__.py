import requests
import json
import logging

__author__ = 'alesha'

gephi_master_url = 'http://localhost:8080/workspace0?operation=updateGraph'


class GephiStreamer(object):
    def __init__(self):
        self.log = logging.getLogger().getChild('gephi_streamer')
        self.nodes = {}
        self.edges = {}

    def __send(self, data):
        to_send = json.dumps(data)
        try:
            requests.post(gephi_master_url, data=to_send)
        except IOError as e:
            self.log.error('can not connect to gephi')


    def add_relation(self, from_node_id, to_node_id, relation_type):
        """
        sending to gephi master graph streamer two nodes and one edge
        :param from_node: {identifier:{'label':..., 'weight':...}}
        :param to_node: {identifier:{'label':..., 'weight':...}}
        :return:
        """
        if from_node_id not in self.nodes:
            self.__send({'an': {from_node_id: {'label': from_node_id, 'not_loaded': True}}})
            self.nodes[from_node_id] = None
        if to_node_id not in self.nodes:
            self.__send({'an': {to_node_id: {'label': to_node_id, 'not_loaded': True}}})
            self.nodes[to_node_id] = None

        edge_id = "%s_%s" % (from_node_id, to_node_id)
        saved = self.edges.get(edge_id)
        if saved is None:
            self.edges[edge_id] = 1
            self.__send(
                {'ae': {
                    edge_id: {'source': from_node_id,
                              'target': to_node_id,
                              'directed': True,
                              'weight': self.edges[edge_id],
                              'label': relation_type
                              }
                }})
        else:
            saved += 1
            self.edges[edge_id] = saved
            self.__send({'ce': {edge_id: {'weight': saved}}})


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


def bfs(graph, start_vertex_name):
    start_vertex = graph.get_vertex(start_vertex_name)

    vertQueue = Queue()
    vertQueue.enqueue(start_vertex)

    while (vertQueue.size() > 0):
        currentVert = vertQueue.dequeue()
        for nbr in graph.get_vertex_neighbors(start_vertex.id):
            if ('white' == nbr.color):
                nbr.color = 'gray'
                nbr.distance = currentVert.distance + 1
                nbr.parent = currentVert
                vertQueue.enqueue(nbr)
        currentVert.color = 'black'
        graph.add_index('%s-%s>' % (start_vertex_name, currentVert.distance), currentVert)

    return vertQueue


def visualise_at_gephi(graph):
    gstreamer = GephiStreamer()

    for f, t in graph.edge_list.items():
        for t_ in t:
            gstreamer.add_relation(f, t_['dest'], t_['cost'])



if __name__ == '__main__':
    from    sys import argv
    from atd.word_stairs import build_graph

    from atd.knight import knightGraph

    # pickle_file_name = 'resources/graph.pickle'
    #
    # resource_fname = argv[2] if len(argv) > 2 else 'resources/words.txt'
    # g = build_graph(resource_fname)

    g = knightGraph(8)
    print('graph created...')

    # queue = bfs(g, 'fool')
    # print(queue)
    print(g)
    visualise_at_gephi(g)
