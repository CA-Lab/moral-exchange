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
    edges   = ManyToMany('Edge')         # <-- and this one
    def __repr__(self):
        return '<Node [%s] f=%i s=%s>' % (self.id, self.fitness, self.state)

class Edge(Entity):
    w     = Field(Integer)
    nodes = ManyToMany('Node')
    
    def __repr__(self):
        return '<Edge "%s">' % self.id


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
        


g = init_watts()



#session.commit()
#Movie.query.all()
#d = Director.get_by(name=u'Ridley Scott')
#q = Movie.query.filter_by(director=d)
