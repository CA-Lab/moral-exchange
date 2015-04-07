import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
from pprint import pprint
from initializators import *
import argparse

parser = argparse.ArgumentParser(description='Prissoner\'s dilema with trust network simulation.')
parser.add_argument('--runid', default="" )
parser.add_argument('--iterations', type=int, default=500 )
parser.add_argument('--plot',   type=argparse.FileType('w'), help="path to plot", default=open('aguas.png', 'w') )
parser.add_argument('--optimize', default="balance", choices=['fitness', 'trust', 'balance'] )
parser.add_argument('--step', default="async", choices=['async', 'sync'] )

args = parser.parse_args()


# log keeping variables
time = 0
time_list = []
energy_state = []
fitness_state = []

# states: cooperate, detract
C = True
D = False
# threshold for state change
theta = 1

def normalize(g):

    G = g.copy()
    
    # calculate global trust
    trust = []
    for i, j in G.edges():
        trust.append( G.edge[i][j]['w']  )
    T = float(sum(trust))

    # normalize trust
    for i, j in G.edges():
        G.edge[i][j]['w'] = G.edge[i][j]['w'] / T

        
    # calculate global fitness
    fitness = []
    for i in G.nodes():
        fitness.append( G.node[i]['f'] )
    F = float(sum(fitness))

    for i in G.nodes():
        G.node[i]['f'] = G.node[i]['f'] / F

    return G


def report():
    global time, g, energy_state, fitness_state

    time_list.append(time)

    # report global trust
    ef = []
    for i, j in g.edges():
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            ef.append( g.edge[i][j]['w']  )
    E = sum(ef)

    energy_state.append(E)

    # report global fitness
    fitness_i = []
    for i in g.nodes():
        fitness_i.append( g.node[i]['f'] )
    F = sum(fitness_i)

    fitness_state.append(F)


def plot(plotfile):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(time_list, energy_state, 'b-')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Global trust states')

    ax2 = fig.add_subplot(212)
    ax2.plot(time_list, fitness_state, 'r-')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Global fitness states')

    plt.savefig(plotfile)


def node_state_optimize_trust(node):
    global g, theta
    tau = sum([g.edge[node][j]['w'] for j in g.neighbors(node)]) # tau for trust: sum of the weights in edges from this node

    if not g.node[node]['f']:
        f = 0.0000000001
    else:
        f = g.node[node]['f']
    
    d = float(tau) / f
    
    if d <= theta:
        return not g.node[node]['s']
    else:
        return g.node[node]['s']


def node_state_optimize_fitness(node):
    global g, theta
    tau = sum([g.edge[node][j]['w'] for j in g.neighbors(node)]) # sum of the weights in edges from this node

    if not tau:
        tau = 0.0000000001
    
    d = g.node[node]['f'] / float(tau)
    
    if d <= theta:
        return not g.node[node]['s']
    else:
        return g.node[node]['s']

import operator

def node_state_optimize_balance(node):
    # will accumulate fitness_delta + trust for each pair of
    # cooperate, detract; detract, cooperate;
    # cooperate, cooperate; detract, detract
    b = {(C,D): 0,
         (D,C): 0,
         (C,C): 0,
         (D,D): 0, }
    for j in g.neighbors(node):
        if g.node[node]['s'] == C and g.node[j]['s'] == D:
            b[C,D] += -2 + g.edge[node][j]['w']

        if g.node[node]['s'] == D and g.node[j]['s'] == C:
            b[D,C] += 2 + g.edge[node][j]['w']
            
        if g.node[node]['s'] == C and g.node[j]['s'] == C:
            b[C,C] += 1  + g.edge[node][j]['w']

        if g.node[node]['s'] == D and g.node[j]['s'] == D:
            b[D,D] += g.edge[node][j]['w']
            
    # choose the best strategy sorting dictionary b
    sorted_b = sorted(b.items(), key=operator.itemgetter(1))
    # grab key (C or D) of largest value
    return sorted_b[-1][0][0]




if args.optimize == 'trust':
    node_strategy = node_state_optimize_trust
elif args.optimize == 'fitness':
    node_strategy = node_state_optimize_fitness
elif args.optimize == 'balance':
    node_strategy = node_state_optimize_balance
    
def step_async():
    global time, g
    time += 1

    # grab a node
    i = rd.choice(g.nodes())
    
    #
    # set state for node
    #
    g.node[i]['s'] = node_strategy(i)

        
    # interact
    for j in g.neighbors(i):
        if g.node[i]['s'] == C and g.node[j]['s'] ==  D:
            g.node[i]['f'] += -2
            g.node[j]['f'] += 2
            g.edge[i][j]['w'] += -1
            
        if g.node[i]['s'] ==  D and g.node[j]['s'] == C:
            g.node[i]['f'] += 2
            g.node[j]['f'] += -2
            g.edge[i][j]['w'] += -1
            
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            g.node[i]['f'] += 1
            g.node[j]['f'] += 1
            g.edge[i][j]['w'] += 2

        if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
            g.node[i]['f'] += 0
            g.node[j]['f'] += 0
            g.edge[i][j]['w'] += 0


    
    
            
def step_sync():
    global time, g
    time += 1

    g_plus = g.copy()

    # do all nodes
    for i in g.nodes():

        # set state for node
        g_plus.node[i]['s'] = node_strategy(i)

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



if args.step == 'sync':
    step = step_sync
elif args.step == 'async':
    step = step_async

    

# initialize network
g = init_watts()

# run as many steps as the user wants
for time in range(0, args.iterations):
    step()
    report()
#    g = reset_fitness_and_trust(g)

# write down a plot
plot(args.plot)
