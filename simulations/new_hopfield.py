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
perturbation_period = 1200
pert_accu = 0
time = 0

def init_full():
    global time, g, positions

    g = nx.complete_graph(100)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])

def init_erdos():
    global time, g, positions, U
    
    time = 0
    g = nx.erdos_renyi_graph(560, .08)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])

def init_watts():
    global time, g, positions, U
    time = 0

    g = nx.watts_strogatz_graph(56, 2, 0.3)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])

def init_barabasi():
    global time, g, positions, U
    time = 0

    g = nx.barabasi_albert_graph(560, 300)
    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])




def draw():
    pl.cla()
    nx.draw(g, pos = positions,
            node_color = [g.node[i]['s'] for i in g.nodes_iter()],
            with_labels = True, edge_color = 'c',
            width = [g.edge[i][j]['w'] for (i,j) in g.edges_iter()],
            cmap = pl.cm.autumn, vmin = 0, vmax = 1)
    
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 

def randomize_states():
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    


def node_state(i, g):
    m_1 = 0
    for j in g.neighbors(i):
        m_1 += g.edge[i][j]['w'] * -1 * g.node[j]['s']

    m_2 = 0
    for j in g.neighbors(i):
        m_2 += g.edge[i][j]['w'] * 1 * g.node[j]['s']
        
    if m_1 != m_2:
        if m_1 > m_2:
            g.node[i]['s'] = -1
        else:
            g.node[i]['s'] = 1

def local_u(i, g):
    u = 0
    for j in g.neighbors(i):
        u +=  g.edge[i][j]['w'] * g.node[i]['s'] * g.node[j]['s'] 
    return u


def global_u(g):
    U = 0
    for i in g.nodes():
        U += local_u( i, g )
    return U


            
def step():
    global time, g, positions, pert_accu, perturbation_period
    time += 1

    # if pert_accu == perturbation_period:
    #     pert_accu = 0
    #     randomize_states()
    # else:
    #     pert_accu += 1
    

    #m = []

    i = rd.choice(g.nodes())
    
    node_state(i, g)

    time_list.append(time)
    energy_state.append( global_u(g) )
    




def step_sync():
    global time, g, positions, pert_accu, perturbation_period
    time += 1

    # if pert_accu == perturbation_period:
    #     pert_accu = 0
    #     randomize_states()
    # else:
    #     pert_accu += 1
    

    #m = []
    h = g.copy()
    
    for i in g.nodes():
        node_state(i,h)

    g = h.copy()
        
    time_list.append(time)
    energy_state.append( global_u(g) )

    



def no_draw():
    global time
    print time

        
import pycxsimulator
#init()
init_full()
#init_watts()
#init_erdos()
#init_barabasi()
positions = nx.spring_layout(g)
#pycxsimulator.GUI().start(func = [init_erdos, no_draw, step])
pycxsimulator.GUI().start(func = [init_full, no_draw, step_sync])
plt.cla()
plt.plot(time_list, energy_state, 'b-')
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('new_plot.png')
