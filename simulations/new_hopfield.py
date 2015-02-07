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
m = []

def init_full():
    global time, g, positions

    g = nx.complete_graph(56) 

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
    

def step():
    global time, g, positions, pert_accu, perturbation_period, m
    time += 1

    if pert_accu == perturbation_period:
        pert_accu = 0
        randomize_states()
    else:
        pert_accu += 1
    
    u = 0
    #m = []
    U = 0
    
    i = rd.choice(g.nodes())
    
    m_1 = []
        
    for j in g.neighbors(i):
        m_1.append(g.edge[i][j]['w'] * -1 * g.node[j]['s'])
    M_1 = sum(m_1)
    #print M_1

    m_2 = []
        
    for j in g.neighbors(i):
        m_2.append(g.edge[i][j]['w'] * 1 * g.node[j]['s'])
    M_2 = sum(m_2)
    #print M_2
        
    if M_1 != M_2:
        if M_1 > M_2:
            g.node[i]['s'] = -1
        else:
            g.node[i]['s'] = 1

    for j in g.neighbors(i):
        u +=  g.edge[i][j]['w'] * g.node[i]['s'] * g.node[j]['s'] 
        m.append(u)
    U = sum(m)


            
    time_list.append(time)
    energy_state.append( U )




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
pycxsimulator.GUI().start(func = [init_erdos, no_draw, step])
#pycxsimulator.GUI().start(func = [init_full, draw, step])
plt.cla()
plt.plot(time_list, energy_state, 'b-')
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('new_plot.png')
