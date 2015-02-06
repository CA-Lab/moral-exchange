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
perturbation_period = 164
pert_accu = 0

def init_full():
    global time, g, positions, U
    E = 0
    time = 0
    g = nx.complete_graph(50)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])    

    
def init_watts():
    global time, g, positions, U
    E = 0
    time = 0

    g = nx.watts_strogatz_graph(25, 2, 0.3)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])


def init_erdos():
    global time, g, positions, U
    E = 0
    time = 0
    #"""p is calculated according to Watson et al 2011, p = k/N, in the current configuration k = 2. """
    g = nx.erdos_renyi_graph(25, .08)

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
    #pl.suptitle( 'T =' + str(gt))
    plt.show() 

def local_u(i):
    m = []
    i = rd.choice(g.nodes())

    for j in g.neighbors(i):
        m.append( g.edge[i][j]['w'] * g.node[j]['s'] )
    return sum(m)        

def global_u():
   
    U = []
    for i in g.nodes():
        U.append( local_u( i ) )

    return sum( U )

def randomize_states():
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])

def hebbian():
    global time, g, positions, U

    
    i = rd.choice(g.nodes())

    
    if local_u( i ) >= 0:
        g.node[i]['s'] = 1
    else:
        g.node[i]['s'] = -1

    for j in g.neighbors( i ):
        if g.node[i]['s'] == g.node[j]['s']:
            g.edge[i][j]['w'] += 1
        else:
            g.edge[i][j]['w'] -= 1

def hopfield():

    i = rd.choice(g.nodes())
    
    if local_u(i) >= 0:
        g.node[i]['s'] = 1
    else:
        g.node[i]['s'] = -1
            
def step():
    global time, g, positions, U, pert_accu, perturbation_period
    time += 1
    if pert_accu == perturbation_period:
        pert_accu = 0
        randomize_states()
    else:
        pert_accu += 1
        
    if time <= 460:
        hopfield()
    else:
        hebbian()

    
    time_list.append(time) 
    energy_state.append( global_u() )

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
#pycxsimulator.GUI().start(func = [init_erdos, no_draw, step])
pycxsimulator.GUI().start(func = [init_erdos, draw, step])
plt.cla()
plt.plot(time_list, energy_state, 'b-')
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('demo_plot.png')
#plt.show()
