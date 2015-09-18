from random import choice, randint
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from pprint import pprint
import networkx as nx

A = True
B = False

nodes = 100


# agentes se inicializan con behaviours
agentes        = range(nodes)
agent_behavior = [choice([A,B]) for n in range(nodes)]
agent_fitness  = [0 for n in range(nodes)]





###################
# init adj matrix #
###################
# original adj_matrix
adj_matrix = []
for i in range(nodes):
    adj_matrix.append([])
    for j in range(nodes):
        adj_matrix[i].append(0)
        
adj_matrix_L = list(adj_matrix)


g = nx.erdos_renyi_graph(nodes, 0.1)

for s,t in g.edges():
    interaction  = choice([-1,1])
    adj_matrix[s][t] = interaction
    adj_matrix[t][s] = interaction



    
    
def utilidad_global():
    return sum( [agent_fitness[i] for i in agentes] )


def vecinos(i):
    """
    todos los nodos son sus vecinos, hay que quitar i
    """
    vecindad = []
    for j in range(len(adj_matrix[i])):
        if adj_matrix[i][j] != 0:
            vecindad.append(j)

    return vecindad
    


def capping_theta(n):
    if n>1:
        return 1
    elif n<-1:
        return -1
    else:
        return n


def update_behavior(i):
    current_behavior_i = agent_behavior[i]

    agent_behavior[i] = A
    local_utility_A = sum( [outcome(i, j) * capping_theta(adj_matrix[i][j] + adj_matrix_L[i][j]) for j in vecinos(i)] ) 
    agent_behavior[i] = B    
    local_utility_B = sum( [outcome(i, j) * capping_theta(adj_matrix[i][j] + adj_matrix_L[i][j]) for j in vecinos(i)] )

    if local_utility_A == local_utility_B:
        agent_behavior[i] = current_behavior_i # no update
    elif local_utility_A > local_utility_B:
        agent_behavior[i] = A
    else:
        agent_behavior[i] = B 



def learn(i):
    # compute local utility A
    current_w_L = list(adj_matrix_L)
    r = 0.005
    for j in vecinos(i):
        current_w_L[i][j] = current_w_L[i][j] + (r * agent_behavior[i] * agent_behavior[j])

    local_utility_A = sum( [outcome(i, j) * capping_theta(adj_matrix[i][j] + current_w_L[i][j]) for j in vecinos(i)] )

    # compute local utility B    
    current_w_L = list(adj_matrix_L)
    r = - 0.005
    for j in vecinos(i):
        current_w_L[i][j] = current_w_L[i][j] + (r * agent_behavior[i] * agent_behavior[j])

    local_utility_B = sum( [outcome(i, j) * capping_theta(adj_matrix[i][j] + current_w_L[i][j]) for j in vecinos(i)] )

    
    if local_utility_A == local_utility_B:
        pass
    elif local_utility_A > local_utility_B:
        r = 0.005
        for j in vecinos(i):        
            adj_matrix_L[i][j] = adj_matrix_L[i][j] + (r * agent_behavior[i] * agent_behavior[j])
            adj_matrix_L[j][i] = adj_matrix_L[j][i] + (r * agent_behavior[i] * agent_behavior[j])
    else:
        r = - 0.005
        for j in vecinos(i):        
            adj_matrix_L[i][j] = adj_matrix_L[i][j] + (r * agent_behavior[i] * agent_behavior[j])
            adj_matrix_L[j][i] = adj_matrix_L[j][i] + (r * agent_behavior[i] * agent_behavior[j])

            

def outcome(i, j):
    # del payoff matrix
    if agent_behavior[i] == agent_behavior[j]:
        return 1
    else:
        return 0



def play(i):
    update_behavior(i)
    agent_fitness[i] = sum( [outcome(i, j) for j in vecinos(i)] )
       


def play_and_learn(i):
    update_behavior(i)
    learn(i)
    agent_fitness[i] = sum( [outcome(i, j) for j in vecinos(i)] )


    
u = []

def period(length):
    for t in range(length):
        play(randint(0,nodes-1))
    u.append(utilidad_global())


def learn_period(length):
    for t in range(length):
        play_and_learn(randint(0,nodes-1))
    u.append(utilidad_global())


# no learning loop
for n in range(1000):
    period(1000)    
    agent_behavior = [choice([A,B]) for n in range(nodes)]



# learning loop
for n in range(1000):
    learn_period(1000)    
    agent_behavior = [choice([A,B]) for n in range(nodes)]


# no learning loop
for n in range(1000):
    period(1000)    
    agent_behavior = [choice([A,B]) for n in range(nodes)]
    
    
plt.cla()
plt.scatter( range(3000), u, c=u'r', marker=u'D' )
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('hebbian_agents.svg')

