import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
from pprint import pprint
from initializators import *

time_list = []
energy_state = []
fitness_state = []

C = True
D = False
time = 0
theta = 1


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


def draw():
    global time
    print time


def step_async():
    global time, g
    time += 1

    # grab a node
    i = rd.choice(g.nodes())
    

    # set state for node
    m = []    
    for j in g.neighbors(i):
        m.append( g.edge[i][j]['w'] )
        
    tau = sum(m)

    if not g.node[i]['f']:
        g.node[i]['f'] = 0.0000000001
    
    d   = tau / g.node[i]['f']

    
    if d <= theta:
        g.node[i]['s'] = not g.node[i]['s']

        
    # interact
    m_i = []
    m_j = []
    w = []
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


    # report
    time_list.append(time)
    
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

    
            
def step_sync_global():
    global time, g
    time += 1

    g_plus = g.copy()

    # do all nodes
    for i in g.nodes():

        # set state for node
        m = []
        for j in g.neighbors(i):
            m.append( g.edge[i][j]['w'] )
        
        tau = sum(m)

        if not g.node[i]['f']:
            g.node[i]['f'] = 0.0000000001

        d   = tau / g.node[i]['f']
        if d <= theta:
            g_plus.node[i]['s'] = not g.node[i]['s']


        # interact
        m_i = []
        m_j = []
        w = []
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

    # report Viendo la literatura F (fitness global) y Tau (Trust
    # global) deben ser promedios, es decir F = sum(f_i)/n, en donde n
    # es el numero de nodos en la red. Lo mismo para Trust global.
    time_list.append(time)
    
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


g = init_watts()
for time in range(0,1000):
    step_sync_global()

plot()
