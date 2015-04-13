import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
#import operator
import argparse
import random as rd
import networkx as nx

from pprint import pprint

parser = argparse.ArgumentParser(description='Prissoner\'s dilema with trust network simulation.')
parser.add_argument('--runid', default="" )
parser.add_argument('--iterations', type=int, default=500 )
parser.add_argument('--plot',   type=argparse.FileType('w'), help="path to plot", default=open('aguas.png', 'w') )
#parser.add_argument('--game', default="prissoner", choices=['snow'] )
#parser.add_argument('--step', default="async", choices=['async', 'sync'] )

args = parser.parse_args()


# log keeping variables
time = 0
time_list = []
energy_state = []
fitness_state = []
state_changes = []



C = True
D = False

g = nx.watts_strogatz_graph(500, 8, 0.1)

def set_nodes(g, fitness=10 ):
    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = fitness

    return g


def global_fitness( ):
    fitness = []
    for i in g.nodes():
        fitness.append( g.node[i]['f'] )
    F = float(sum(fitness))

    return F


def node_strategy_selection(node):
    global g

    neighbors_C = []
    neighbors_D = []

    for i in g.nodes():
        for j in g.neighbors(i):
            if g.node[j]['s'] == C:
                neighbors_C.append( g.node[j]['s'] )
            else:
                neighbors_D.append( g.node[j]['s'] )
    
    if len( neighbors_C ) > len( neighbors_D ):
        return g.node[node]['s'] == C
    else:
        return g.node[node]['s'] == D


def step_sync():
    global time, g
    time += 1
    print time
    g_plus = g.copy()

    # do all nodes
    for i in g.nodes():

        # set state for node
        g_plus.node[i]['s'] = node_strategy_selection(i)

        # interact
        for j in g.neighbors(i):
            if g.node[i]['s'] == C and g.node[j]['s'] ==  D:
                g_plus.node[i]['f'] += -2
                g_plus.node[j]['f'] += 2
                g_plus.edge[i][j]['w'] += -1
            
            if g.node[i]['s'] ==  D and g.node[j]['s'] == C:
                g_plus.node[i]['f'] += 2
                g_plus.node[j]['f'] += -2
                g_plus.edge[i][j]['w'] += -1
            
            if g.node[i]['s'] == C and g.node[j]['s'] == C:
                g_plus.node[i]['f'] += 1
                g_plus.node[j]['f'] += 1
                g_plus.edge[i][j]['w'] += 2

            if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
                g_plus.node[i]['f'] += 0
                g_plus.node[j]['f'] += 0
                g_plus.edge[i][j]['w'] += 0
                
    g = g_plus.copy()

def plot(plotfile):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(time_list, fitness_state, 'b-')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Global trust states')

    ax2 = fig.add_subplot(212)
    ax2.plot(time_list, state_changes, 'r-')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Global fitness states')
    
    plt.savefig(plotfile)

# run as many steps as the user wants
for time in range(0, args.iterations):
    g_pre = g.copy()
    step_sync()
    report()
    
# write down a plot
plot(args.plot)



