import matplotlib
matplotlib.use('TkAgg')
# matplotlib.use('GTK')
import matplotlib.pyplot as plt
import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import numpy as np
import math as mt
from pprint import pprint

time_list = []
energy_state = []

C = True
D = False
theta = 1



def plot():
    plt.cla()
    plt.plot(time_list, energy_state, 'bs-')
    plt.xlabel('Time')
    plt.ylabel('Energy states')
#    plt.ylim(-300, 300)
    plt.savefig('fitness_plot.png')


"""Generates a full connected network"""
def init_simple():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.Graph()
    g.add_nodes_from(['a','b','c','d'])

    for i in g.node:
        for j in g.node:
            # trust
            g.add_edge(i,j,w=10)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10
        



def init_watts():
    global time, g, positions, E
    E = 0
    time = 0

    g = nx.watts_strogatz_graph(100, 2, 0.3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)
        

def init_erdos():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.erdos_renyi_graph(100, .3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)

        
def init_barabasi():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.barabasi_albert_graph(200, 15)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)


def draw():
    # pl.cla()
    # nx.draw(g, pos = positions,
    #         node_color = [g.node[i]['s'] for i in g.nodes_iter()],
    #         with_labels = True, edge_color = 'c',
    #         cmap = pl.cm.autumn, vmin = 0, vmax = 1)
    
    # pl.axis('image')
    # pl.title('t = ' + str(time))
    # #pl.title('Energy = ' + str(E))
    # pl.show() 
    global time
    print time


def step_async():
    global time, g, positions, E
    time += 1

    # grab a node
    i = rd.choice(g.nodes())
    

    # set state for node
    m = []    
    for j in g.neighbors(i):
        m.append( g.edge[i][j]['w'] )
        
    tau = sum(m)

    if not g.node[i]['f']:
        g.node[i]['f'] = 0.0000000001

    if not tau:
        tau = 0.0000000001
        
    #d   = tau / g.node[i]['f']
    d   =  g.node[i]['f'] / tau

    
    if d <= theta:
        g.node[i]['s'] = not g.node[i]['s']

        
    # interact
    m_i = []
    m_j = []
    w = []
    for j in g.neighbors(i):
        if g.node[i]['s'] == C and g.node[j]['s'] ==  D:
            g.node[i]['f'] += -2
            g.node[j]['f'] += 2
            g.edge[i][j]['w'] += -1
            
        if g.node[i]['s'] ==  D and g.node[j]['s'] == C:
            g.node[i]['f'] += 2
            g.node[j]['f'] += -2
            g.edge[i][j]['w'] += -1
            
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            g.node[i]['f'] += 1
            g.node[j]['f'] += 1
            g.edge[i][j]['w'] += 2

        if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
            g.node[i]['f'] += -1
            g.node[j]['f'] += -1
            g.edge[i][j]['w'] += -2


    print i, g.node[i],d,tau
    
    # report
    ef = []
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
            ef.append( g.edge[i][j]['w']  )
            E = sum(ef)
    time_list.append(time)
    energy_state.append(E)


    
            
def step_sync_global():
    global time, g,  E
    time += 1

    g_plus = g.copy()

    # do all nodes
    for i in g.nodes():

        # set state for node
        m = []
        for j in g.neighbors(i):
            m.append( g.edge[i][j]['w'] )
        
        tau = sum(m)

        if not g.node[i]['f']:
            g.node[i]['f'] = 0.0000000001

        if not tau:
            tau =  0.0000000001

        #d   = tau / g.node[i]['f']
        d   =  g.node[i]['f'] / tau
        if d <= theta:
            g_plus.node[i]['s'] = not g.node[i]['s']


        # interact
        m_i = []
        m_j = []
        w = []
        for j in g.neighbors(i):
            if g.node[i]['s'] == C and g.node[j]['s'] ==  D:
                g_plus.node[i]['f'] += -2
                g_plus.node[j]['f'] += 2
                g_plus.edge[i][j]['w'] += -1
            
            if g.node[i]['s'] ==  D and g.node[j]['s'] == C:
                g_plus.node[i]['f'] += 2
                g_plus.node[j]['f'] += -2
                g_plus.edge[i][j]['w'] += -1
            
            if g.node[i]['s'] == C and g.node[j]['s'] == C:
                g_plus.node[i]['f'] += 1
                g_plus.node[j]['f'] += 1
                g_plus.edge[i][j]['w'] += 2

            if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
                g_plus.node[i]['f'] += -1
                g_plus.node[j]['f'] += -1
                g_plus.edge[i][j]['w'] += -2


    g = g_plus.copy()

    # report
    ef = []
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
            ef.append( g.edge[i][j]['w']  )
            E = sum(ef)
    time_list.append(time)
    energy_state.append(E)




import pycxsimulator

init_watts()
#init_erdos()
#init_barabasi()
#init_simple()
positions = nx.spring_layout(g)
pycxsimulator.GUI().start(func = [init_watts, draw, step_sync_global])

plot()
