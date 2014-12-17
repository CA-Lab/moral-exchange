from __future__ import division
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
import operator
from networkx.readwrite import json_graph
from pprint import pprint

time_list = []
time_list2 = []
energy_state = []
fitness_state = []
global_cc = []
global_apl = []


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
    ax1 = fig.add_subplot(411)
    ax1.plot(time_list, energy_state, 'b-')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Global trust states')

    ax2 = fig.add_subplot(412)
    ax2.plot(time_list2, fitness_state, 'r-')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Global fitness states')

    ax3 = fig.add_subplot(413)
    ax3.plot(time_list2, global_cc, 'r-')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Global CC')

    ax4 = fig.add_subplot(414)
    ax4.plot(time_list2, global_apl, 'r-')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Global APL')

    plt.savefig('rewire_fitness.png')


def report():
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

    global_cc.append(nx.average_clustering(g))
    try:
        global_apl.append(nx.average_shortest_path_length(g))
    except:
        print "no apl"
        global_apl.append(0)
    
"""Generates a full connected network"""
def init_simple():
    global time, g, positions, E, F
    E = 0
    F = 0
    time = 0
    g = nx.Graph()
    g.add_nodes_from(['a','b','c','d','e'])

    g.add_edges_from([('a','b'),('b','c'),('c','a'),('d','e'),('c','d'),('e','c')])

    for i, j in g.edges():
        g.edge[i][j]['w'] = rd.choice([0,1,2,3,4])
    
    # for i in g.node:
    #     for j in g.node:
    #         # trust
    #         g.add_edge(i,j,w=10)

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

    g = nx.watts_strogatz_graph(50, 2, 0.3)

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
    g = nx.erdos_renyi_graph(20, .3)

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
    pl.cla()
    nodeSize=[g.node[n]['f']**2 for n in nx.nodes(g)]
    nx.draw(g, pos = positions,
            node_color = [g.node[i]['s'] for i in g.nodes_iter()],
            with_labels = True, edge_color = 'c',
            cmap = pl.cm.autumn, vmin = 0, vmax = 1,
            node_size=nodeSize, alpha=0.75)
    
    pl.axis('image')
    pl.title('t = ' + str(time))
    #pl.title('Energy = ' + str(E))
    pl.show() 
    global time
    print time

def not_draw():
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
        
    d   = tau / g.node[i]['f']
    #d   =  g.node[i]['f'] / tau
    
    if d <= theta:
        g.node[i]['s'] = not g.node[i]['s']
    
    # interact
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


    # rewire!
    rewire_async(i)

    # report for later plotting
    report()



            
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


        try:
            # interact
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
        except KeyError:
            print i,j
            for n in g_plus.nodes():
                print n, g.node[n], g.get_edge_data(i,j)



    # rewire
    for i in g_plus.nodes():
        weights = {}
        for j in g_plus.neighbors(i):
            weights[j] = g_plus.get_edge_data(i, j)['w']

        if weights:
            sorted_w = sorted(weights.items(), key=operator.itemgetter(1))
            weakest = sorted_w.pop(0)
            if weakest[1] < 1:
                g_plus.remove_edge(i, weakest[0])
    
                # 
                other_nodes = g_plus.nodes()
                other_nodes.remove(i) # no self loop
                total_fitness = sum([g_plus.node[n]['f'] for n in other_nodes]) + 0.0000000001
                proportional_f_per_node = {}
                acc = 0
                for n in other_nodes:
                    proportional_f_per_node[n] = (acc, acc + (g_plus.node[n]['f'] / total_fitness))
                    acc = proportional_f_per_node[n][1]

                # flip a coin
                r = rd.random()
                for n in proportional_f_per_node:
                    if r >= proportional_f_per_node[n][0] and r <= proportional_f_per_node[n][1]:
                        if not g_plus.get_edge_data(i, n):
                            g_plus.add_edge(i, n, w=10)


                
    g = g_plus.copy()
    
    # report for later plotting
    report()


                
                
def rewire_async(node):
    # find weakest link, remove it
    weights = {}
    for j in g.neighbors(node):
        weights[j] = g.get_edge_data(node, j)['w']

    if weights:
        sorted_w = sorted(weights.items(), key=operator.itemgetter(1))
        weakest = sorted_w.pop(0)
        if weakest[1] < 1:
            g.remove_edge(node, weakest[0])

            # find trustable node to wire
            other_nodes = g.nodes()
            other_nodes.remove(node) # no self loop
            total_fitness = sum([g.node[n]['f'] for n in other_nodes])
            proportional_f_per_node = {}
            acc = 0
            for n in other_nodes:
                proportional_f_per_node[n] = (acc, acc + (g.node[n]['f'] / total_fitness))
                acc = proportional_f_per_node[n][1]

            # flip a coin
            r = rd.random()
            for n in proportional_f_per_node:
                if r >= proportional_f_per_node[n][0] and r <= proportional_f_per_node[n][1]:
                    if not g.get_edge_data(node, n):
                        g.add_edge(node, n, w=10)

    
import pycxsimulator

#init_watts()
init_erdos()
#init_barabasi()
#init_simple()
positions = nx.spring_layout(g)
pycxsimulator.GUI().start(func = [init_erdos, draw, step_async])
#pycxsimulator.GUI().start(func = [init_barabasi, not_draw, step_sync_global])


plot()
