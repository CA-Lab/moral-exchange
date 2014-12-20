#import matplotlib
# matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
#import pylab as pl
import random as rd
#import scipy as sp
import networkx as nx
#import numpy as np
#import math as mt
from pprint import pprint

from elixir import *

metadata.bind = "sqlite:///db.sqlite"
metadata.bind.echo = False

C = True
D = False
theta = 1


class Node(Entity):
    fitness = Field(Integer)
    state   = Field(Boolean)
    edges   = ManyToMany('Edge')

    
    def neighbors(self):
        nodes = set()
        for e in self.edges:
            for n in e.nodes:
                nodes.add(n)
        nodes.remove(self)
        return nodes

    
    # will I be True or False?
    def update_state(self):
        m = []    
        for e in self.edges:
            m.append( e.w )
        
        tau = sum(m)
        
        if not tau:
            tau = 0.0000000001
        
        d =  self.fitness / tau

        if d <= theta:
            self.state = not self.state

    
    def __repr__(self):
        return '<Node [%s] f=%i s=%s>' % (self.id, self.fitness, self.state)


    
class Edge(Entity):
    w     = Field(Integer)
    nodes = ManyToMany('Node')

    
    def prissoners_dilema( self ):    
        # interaction of nodes
        if self.nodes[0].state == True  and self.nodes[1].state ==  False:
            self.nodes[0].fitness += -2
            self.nodes[1].fitness += 2
            self.w += -1
                
        if self.nodes[0].state == False and self.nodes[1].state == True:
            self.nodes[0].fitness += 2
            self.nodes[1].fitness += -2
            self.w += -1
                
        if self.nodes[0].state == True  and self.nodes[1].state == True:
            self.nodes[0].fitness += 1
            self.nodes[1].fitness += 1
            self.w += 2
    
        if self.nodes[0].state == False and self.nodes[1].state ==  False:
            self.nodes[0].fitness += -1
            self.nodes[1].fitness += -1
            self.w += -2

        self.nodes[0].update_state()
        self.nodes[1].update_state()
        session.commit()

        
    def __repr__(self):
        return '<Edge %s, %s>' % (self.nodes, self.w)


setup_all()
create_all()





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





def network_to_db(g):
    for n in g.nodes():
        node = Node(id      = n,
                    fitness = g.node[n]['f'],
                    state   = g.node[n]['s'])
        session.commit()
        
    for e in g.edges():
        u = Node.get(e[0])
        v = Node.get(e[1])
        edge = Edge( w     = g.get_edge_data(*e)['w'],
                     nodes = [u, v] )
        
        session.commit()





def network_from_db():
    g = nx.Graph()
    # load nodes
    for n in Node.query.all():
        g.add_node(n.id, { 'f': n.fitness,
                           's': n.state })
    # load edges
    for e in Edge.query.all():
        g.add_edge(e.nodes[0].id,
                   e.nodes[1].id,
                   {'w': e.w })

    return g





def random_prissoner_walk():
    e = rd.choice( Edge.query.all() )
        
    while True:
        print "interaction among ", e
        e.prissoners_dilema()
        e = edge_from_edge( e )
        if not e:
            e = rd.choice( Edge.query.all() )
    

def edge_from_edge( edge ):
    node    = rd.choice( edge.nodes )
    n_edges = list( node.edges )
    n_edges.remove( edge )
    if n_edges:
        return rd.choice(n_edges)
    else:
        return False
    


    

#g = init_watts()
#network_to_db(g)
#h = network_from_db()

random_prissoner_walk()
