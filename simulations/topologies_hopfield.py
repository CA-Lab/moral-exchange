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


def init():
    global time, g, positions, E
    E = 0
    time = 0
    #g = nx.erdos_renyi_graph(100, .3)
    g = nx.watts_strogatz_graph(100, 2, 0.3)
    #g = nx.barabasi_albert_graph(500, 15)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-2,-1,0,1,2])

    

init()

positions = nx.circular_layout(g)

def draw():
    pl.cla()
    nx.draw(g, pos = positions, node_color = [g.node[i]['s'] for i in g.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.YlGn_r, vmin = 0, vmax = 1)
    pl.axis('image')
    pl.title('t = ' + str(time))
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
        if e >= 1:
            g.node[i]['s'] = 1
        else:
            g.node[i]['s'] = -1
    
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
                ef.append( g.edge[i][j]['w']  )
                E = sum(ef)
    
    
    for i in g.node:
        states.append(g.node[i]['s'])
        if len(states) == 22:
            print states
                

    energy_state.append(E)
    time_list.append(time)
    
    # plt.plot(time_list, energy_state, 'bs-')
    # plt.xlabel('Time')
    # plt.ylabel('Energy states')
    # plt.ylim(-120, 200)
    # plt.savefig('plot_1.png')
    # plt.show()



import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])

plt.plot(time_list, energy_state, 'bs-')
plt.xlabel('Time')
plt.ylabel('Energy states')
plt.ylim(-120, 1000)
plt.savefig('plot_1.png')
plt.show()
