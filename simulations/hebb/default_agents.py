from random import choice, randint
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt


A = True
B = False

# agentes se inicializan con behaviours
agentes        = range(100)
agent_behavior = [choice([A,B]) for n in range(100)]
agent_fitness  = [0 for n in range(100)]


def utilidad_global():
    return sum( [agent_fitness[i] for i in agentes] )


def vecinos(i):
    """
    todos los nodos son sus vecinos, hay que quitar i
    """
    vecindad = list(agentes)
    vecindad.remove(i)
    return vecindad

def update_behavior(i):
    current_behavior_i = agent_behavior[i]

    agent_behavior[i] = A
    local_utility_A = sum( [outcome(i, j) for j in vecinos(i)] )
    agent_behavior[i] = B    
    local_utility_B = sum( [outcome(i, j) for j in vecinos(i)] )

    if local_utility_A == local_utility_B:
        agent_behavior[i] = current_behavior_i # no update
    elif local_utility_A > local_utility_B:
        agent_behavior[i] = A
    else:
        agent_behavior[i] = B 


        

def outcome(i, j):
    # del payoff matrix
    if agent_behavior[i] == agent_behavior[j]:
        return 1
    else:
        return 0



def play(i):
    update_behavior(i)
    agent_fitness[i] = sum( [outcome(i, j) for j in vecinos(i)] )
       



u = []

for t in range(1000):
    play(randint(0,99))
    u.append(utilidad_global())



plt.cla()
plt.scatter( range(1000), u, c=u'r', marker=u'D' )
plt.xlabel('Time')
plt.ylabel('Global Utility')
plt.savefig('default_agents.svg')
