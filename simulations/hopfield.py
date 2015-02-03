# python hopfield.py --csv ../Data/cols-cols_w_edgelist.csv
# python hopfield.py -h da la sinopsis

import matplotlib
#matplotlib.use('TkAgg')
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
import random as rd
import networkx as nx
import argparse
import csv
import sys
from progressbar import ProgressBar



time_list = []
energy_state = []


parser = argparse.ArgumentParser(description='Hopfield network simulation.')
parser.add_argument('--csv', type=argparse.FileType('r'), help='Edge list in CSV format')
parser.add_argument('--iterations', type=int, default=10000, help='how many iterations')
args = parser.parse_args()

pbar = ProgressBar(maxval=args.iterations)


def init_from_csv():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.read_weighted_edgelist(args.csv, delimiter=",")

    initbar = ProgressBar(len(g.nodes()))
    print "setting random states"
    n = 0
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
        n+=1
        initbar.update(n)
    initbar.finish()



    
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
        #g.edge[i][j]['weight'] = rd.choice([-2,-1,0,1,2])

    # for i in g.edge:
    #     for j in g.edge:
    #         g.edge[i][j]['weight'] = rd.choice([-2,-1,0,1,2])

    """for proof testing """
    g.edge['a']['b']['weight'] = -2
    g.edge['a']['c']['weight'] = -1
    g.edge['a']['d']['weight'] = 0
    g.edge['a']['a']['weight'] = 0

    g.edge['b']['a']['weight'] = -2
    g.edge['b']['c']['weight'] = 1
    g.edge['b']['d']['weight'] = 2
    g.edge['b']['b']['weight'] = 2
    
    g.edge['c']['a']['weight'] = -1
    g.edge['c']['b']['weight'] = 1
    g.edge['c']['d']['weight'] = 0
    g.edge['c']['c']['weight'] = 0

    g.edge['d']['a']['weight'] = 0
    g.edge['d']['b']['weight'] = 2
    g.edge['d']['c']['weight'] = 0
    g.edge['d']['d']['weight'] = 0
    
def init_watts():
    global time, g, positions, E
    E = 0
    time = 0

    g = nx.watts_strogatz_graph(100, 2, 0.3)

    
    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['weight'] = rd.choice([-2,-1,0,1,2])


def init_erdos():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.erdos_renyi_graph(100, .3)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['weight'] = rd.choice([-2,-1,0,1,2])

def init_barabasi():
    global time, g, positions, E
    E = 0
    time = 0
    g = nx.barabasi_albert_graph(200, 15)

    for i in g.nodes():
        g.node[i]['s'] = rd.choice([1,-1])
    
    for i,j in g.edges():
        g.edge[i][j]['weight'] = rd.choice([-2,-1,0,1,2])




def step():
    global time, g, positions, E

    time += 1
    states = []
    m = []
    """ef for energy function"""
    ef = []

    i = rd.choice(g.nodes())
    for j in g.neighbors(i):
        m.append( g.edge[i][j]['weight'] * g.node[j]['s'] )
        
    e = sum(m)

    if e >= 1:
        g.node[i]['s'] = 1
    else:
        g.node[i]['s'] = -1
        
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
            ef.append( g.edge[i][j]['weight']  )
            E = sum(ef)

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
            m.append( g.edge[i][j]['weight'] * g.node[j]['s'] )

        e = sum(m)
        # print i, e

        if e >= 1:
            g_plus.node[i]['s'] = 1
        else:
            g_plus.node[i]['s'] = -1


    g = g_plus.copy()
                    
    for i, j in g.edges():
        if g.node[i]['s'] == 1 and g.node[j]['s'] == 1:
            ef.append( g.edge[i][j]['weight']  )
            E = sum(ef)

    
    for i in g.node:
        states.append(g.node[i]['s'])
        if len(states) == 4:
            print states
                


    time_list.append(time)
    energy_state.append(E)





#init_watts()
#init_erdos()
#init_barabasi()


init_from_csv()
print "running simulation"
for time in range(0,args.iterations):
    step()
    pbar.update(time)    
pbar.finish()



plt.cla()
plt.plot(time_list, energy_state, 'bs-')
plt.xlabel('Time')
plt.ylabel('Energy states')

plt.savefig('e_plot.svg')


