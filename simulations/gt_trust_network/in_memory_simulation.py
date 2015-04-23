import matplotlib
#matplotlib.use('svg')
import matplotlib.pyplot as plt
import pylab as pl
import operator
import random as rd
from initializators import *
import argparse
import numpy as np

from pprint import pprint
from time import sleep

parser = argparse.ArgumentParser(description='Prissoner\'s dilema with trust network simulation.')
parser.add_argument('--runid', default="" )
parser.add_argument('--iterations', type=int, default=50 )
parser.add_argument('--optimize', default="probabilistic", choices=['fitness', 'trust', 'balance', 'majority', 'probabilistic'] )
parser.add_argument('--init', default="erdos", choices=['simple', 'full', 'real', 'erdos', 'di_erdos', 'di_watts', 'watts', 'barabasi', 'di_scale_free', 'fosiss'] )
parser.add_argument('--step', default="sync", choices=['async', 'sync'] )

args = parser.parse_args()


# log keeping variables
time = 0
time_list = []
energy_state = []
energy_state_S = []
fitness_state = []
fitness_S = []
DC_ratio      = []
state_changes = []

# initial and final fitnesses and trusts
F_t0 = []
F_tn = []
T_t0 = []
T_tn = []

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
    global time, g, g_pre, energy_state, fitness_state

    time_list.append(time)

    # report global trust
    ef = []
    for i, j in g.edges():
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            ef.append( g.edge[i][j]['w']  )
    E = float(sum(ef) ) / float( len( g.edges() ) )

    energy_state.append(E)
    Es = np.std(ef)
    energy_state_S.append(Es)

    # report global fitness
    fitness_i = []
    for i in g.nodes():
        fitness_i.append( g.node[i]['f'] )
    F = float(sum(fitness_i)) / float( len( g.nodes() ) )
    fitness_state.append(F)

    Fs = np.std(fitness_i)
    fitness_S.append(Fs)

    

    # report ratio of C or D
    cooperators = 0
    l = len(g.nodes())    
    for i in g.nodes():
        if g.node[i]['s'] == C:
            cooperators += 1.0

    DC_ratio.append( cooperators / l )


    changed = 0
    for n in g.nodes():
        if g.node[n]['s'] != g_pre.node[n]['s']:
            changed+=1
#            print time,g.node[n]['s'], g_pre.node[n]['s']
            
    state_changes.append(changed)

                
    if time == args.iterations - 1:
        for n in g.nodes():
            F_tn.append(g.node[n]['f'])
        for e in g.edges():
            T_tn.append(g.get_edge_data(*e)['w'])
    

    
def plot_dynamics(plotfile):
    fig = plt.figure(figsize=(23.5, 13.0))
    ax1 = fig.add_subplot(411)
    ax1.plot(time_list, energy_state, 'b-') 
    ax1.plot(time_list, energy_state_S, 'b--') 
    ax1.set_xlabel('Time')
    ax1.set_ylabel('mean trust states')

    ax2 = fig.add_subplot(412)
    ax2.plot(time_list, fitness_state, 'r-')
    ax2.plot(time_list, fitness_S, 'r--')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('mean fitness states')

    ax3 = fig.add_subplot(413)
    ax3.plot(time_list, state_changes, 'g-')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('state changes per step')

    ax4 = fig.add_subplot(414)
    ax4.plot(time_list, DC_ratio, 'r-')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('DC ratio')
    
    plt.savefig(plotfile, dpi=300)



def plot_histograms(plotfile):
#    pprint(T_t0)

    fig = plt.figure(figsize=(23.5, 13.0))

    ax3 = fig.add_subplot(221)
    ax3.hist(T_t0, 50, normed=0, facecolor='b', alpha=0.33)
    
    ax4 = fig.add_subplot(222)
    ax4.hist(T_tn, 50, normed=0, facecolor='b', alpha=0.77)
    
    ax1 = fig.add_subplot(223)
    ax1.hist(F_t0, 50, normed=0, facecolor='r', alpha=0.33)

    ax2 = fig.add_subplot(224)
    ax2.hist(F_tn, 50, normed=0, facecolor='r', alpha=0.77)

    
    plt.savefig(plotfile, dpi=300)

    
    

def node_state_optimize_trust(node):
    global g, theta
    
    tau = sum([g.edge[node][j]['w'] for j in g.neighbors(node)]) # tau for trust: sum of the weights in edges from this node

    # small trust? must change!
    if tau <= 0:
        return not g.node[node]['s']
    
    if not g.node[node]['f']:
        f = 0.0000000001
    else:
        f = g.node[node]['f']
    
    d = float(tau) / float(f)

    if d <= theta:
        return not g.node[node]['s']
    else:
        return g.node[node]['s']


def node_state_optimize_fitness(node):
    global g, theta

    # no fitness? must change!
    if g.node[node]['f'] <= 0:
        return not g.node[node]['s']        
    
    tau = sum([g.edge[node][j]['w'] for j in g.neighbors(node)]) # sum of the weights in edges from this node

    if not tau:
        tau = 0.0000000001
    
    d = float(g.node[node]['f']) / float(tau)
    
    if d <= theta:
        return not g.node[node]['s']
    else:
        return g.node[node]['s']


def node_state_optimize_majority(node):
    global g

    neighbors_C = []
    neighbors_D = []

    for j in g.neighbors(node):
        if g.node[j]['s'] == C:
            neighbors_C.append( g.node[j]['s'] )
        else:
            neighbors_D.append( g.node[j]['s'] )
    
    if len( neighbors_C ) > len( neighbors_D ):
        return g.node[node]['s'] == C
    elif len( neighbors_C ) < len( neighbors_D ):
        return g.node[node]['s'] == D
    else:
        return g.node[node]['s']


    
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



def node_state_probabilistic(i):
    f_i   = 0
    c_i_j = 0
    for j in g.neighbors(i):
        if g.node[i]['s'] == C and g.node[j]['s'] ==  D:
            f_i   += -1
            c_i_j += -.5
            
        if g.node[i]['s'] ==  D and g.node[j]['s'] == C:
            f_i   += 1
            c_i_j += -.5
                       
        if g.node[i]['s'] == C and g.node[j]['s'] == C:
            f_i   += .5
            c_i_j += 1

        if g.node[i]['s'] ==  D and g.node[j]['s'] ==  D:
            f_i   += 0
            c_i_j += 0

    fitness   = float(f_i) / float(len(g.neighbors(i)))
    trust     = float(c_i_j) / float(len(g.neighbors(i)))
    naiveness =  fitness + trust

    if naiveness > 1:
        naiveness = 1

    if naiveness < 0:
        naiveness = 0

    if naiveness <= 0.20:
        state = D
    else:
        state = C

    return state





if args.optimize == 'trust':
    node_strategy = node_state_optimize_trust
elif args.optimize == 'fitness':
    node_strategy = node_state_optimize_fitness
elif args.optimize == 'balance':
    node_strategy = node_state_optimize_balance
elif args.optimize == 'majority':
    node_strategy = node_state_optimize_majority
elif args.optimize == 'probabilistic':
    node_strategy = node_state_probabilistic


def step_async():
    global time, g

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
if args.init == 'erdos':
    g = init_erdos()
elif args.init == 'simple':
    g = init_simple()
elif args.init == 'full':
    g = init_full()
elif args.init == 'di_erdos':
    g = init_erdos_directed()    
elif args.init == 'watts':
    g = init_watts()
elif args.init == 'di_watts':
    g = init_directed_watts()
elif args.init == 'barabasi':
    g = init_barabasi()
elif args.init == 'di_scale_free':
    g = init_di_scale_free()
elif args.init == 'real':
    g = init_real()
elif args.init == 'fosiss':
    g = init_fosiss()


for n in g.nodes():
    F_t0.append(g.node[n]['f'])

for e in g.edges():
    T_t0.append(g.get_edge_data(*e)['w'])

    
    
g_pre = g.copy()
# run as many steps as the user wants
for time in range(0, args.iterations):
    g_pre = g.copy()
    step()
    report() 

    
# write down a plot
dynamics_plot = "%s_%s_%s_dynamics.png" % (args.init, args.optimize, args.step)
histograms_plot = "%s_%s_%s_hist.png" % (args.init, args.optimize, args.step)
plot_dynamics(dynamics_plot)
plot_histograms(histograms_plot)
