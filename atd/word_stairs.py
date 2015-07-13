__author__ = 'alesha'
from collections import defaultdict
from atd.entities import Graph, TreeVertex




def build_graph(word_file, max_length=4, min_length=4):
    d = defaultdict(list)
    g = Graph()
    with open(word_file) as f:
        for line in f:
            word = line[:].lower().strip()
            if (len(word) > max_length) or (len(word) < min_length):
                continue
            for i in range(len(word)):
                bucket = word[:i] + '_' + word[i + 1:]
                d[bucket].append(word)

    for bucket, words in d.items():
        for word in words:
            for word2 in words:
                if word2 != word:
                    g.add_edge(word, word2, vertexClass=TreeVertex)

    return g
