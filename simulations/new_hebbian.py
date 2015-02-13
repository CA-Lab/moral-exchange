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

energy_state_g = []
energy_state_o = []

T_list = [0, ]
T = 0
U_plot = [0, ]

perturbation_period = 1001
pert_accu = 0
time = 0
m = []

def init_full():
    global time, g, o, positions

    g = nx.complete_graph(100) 

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,0,1])


    #should weights be initialized to 0, 1 or 0.01?
    o = g.copy()
    # for i,j in o.edges():
    #     o.edge[i][j]['w'] = 0
    
def init_erdos():
    global time, g, o, positions, U
    
    time = 0
    g = nx.erdos_renyi_graph(120, .06)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,0,1])

    o = g.copy()
    # for i,j in o.edges():
    #     o.edge[i][j]['w'] = 0
    
def init_watts():
    global time, g, o, positions, U
    time = 0

    g = nx.watts_strogatz_graph(56, 2, 0.3)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])

    o = g.copy()
    for i,j in h.edges():
        h.edge[i][j]['w'] = 0
        
def init_barabasi():
    global time, g, o, positions, U
    time = 0

    g = nx.barabasi_albert_graph(560, 300)
    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])

    o = g.copy()
    for i,j in o.edges():
        o.edge[i][j]['w'] = 0
        
def draw():
    pl.cla()
    nx.draw(g, pos = positions,
            node_color = [g.node[i]['s'] for i in g.nodes_iter()],
            with_labels = True, edge_color = 'c',
            #width = [g.edge[i][j]['w'] for (i,j) in g.edges_iter()],
            cmap = pl.cm.autumn, vmin = 0, vmax = 1)
    
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 

def randomize_states( g ):
    for i in g.nodes():
        state = rd.choice([1,-1])
        g.node[i]['s'] = state
        o.node[i]['s'] = state

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
            o.node[i]['s'] = -1
        else:
            g.node[i]['s'] = 1
            o.node[i]['s'] = 1

def local_uo(i, o):
    u_o = 0
    for j in o.neighbors(i):
        u_o +=  o.edge[i][j]['w'] * o.node[i]['s'] * o.node[j]['s']
    return u_o

# def local_ul(i, g):
#     u_l = 0
#     for j in g.neighbors(i):
#         u_l += g.edge[i][j]['w'] * g.node[i]['s'] * g.node[j]['s']
#     return u_l


def global_uo(o):
    global pert_accu, perturbation_period
    U = 0
    U_plot = []
    for i in o.nodes():
        U += local_uo( i, g )
    return U

# def global_ul(g):
#     U_l = 0
#     for i in g.nodes():
#         U_l += local_ul( i, g )


def step():
    global time, g, o, positions, pert_accu, perturbation_period, T
    time += 1

    if pert_accu == perturbation_period:
        pert_accu = 0
        randomize_states(g)
    else:
        pert_accu += 1
    

    i = rd.choice(g.nodes())

    r = 0.005
    
    m_1 = 0
    for j in g.neighbors(i) and o.neighbors(i):
        m_1 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] + r) * g.node[i]['s'] * g.node[j]['s']


    m_2 = 0
    for j in g.neighbors(i) and o.neighbors(i):
        m_2 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] -r) * g.node[i]['s']  * g.node[j]['s']

        
    if m_1 != m_2:
        if m_1 > m_2:
            g.edge[i][j]['w'] += r
        else:
            g.edge[i][j]['w'] -= r

    
    node_state( i, g )


    time_list.append(time)
    energy_state_o.append( global_uo(o) )
    #energy_state_g.append( global_ul(g) )
    
    if time%1000 == 0:
        T += 1
        T_list.append( T )
        U_plot.append( global_uo(o) )




def step_sync():
    global time, g, o, positions, pert_accu, perturbation_period, T
    time += 1

    if pert_accu == perturbation_period:
        pert_accu = 0
        randomize_states( g )
    else:
        pert_accu += 1

        
    i = rd.choice(g.nodes())

    r = 0.005
    
    m_1 = 0
    for j in g.neighbors(i) and o.neighbors(i):
        m_1 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] + r) * g.node[i]['s'] * g.node[j]['s']


    m_2 = 0
    for j in g.neighbors(i) and o.neighbors(i):
        m_2 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] -r) * g.node[i]['s']  * g.node[j]['s']

        
    if m_1 != m_2:
        if m_1 > m_2:
            g.edge[i][j]['w'] += r
        else:
            g.edge[i][j]['w'] -= r

    
    #node_state( i, g )
    

    #m = []
    h = g.copy()
    p = o.copy()
    
    for i in g.nodes() and o.nodes():
        node_state(i,h)

    g = h.copy()
    o = p.copy()

    time_list.append(time)
 #   energy_state_o.append( global_uo(o) )
#     #energy_state_g.append( global_ul(g) )
    
    if time%1000 == 0:
        T += 1
        T_list.append( T )
        U_plot.append( global_uo(o) )


def no_draw():
    global time
    print time

        
import pycxsimulator
#init()
#init_full()
#init_watts()
init_erdos()
#init_barabasi()
positions = nx.spring_layout(g)
pycxsimulator.GUI().start(func = [init_erdos, no_draw, step_sync])
#pycxsimulator.GUI().start(func = [init_full, draw, step])
plt.cla()
#plt.plot(time_list, energy_state_g, 'b+')
#plt.plot(time_list, energy_state_o, 'r-')
plt.scatter( T_list, U_plot, c=u'r', marker=u'D' )
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('new_hebbian_plot.png')
