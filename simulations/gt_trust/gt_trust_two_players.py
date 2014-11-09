import random
import matplotlib
import pylab as pl
import matplotlib.pyplot as plt
import pprint


C = True
D = False


def random_strategy(player, T, t): #players get their strategies randomly    
    return random.choice([D,C, ])

def tit_for_tat(player, T, t):
    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'
    
    return T[t]['s_'+other_player]



def selfish_memory(player, T, t):
    
    if T[t-1]['f_'+player] < T[t]['f_'+player]:
        # fitness increase, same strategy as last iteration
        return T[t]['s_'+player]
    else:
        # fitness decrease, switch strategy
        if T[t]['s_'+player] == C:
            return  D
        else:
            return C




def selfish_perfect_memory(player, T, t):
    
    if T[t-1]['f_'+player] < T[t]['f_'+player]:
        # fitness increase, same strategy as last iteration
        return T[t]['s_'+player]
    else:
        # fitness decrease, CHOOSE strategy
        # build memory of past choices 
        choices = [ T[t]['s_'+player], ]

        for i in range(1, len(T)):
            if T[i-1]['f_'+player] < T[i]['f_'+player]:
                choices.append(T[i-1]['s_'+player])

        return random.choice( choices )



def selfish_memory_weighted_random(player, T, t):
    
    if T[t-1]['f_'+player] < T[t]['f_'+player]:
        # fitness increase, same strategy as last iteration
        return T[t]['s_'+player]
    else:
        # fitness decrease, CHOOSE strategy
        if random.random() > 0.7:
            return T[t]['s_'+player]
        else:
            return not T[t]['s_'+player]
    

# perfect memory tit for tat
def proportional_tit_for_tat(player, T, t):
    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    # past choices of the other player
    choices = []
    for s in T:
        choices.append(s['s_'+other_player])

    return random.choice( choices )



def memory_tit_for_tat(player, T, t):

    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    # past choices of the other player
    memory_size = 15
    choices = []
    if len(T)<memory_size:
        for s in T:
            choices.append(s['s_'+other_player])
    else:
        for n in range(len(T)-1,len(T)-memory_size,-1):
            choices.append(T[n]['s_'+other_player])

    return random.choice( choices )



# players have different memory span
def different_memories_tit_for_tat(player, T, t):
    if player == 'a':
        other_player = 'b'
        memory_size = 15
    elif player == 'b':
        other_player = 'a'
        memory_size = 5

    # past choices of the other player
    choices = []
    if len(T)<memory_size:
        for s in T:
            choices.append(s['s_'+other_player])
    else:
        for n in range(len(T)-1,len(T)-memory_size,-1):
            choices.append(T[n]['s_'+other_player])
          
    return random.choice( choices )




def selfish_differential_fitness(player, T, t):
    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    if T[t]['f_'+player] > T[t]['f_'+other_player]:
        # I'm winning!
        return T[t]['s_'+player]
    else:
        # must change

        if T[t]['f_'+other_player]:
            p = 1 - (float(T[t]['f_'+player])/float(T[t]['f_'+other_player]))
        else:
            p = 1 - (float(T[t]['f_'+player]+1)/float(T[t]['f_'+other_player]+1))

        print player,T[t]['f_'+player],T[t]['f_'+other_player],p
        
        if random.random() < p:
            return T[t]['s_'+other_player]
        else:
            return T[t]['s_'+player]



def altruist_differential_fitness(player, T, t):

    if player == 'a':
        other_player = 'b'
    elif player == 'b':
        other_player = 'a'

    if T[t]['f_'+player] > T[t]['f_'+other_player]:
        # I'm winning!
        # too far?
        if T[t]['f_'+other_player]:
            p = 1 - (float(T[t]['f_'+other_player])/float(T[t]['f_'+player]))
        else:
            p = 1 - (float(T[t]['f_'+player]+1)/float(T[t]['f_'+other_player]+1))

        if random.random() < p:
            return True
        else:
            return T[t]['s_'+other_player]
    else:
        return not T[t]['s_'+player]
#        return True



def trust_dependant_strategy(player, T, t):
    tmp = 1
    increments = 0
    decrements = 0
    while tmp<len(T):
        if T[tmp-1]['trust'] < T[tmp]['trust']:
            increments += T[tmp]['trust'] - T[tmp-1]['trust']
        else:
            decrements += T[tmp-1]['trust'] - T[tmp]['trust']
        tmp += 1


    if (increments - decrements) > 0:
        # trust increment
        #return T[t-1]['s_'+player]
        return memory_tit_for_tat(player, T, t)
    else:
        print t, increments, decrements, increments - decrements, float(decrements) / (float(increments) + float(decrements))
        if random.random() < float(decrements) / (float(increments) + float(decrements)):
            return True
        else:
            return False



def step(state, T, t, strategy=random_strategy): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor. Prisoner's Dilemma T > R > P > S; Snowdrift game: T > R > S > P. Actual configuration is Prisoner's Dilemma

    if state['s_a'] == C and state['s_b'] ==  D:
        return {'f_a': state['f_a']-2,
                's_a': strategy('a',T,t),
                'f_b': state['f_b']+2,
                's_b': strategy('b',T,t),
                'trust': state['trust']-1}

            
    if state['s_a'] ==  D and state['s_b'] == C:
        return {'f_a': state['f_a']+2,
                's_a': strategy('a',T,t),
                'f_b': state['f_b']-2,
                's_b': strategy('b',T,t),
                'trust': state['trust']-1}


    if state['s_a'] == C and state['s_b'] == C:
        return {'f_a': state['f_a']+1,
                's_a': strategy('a',T,t),
                'f_b': state['f_b']+1,
                's_b': strategy('b',T,t),
                'trust': state['trust']+2}

    if state['s_a'] ==  D and state['s_b'] ==  D:
        return {'f_a': state['f_a']-1,
                's_a': strategy('a',T,t),
                'f_b': state['f_b']-1,
                's_b': strategy('b',T,t),
                'trust': state['trust']-2}





# plot
def plot(T, path):
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

        if t['s_a']== C:
            id_a.append(-1)
        else:
            id_a.append(-2)

        if t['s_b']== C:
            id_b.append(-3)
        else:
            id_b.append(-4)

        time_list.append(n)
        n+=1



    plt.plot(time_list,trust_list, 'bs-')
    plt.plot(time_list,fitness_a, 'r--')
    plt.plot(time_list,fitness_b,'g+-')
    plt.plot(time_list,id_a,'r--')
    plt.plot(time_list,id_b,'g+-')
    #plt.show()
    plt.savefig(path)


