import matplotlib
#matplotlib.use('GTK')
import matplotlib.pyplot as plt
import pylab as pl
#import scipy as sp
import numpy as np
import argparse
import random as rd
import networkx as nx
from time import sleep
from elixir import *

from pprint import pprint


parser = argparse.ArgumentParser(description='prissoner dilema network simulation')
parser.add_argument('--db_url', default='sqlite:///db.sqlite', help='DB URL, e.g. sqlite:///db.sqlite')
parser.add_argument('--mode', required=True, choices=['init','view','walk'])

args = parser.parse_args()



# database connect
metadata.bind = args.db_url



theta = 1
##############
# Node model #
##############
class Node(Entity):
    fitness = Field(Integer)
    state   = Field(Boolean)
    edges   = ManyToMany('Edge')

    using_options(tablename='nodes')
    
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


##################
# Edge model     #
##################
class Edge(Entity):
    w     = Field(Integer)
    nodes = ManyToMany('Node')

    using_options(tablename='edges')
    
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




def init_watts():
    g = nx.watts_strogatz_graph(20, 2, 0.3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([True, False])
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




def edge_from_edge( edge ):
    node    = rd.choice( edge.nodes )
    n_edges = list( node.edges )
    n_edges.remove( edge )
    if n_edges:
        return rd.choice(n_edges)
    else:
        return False



def random_prissoner_walk():
    e = rd.choice( Edge.query.all() )
        
    while True:
        print "interaction", e
        try:
            e.prissoners_dilema()
        except:
            session.rollback()
            print "rolled back"
        sleep(0.2) # makes ctl-break easier
        e = edge_from_edge( e )
        if not e:
            print "reached the border"
            e = rd.choice( Edge.query.all() )



def view():
    g       = network_from_db()
    old_pos = nx.layout.spring_layout(g, iterations=11)
    
    while True:
        pos = nx.layout.spring_layout(g, pos=old_pos, iterations=11)
        node_sizes  = [g.node[n]['f']*50 for n in g.nodes()]
        node_colors = [g.node[n]['s'] for n in g.nodes()]
        nx.draw(g,
                pos         = pos,
                with_labels = False,
                node_size   = node_sizes,
                node_color  = node_colors,
                alpha       = 1,
                edge_color  = "lightgrey")
        pl.axis('image')
        # plt.show()
        plt.savefig("aguas.png", dpi=150)
        sleep(0.2)
        g = network_from_db()
        old_pos = pos
        pl.cla()


#    pl.title('cited in')
#



if args.mode == 'init':
    create_all()
    g = init_watts()
    network_to_db(g)
elif args.mode == 'walk':
    random_prissoner_walk()
elif args.mode == 'view':
    view()



    # old_pos = nx.graphviz_layout(g, prog='twopi', args='-Goverlap=scale -Gnodesep=70')
    
