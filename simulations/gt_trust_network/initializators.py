import networkx as nx
import random as rd

C = True
D = False


"""Generates a simple full connected network"""
def init_simple():
    g = nx.Graph()
    g.add_nodes_from(['a','b','c'])

    # complete graph
    for i in g.node:
        for j in g.node:
            g.add_edge(i,j,w=10)
            

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g

def init_real():
    #imports real network data
    g = nx.read_edgelist('weightless_testing_case.csv')

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)


def init_full():
    # complete graph
    g =  nx.complete_graph(20)

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g

def init_erdos():
    g = nx.erdos_renyi_graph(100, .3)

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g
        

def init_erdos_directed():
    # directed erdos renyi
    g =  nx.erdos_renyi_graph( 100, .3, directed = True )

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g


def init_watts():
    g = nx.watts_strogatz_graph(500, 8, 0.1)

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g

def init_directed_watts():
    h = nx.watts_strogatz_graph(500, 8, 0.1)
    g = h.to_directed()

    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)

    return g
    

def init_barabasi():
    g = nx.barabasi_albert_graph(1200, 15)
    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)
    return g

def init_di_scale_free():
    g = nx.scale_free_graph(50)
    g = reset_states(g)
    g = reset_fitness(g)
    g = reset_trust(g)
    return g


def reset_fitness(g, fitness=10):
    for i in g.nodes():
        g.node[i]['f'] = fitness
    return g


def reset_states(g):
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([C,D])
    return g


def reset_trust(g, trust=10):
    for e in g.edges():
        g.add_edge(*e, w=trust)
    return g
