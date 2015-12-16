from gt_trust_two_players import *

C = True
D = False

state0 = {'f_a': 10,
          's_a': D,
          'f_b': 10,
          's_b': C,
          'trust': 10,}

state1 = {'f_a': 12,
          's_a':  C,
          'f_b': 8,
          's_b':  D,
          'trust': 9,}

runs = []
for i in range(0,1000):
    T = [ state0,  ]
    state = step(T[0], T, 0, strategy=random_strategy)
    T.append( state )

    t=1
    while T[t]['trust']>0 and t<200:
        state = step(T[t], T, t, strategy=selfish_perfect_memory)
        T.append( state )
        t +=1

    runs.append(T)


multiplot(runs, 'selfish_memory_multi.png')
