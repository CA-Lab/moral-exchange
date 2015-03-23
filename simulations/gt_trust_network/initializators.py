import networkx as nx
import random as rd

C = True
D = False


"""Generates a full connected network"""
def init_simple():
    g = nx.Graph()
    g.add_nodes_from(['a','b','c'])

    for i in g.node:
        for j in g.node:
            # trust
            g.add_edge(i,j,w=10)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10
        
    return g


def init_watts():
    g = nx.watts_strogatz_graph(100, 2, 0.3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)

    return g
        

def init_erdos():
    E = 0
    F = 0
    time = 0
    g = nx.erdos_renyi_graph(100, .3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)

    return g
        
def init_barabasi():

    g = nx.barabasi_albert_graph(200, 15)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)

    return g
