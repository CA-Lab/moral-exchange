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

perturbation_period = 1001
pert_accu = 0
time = 0
T = 0
m = []
T_list = [0, ]
U_plot = [0, ]

def init_full():
    global time, g, o, positions

    g = nx.complete_graph(50) 

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = 0


    # should weights be initialized to 0, 1 or 0.01?
    o = g.copy()
    for i,j in o.edges():
        o.edge[i][j]['w'] = rd.choice([1,0,-1])

def init_erdos():
    global time, g, o, positions, U
    
    time = 0
    g = nx.erdos_renyi_graph(50, .07)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,0,1])

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
    for i in o.nodes():
        state = rd.choice([1,-1])
        o.node[i]['s'] = state

def local_uo(i, o):
    u_o = 0
    for j in o.neighbors(i):
        u_o +=  o.edge[i][j]['w'] * o.node[i]['s'] * o.node[j]['s']
    return u_o


def global_uo(o):
    U = 0
    for i in o.nodes():
        U += local_uo( i, g )
    return U

def node_state():
    i = rd.choice(g.nodes())
    
    m_1 = 0
    for j in o.neighbors(i):
        m_1 += (o.edge[i][j]['w'] + g.edge[i][j]['w']) * -1 * o.node[j]['s']
   

    m_2 = 0
    for j in o.neighbors(i):
        m_2 += (o.edge[i][j]['w'] + g.edge[i][j]['w']) * 1 * o.node[j]['s']


    if m_1 != m_2:
        if m_1 > m_2:
            o.node[i]['s'] = -1
        else:
            o.node[i]['s'] = 1

def step():
    global time, g, o, positions, T
    
    time = 0
    randomize_states(o)
    #steps = 1000
    while time < 1000:
        node_state()
        time += 1

    if time%1000 == 0:
        T += 1
    if T > 100 and T < 300:
        learning()
    else:
        node_state()
        
    T_list.append( T )
    U_plot.append( global_uo(o) )

    time_list.append(time)
    #energy_state_o.append( global_uo(o) )
    #energy_state_g.append( global_ul(g) )
    
def learning():
#def step():
    global time, g, o, positions, pert_accu, perturbation_period
    #time += 1

    # if pert_accu == perturbation_period:
    #     pert_accu = 0
    #     randomize_states(g)
    # else:
    #     pert_accu += 1
    

    #i = rd.choice(g.nodes())

    r = 0.005
    
    # m_1 = 0
    # for j in g.neighbors(i) and o.neighbors(i):
    #     m_1 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] + r) * g.node[i]['s'] * g.node[j]['s']

    for i in o.nodes():
        m_1 = 0
        for j in o.neighbors(i):
            m_1 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] + r) * o.node[i]['s'] * o.node[j]['s']
    

        m_2 = 0
        for j in o.neighbors(i):
            m_2 += (g.edge[i][j]['w'] + o.edge[i][j]['w'] -r) * o.node[i]['s']  * o.node[j]['s']

        
        if m_1 != m_2:
            if m_1 > m_2:
                g.edge[i][j]['w'] += r
            else:
                g.edge[i][j]['w'] -= r


    
    
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
pycxsimulator.GUI().start(func = [init_full, no_draw, step])
#pycxsimulator.GUI().start(func = [init_full, draw, step])
plt.cla()
#plt.plot(time_list, energy_state_g, 'b+')
#plt.plot(time_list, energy_state_o, 'r-')
plt.scatter( T_list, U_plot, c=u'r', marker=u'D' )
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('learning_plot.png')
