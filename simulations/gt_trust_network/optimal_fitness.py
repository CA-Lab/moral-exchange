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
time_list2 = []
energy_state = []
fitness_state = []

C = True
D = False
theta = 1

# def plot():
#     plt.cla()
#     plt.plot(time_list, energy_state, 'bs-')
#     plt.plot(time_list, fitness_state, 'r--')
#     plt.xlabel('Time')
#     plt.ylabel('Energy states')
#     plt.savefig('test.png')


def plot():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(time_list, energy_state, 'bs-')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Global trust states')

    ax2 = fig.add_subplot(212)
    ax2.plot(time_list2, fitness_state, 'ro-')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Global fitness states')

    plt.savefig('opt_fitness.png')

"""Generates a full connected network"""
def init_simple():
    global time, g, positions, E, F
    E = 0
    F = 0
    time = 0
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
        



def init_watts():
    global time, g, positions, E, F
    E = 0
    F = 0
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
    global time, g, positions, E, F
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

        
def init_barabasi():
    global time, g, positions, E, F
    E = 0
    F = 0
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
    # nodeSize=[g.degree(n)**2 for n in nx.nodes(g)]
    # nx.draw(g, pos = positions,
    #         node_color = [g.node[i]['s'] for i in g.nodes_iter()],
    #         with_labels = True, edge_color = 'c',
    #         cmap = pl.cm.autumn, vmin = 0, vmax = 1,
    #tnode_size=nodeSize, alpha=0.75)
    
    # pl.axis('image')
    # pl.title('t = ' + str(time))
    # #pl.title('Energy = ' + str(E))
    # pl.show() 
    global time
    print time


def step_async():
    global time, g, positions, E, F
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
            
        # if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
        #     g.node[i]['f'] += 0
        #     g.node[j]['f'] += 0
        #     g.edge[i][j]['w'] += -2


    print time
    
    # report global Trust
    ef = []
    for i, j in g.edges():
        #if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            ef.append( g.edge[i][j]['w']  )
        E = sum(ef)
    time_list.append(time)
    energy_state.append(E)

    #report global fitness
    fitness_i = []
    for i in g.nodes():
        fitness_i.append( g.node[i]['f'] )
        F = sum(fitness_i)
    time_list2.append(time)
    fitness_state.append(F)
        
    
            
def step_sync_global():
    global time, g,  E, F
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

            # if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
            #     g.node[i]['f'] += 0
            #     g.node[j]['f'] += 0
            #     g.edge[i][j]['w'] += -2

    g = g_plus.copy()

    # report Viendo la literatura F (fitness global) y Tau (Trust global) deben ser promedios, es decir F = sum(f_i)/n, en donde n es el numero de nodos en la red. Lo mismo para Trust global.
    ef = []
    for i, j in g.edges():
        #if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            ef.append( g.edge[i][j]['w']  )
        E = sum(ef)
    time_list.append(time)
    energy_state.append(E)

    # report global fitness
    fitness_i = []
    for i in g.nodes():
        fitness_i.append( g.node[i]['f'] )
        F = sum(fitness_i)
    time_list2.append(time)
    fitness_state.append(F)


import pycxsimulator

init_watts()
#init_erdos()
#init_barabasi()
#init_simple()
positions = nx.spring_layout(g)
#pycxsimulator.GUI().start(func = [init_watts, draw, step_async])
pycxsimulator.GUI().start(func = [init_watts, draw, step_sync_global])


plot()
