import networkx as nx
import random as rd

C = True
D = False


"""Generates a full connected network"""
def init_simple():
    g = nx.Graph()
    g.add_nodes_from(['a','b','c'])

    # complete graph
    for i in g.node:
        for j in g.node:
            g.add_edge(i,j,w=10)
            
    g = set_nodes_and_edges(g)        
    return g


def init_watts():
    g = nx.watts_strogatz_graph(500, 8, 0.1)
    g = set_nodes_and_edges(g)
    return g


def init_erdos():
    g = nx.erdos_renyi_graph(100, .3)
    g = set_nodes_and_edges(g)
    return g
        
def init_barabasi():
    g = nx.barabasi_albert_graph(200, 15)
    g = set_nodes_and_edges(g)
    return g



def set_nodes_and_edges(g, fitness=10, trust=10):
    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = fitness

    for e in g.edges():
        g.add_edge(*e, w=trust)

    return g


def reset_fitness(g, fitness=10, trust=10):
    for i in g.nodes():
        g.node[i]['f'] = fitness
    return g


def reset_states(g, fitness=10, trust=10):
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([C,D])
    return g


def reset_trust(g, fitness=10, trust=10):
    for e in g.edges():
        g.add_edge(*e, w=trust)
    return g
