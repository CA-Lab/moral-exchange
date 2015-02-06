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

#"""perturbation period based on Watson et al, 2011. t = 3/4eN ln N
perturbation_period = 460
pert_accu = 0
ritual_agents = 10

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
    #"""For Watts-Strogatz topology 10 ritual agents seems to work fine in order to optimize U"""
    g = nx.watts_strogatz_graph(56, 3, 0.2)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['w'] = rd.choice([-1,1])


def init_erdos():
    global time, g, positions, U
    E = 0
    time = 0
    g = nx.erdos_renyi_graph(56, .1)

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
        #print sum( U )
    return sum(U)

def randomize_states(nodes=None):
    if not nodes:
        for i in g.nodes():
            g.node[i]['s'] = rd.choice([1,-1])
    else:
        for i in nodes:
            g.node[i]['s'] = rd.choice([1,-1])

def extra_wiring():
    for i in g.nodes():
        for j in g.nodes():
            if not g.get_edge_data(i,j):
                g.add_edge(i,j,w = 1, ritual=True)

def remove_extra_wiring():
    for e in g.edges():
        if 'ritual' in g.get_edge_data(*e):
            g.remove_edge(*e)
                
def ritual():
    global time, g, positions, U, pert_accu, perturbation_period, ritual_agents

    extra_wiring()
    agents = rd.sample(g.nodes(), ritual_agents)
    randomize_states(agents)    
    for n in agents:
        time += 1
        hebbian(n)
        time_list.append(time)
        energy_state.append( global_u() )
        
    remove_extra_wiring()
    randomize_states(agents)

    
def hebbian(i):
    global time, g, positions, U

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
    global time, g, positions, U, pert_accu, perturbation_period, rigual_agents
    time += 1

    if pert_accu == perturbation_period:
        pert_accu = ritual_agents
        ritual()
    else:
        pert_accu += 1

    i = rd.choice(g.nodes())
    
    # if time <= 25:
    #     hopfield()
    # else:
    hebbian(i)
    
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
pycxsimulator.GUI().start(func = [init_erdos, no_draw, step])
#pycxsimulator.GUI().start(func = [init_watts, draw, step])
plt.cla()
plt.plot(time_list, energy_state, 'b-')
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('hebb_plot.png')
#plt.show()
