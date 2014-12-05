from gt_trust_two_players import *

C = True
D = False

state0 = {'f_a': 10,
          's_a': D,
          'f_b': 10,
          's_b': C,
          'trust': 10,}

runs = []
for i in range(0,1000):
    T = [ state0,  ]

    t=0
    while T[t]['trust']>0 and t<200:
        state = step(T[t], T, t, strategy=random_strategy)
        T.append( state )
        t +=1
        
    runs.append(T)


multiplot(runs, 'random_strategy_multi.png')
