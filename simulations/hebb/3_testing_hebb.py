import matplotlib
#matplotlib.use('TkAgg')
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import numpy as np
import math as mt
import pprint as ppt

file_num = 0

time_list = []

energy_state_g = []
energy_state_o = []

perturbation_period = 1000
pert_accu = 0
time = 0
T = 0
m = []
T_list = [0, ]
U_plot = [0, ]
g = nx.complete_graph(120)
o = nx.complete_graph(120)
#GU = open('gu_%d.txt' %file_num, 'w')

def init_full():
    global g, o, file_num
    
    #file_num += 1
    #print file_num

    randomize_states(g)
    
    for i,j in g.edges():
        g.edge[i][j]['weight'] = 0

    o = g.copy()
    for i,j in o.edges():
        if rd.random() < 0.07:
            o.edge[i][j]['weight'] = rd.choice([1,-1])
            

    nx.write_weighted_edgelist(g, 'g_edgelist_%d.csv' %file_num)
    nx.write_weighted_edgelist(o, 'o_edgelist_%d.csv' %file_num)


def init_erdos():
    global g, o
    
    g = nx.erdos_renyi_graph(120, 1)

    randomize_states(g)

    for i,j in g.edges():
        g.edge[i][j]['weight'] = 0
        
    o = g.copy()
    for i,j in o.edges():
        if rd.random() < 0.07:
            o.edge[i][j]['weight'] = rd.choice([-1,1])

def init_small_world():
    
    g = nx.watts_strogatz_graph(120, 8, 0.5)

    randomize_states(g)

    for i,j in g.edges():
        g.edge[i][j]['weight'] = 0
        
    o = g.copy()
    for i,j in o.edges():
        if rd.random() < 0.07:
            o.edge[i][j]['weight'] = rd.choice([-1,1])
        
def draw():
    pl.cla()
    nx.draw(g, pos = positions,
            node_color = [g.node[i]['s'] for i in g.nodes_iter()],
            with_labels = True, edge_color = 'c',
            #width = [g.edge[i][j]['weight'] for (i,j) in g.edges_iter()],
            cmap = pl.cm.autumn, vmin = 0, vmax = 1)
    
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 

def randomize_states( o ):
    for i in o.nodes():
        o.node[i]['s'] = rd.choice([1,-1])
        

def local_uo(i, o):
    u_o = 0
    for j in o.neighbors(i):
        u_o +=  o.edge[i][j]['weight'] * o.node[i]['s'] * o.node[j]['s']
    return u_o


def global_uo(o):
    U = 0
    for i in o.nodes():
        U += local_uo( i, o )
    return U

def node_state(i):
    global g, o
    
    m_1 = 0
    for j in o.neighbors(i):
        m_1 += (o.edge[i][j]['weight'] + g.edge[i][j]['weight']) * -1 * o.node[j]['s']
   

    m_2 = 0
    for j in o.neighbors(i):
        m_2 += (o.edge[i][j]['weight'] + g.edge[i][j]['weight']) * 1 * o.node[j]['s']


    if m_1 > m_2:
        o.node[i]['s'] = -1
    else:
        o.node[i]['s'] = 1

def step():
    global time, o, g, T, perturbation_period, pert_accu, file_num
    
    time +=1
    
    if pert_accu == perturbation_period:
        if T > 600 and T < 3000:
            learning()
        pert_accu = 0
        T += 1
        T_list.append( T )
        U_plot.append( global_uo(o) )
        randomize_states(o)
    else:
        pert_accu += 1
    
    i = rd.choice(o.nodes())


    node_state(i)


    #if time == 3599998:
    #if time == 3599:
    #nx.write_weighted_edgelist(g, 'g_edgelist_end_%d.csv' %file_num)
    #nx.write_weighted_edgelist(o, 'o_edgelist_end_%d.csv' %file_num) 

def learning():
    global  g, o

    r = 0.005
    
    for i in o.nodes():
        m_1 = 0
        for j in o.neighbors(i):
            m_1 += (g.edge[i][j]['weight'] + o.edge[i][j]['weight'] + r) * o.node[i]['s'] * o.node[j]['s']
    

        m_2 = 0
        for j in o.neighbors(i):
            m_2 += (g.edge[i][j]['weight'] + o.edge[i][j]['weight'] -r) * o.node[i]['s']  * o.node[j]['s']

        

        if m_1 > m_2:
            g.edge[i][j]['weight'] += r
        else:
            g.edge[i][j]['weight'] -= r




    
def no_draw():
    global time, file_num
    print time
    

def data():
    global time, o, g, file_num

    if time%3600000 == 0:
        nx.write_weighted_edgelist(g, 'g_edgelist_end_%d.csv' %file_num)
        nx.write_weighted_edgelist(o, 'o_edgelist_end_%d.csv' %file_num)
        GU = open('gu_%d.txt' %file_num, 'w')
        gu = global_uo(o)
        GU.write(str(gu))
        GU.close()

for n in xrange(2):
    file_num += 1
    print file_num
    init_full()
    for n in xrange(perturbation_period * 3600):
        data()
        no_draw()
        step()


plt.cla()
#plt.plot(time_list, energy_state_g, 'b+')
#plt.plot(time_list, energy_state_o, 'r-')
plt.scatter( T_list, U_plot, c=u'r', marker=u'D' )
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('learning_plot_full.svg')
#plt.savefig('learning_plot_small.svg')
#plt.savefig('learning_plot_erdos.svg')
