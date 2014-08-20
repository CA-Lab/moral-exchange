import random

def random_strategy(): #players get their strategies randomly    
    return random.choice(['d','c'])


def step(state, strategy=random_strategy): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor. Prisoner's Dilemma T > R > P > S; Snowdrift game: T > R > S > P. Actual configuration is Prisoner's Dilemma

    if state['s_a'] == 'c' and state['s_b'] == 'd':
        return {'f_a': state['f_a']-2,
                's_a': strategy(),
                'f_b': state['f_b']+2,
                's_b': strategy(),
                'trust': state['trust']-1}

            
    if state['s_a'] == 'd' and state['s_b'] == 'c':
        return {'f_a': state['f_a']+2,
                's_a': strategy(),
                'f_b': state['f_b']-2,
                's_b': strategy(),
                'trust': state['trust']-1}


    if state['s_a'] == 'c' and state['s_b'] == 'c':
        return {'f_a': state['f_a']+1,
                's_a': strategy(),
                'f_b': state['f_b']+1,
                's_b': strategy(),
                'trust': state['trust']+2}

    if state['s_a'] == 'd' and state['s_b'] == 'd':
        return {'f_a': state['f_a']-1,
                's_a': strategy(),
                'f_b': state['f_b']-1,
                's_b': strategy(),
                'trust': state['trust']-2}



initial_state = {'f_a': 10,
                 's_a': 'c',
                 'f_b': 10,
                 's_b': 'c',
                 'trust': 10,}

t = [ initial_state, ]

n=0
while t[n]['trust']>0:
    t.append(step(t[n]))
    n +=1


import pprint
pprint.pprint(t)