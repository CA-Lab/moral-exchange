import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
from pprint import pprint
from initializators import *

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


def plot():
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(time_list, energy_state, 'bs-')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Global trust states')

    ax2 = fig.add_subplot(212)
    ax2.plot(time_list, fitness_state, 'ro-')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Global fitness states')

    plt.savefig('opt_trust.png')


def node_state_optimize_trust(node):
    global g
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
    global g
    tau = sum([g.edge[node][j]['w'] for j in g.neighbors(node)]) # sum of the weights in edges from this node

    if not tau:
        tau = 0.0000000001
    
    d = g.node[node]['f'] / float(tau)
    
    if d <= theta:
        return not g.node[node]['s']
    else:
        return g.node[node]['s']

    
def step_async():
    global time, g
    time += 1

    # grab a node
    i = rd.choice(g.nodes())
    
    #
    # set state for node
    #
    g.node[i]['s'] = node_state_optimize_trust(i)

        
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
            g.node[i]['f'] += -1
            g.node[j]['f'] += -1
            g.edge[i][j]['w'] += -2


    
    
            
def step_sync():
    global time, g
    time += 1

    g_plus = g.copy()

    # do all nodes
    for i in g.nodes():

        # set state for node
        g_plus.node[i]['s'] = node_state_optimize_trust(i)

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
                g_plus.node[i]['f'] += -1
                g_plus.node[j]['f'] += -1
                g_plus.edge[i][j]['w'] += -2


    g = g_plus.copy()



# initialize network
g = init_barabasi()

# run 1000 steps
for time in range(0,100):
    step_async()
    report()

# write down a plot
plot()
