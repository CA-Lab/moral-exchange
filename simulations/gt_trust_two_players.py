import random
import matplotlib
import pylab as pl
import matplotlib.pyplot as plt
import pprint

def random_strategy(player): #players get their strategies randomly    
    return random.choice(['d','c'])

def tit_for_tat(player):
    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'
    
    return T[t]['s_'+other_player]



def selfish_memory(player):
    print player, t, T
    
    if T[t-1]['f_'+player] < T[t]['f_'+player]:
        # fitness increase, same strategy as last iteration
        print "fitness increase"
        return T[t]['s_'+player]
    else:
        print "fitness decrease"
        # fitness decrease, switch strategy
        if T[t]['s_'+player] == 'c':
            return 'd'
        else:
            return 'c'


def proportional_tit_for_tat(player):
    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    # past choices of the other player
    choices = []
    for s in T:
        choices += s['s_'+other_player]

    return random.choice( choices )



def memory_tit_for_tat(player):

    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    # past choices of the other player
    memory_size = 20
    choices = []
    if len(T)<memory_size:
        for s in T:
            choices += s['s_'+other_player]
    else:
        for n in range(len(T)-1,len(T)-memory_size,-1):
            choices += T[n]['s_'+other_player]

    return random.choice( choices )



def step(state, strategy=random_strategy): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor. Prisoner's Dilemma T > R > P > S; Snowdrift game: T > R > S > P. Actual configuration is Prisoner's Dilemma

    if state['s_a'] == 'c' and state['s_b'] == 'd':
        return {'f_a': state['f_a']-2,
                's_a': strategy('a'),
                'f_b': state['f_b']+2,
                's_b': strategy('b'),
                'trust': state['trust']-1}

            
    if state['s_a'] == 'd' and state['s_b'] == 'c':
        return {'f_a': state['f_a']+2,
                's_a': strategy('a'),
                'f_b': state['f_b']-2,
                's_b': strategy('b'),
                'trust': state['trust']-1}


    if state['s_a'] == 'c' and state['s_b'] == 'c':
        return {'f_a': state['f_a']+1,
                's_a': strategy('a'),
                'f_b': state['f_b']+1,
                's_b': strategy('b'),
                'trust': state['trust']+2}

    if state['s_a'] == 'd' and state['s_b'] == 'd':
        return {'f_a': state['f_a']-1,
                's_a': strategy('a'),
                'f_b': state['f_b']-1,
                's_b': strategy('b'),
                'trust': state['trust']-2}



initial_state = {'f_a': 10,
                 's_a': 'c',
                 'f_b': 10,
                 's_b': 'd',
                 'trust': 30,}

initial_state1 = {'f_a': 8,
                 's_a': 'd',
                 'f_b': 12,
                 's_b': 'c',
                 'trust': 29,}

T = [ initial_state, initial_state1,]

t=1
while T[t]['trust']>0 and t<200:
    state = step(T[t], strategy=selfish_memory)
    print state
    T.append( state )
    t +=1




# plot
trust_list = []
fitness_a = []
fitness_b = []
id_a = []
id_b = []
time_list = []
n = 0
for t in T:
    trust_list.append(t['trust'])
    fitness_a.append(t['f_a'])
    fitness_b.append(t['f_b'])

    if t['s_a']=='c':
        id_a.append(-1)
    else:
        id_a.append(-2)

    if t['s_b']=='c':
        id_b.append(-3)
    else:
        id_b.append(-4)

    time_list.append(n)
    n+=1


pprint.pprint(T)
plt.plot(time_list,trust_list, 'bs-')
plt.plot(time_list,fitness_a, 'r--')
plt.plot(time_list,fitness_b,'g+-')
plt.plot(time_list,id_a,'r--')
plt.plot(time_list,id_b,'g+-')
plt.show()


