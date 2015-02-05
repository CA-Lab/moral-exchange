import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import numpy as np
import math as mt
import pprint as ppt

time_list = []
energy_state = []

"""Generates a full connected network"""
def init():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.Graph()
    g.add_nodes_from(['a','b','c','d'])

    for i in g.node:
        for j in g.node:
            g.add_edge(i,j)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])

    #for i, j in g.edges():
        #g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])

    # for i in g.edge:
    #     for j in g.edge:
    #         g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])

    """for proof testing """
    g.edge['a']['b']['w'] = -2
    g.edge['a']['c']['w'] = -1
    g.edge['a']['d']['w'] = 0
    g.edge['a']['a']['w'] = 0

    g.edge['b']['a']['w'] = -2
    g.edge['b']['c']['w'] = 1
    g.edge['b']['d']['w'] = 2
    g.edge['b']['b']['w'] = 2
    
    g.edge['c']['a']['w'] = -1
    g.edge['c']['b']['w'] = 1
    g.edge['c']['d']['w'] = 0
    g.edge['c']['c']['w'] = 0

    g.edge['d']['a']['w'] = 0
    g.edge['d']['b']['w'] = 2
    g.edge['d']['c']['w'] = 0
    g.edge['d']['d']['w'] = 0

def init_full():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.complete_graph(25)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])    

    
def init_watts():
    global time, g, positions, E
    E = 0
    time = 0

    g = nx.watts_strogatz_graph(25, 2, 0.3)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])


def init_erdos():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.erdos_renyi_graph(25, .3)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])

def init_barabasi():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.barabasi_albert_graph(200, 15)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])



def draw():
    pl.cla()
    nx.draw(g, pos = positions,
            node_color = [g.node[i]['s'] for i in g.nodes_iter()],
            with_labels = True, edge_color = 'c',
            cmap = pl.cm.autumn, vmin = 0, vmax = 1)
    
    pl.axis('image')
    pl.title('t = ' + str(time))
    #pl.title('Energy = ' + str(E))
    plt.show() 


def step():
    global time, g, positions, E

    time += 1
    states = []
    m = []
    """ef for energy function"""
    ef = []

    i = rd.choice(g.nodes())
    for j in g.neighbors(i):
        m.append( g.edge[i][j]['w'] * g.node[j]['s'] )
        
    e = sum(m)
    print i, e
    if e >= 1:
        g.node[i]['s'] = 1
    else:
        g.node[i]['s'] = -1
                
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:

            ef.append( g.edge[i][j]['w']  )
            E = sum(ef)

    
    # for i in g.node:
    #     states.append(g.node[i]['s'])
    #     if len(states) == 4:
    #         print states
                


    time_list.append(time)
    energy_state.append(E)



def step_sync_global():
    global time, g, positions, E

    time += 1
    states = []
    m = []
    """ef for energy function"""
    ef = []

    g_plus = g.copy()
    
    for i in g.nodes():
        for j in g.neighbors(i):
            m.append( g.edge[i][j]['w'] * g.node[j]['s'] )

        e = sum(m)
        # print i, e

        if e >= 1:
            g_plus.node[i]['s'] = 1
        else:
            g_plus.node[i]['s'] = -1


    g = g_plus.copy()
                    
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
            ef.append( g.edge[i][j]['w']  )
            E = sum(ef)

    
    for i in g.node:
        states.append(g.node[i]['s'])
        if len(states) == 4:
            print states
                


    time_list.append(time)
    energy_state.append(E)




import pycxsimulator

#init()
init_full()
#init_watts()
#init_erdos()
#init_barabasi()
positions = nx.spring_layout(g)
pycxsimulator.GUI().start(func = [init_full, draw, step])
plt.cla()
plt.plot(time_list, energy_state, 'bs-')
plt.xlabel('Time')
plt.ylabel('Energy states')
#plt.ylim(-100, 100)
#plt.yticks(range(-10, 13, 2))
plt.savefig('e_plot.png')
#plt.show()

