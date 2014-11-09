import gt_trust_two_players

C = True
D = False

state0 = {'f_a': 10,
          's_a': D,
          'f_b': 10,
          's_b': C,
          'trust': 10,}

T = [ state0,  ]

t=0
while T[t]['trust']>0 and t<200:
    state = gt_trust_two_players.step(T[t], T, t, strategy=gt_trust_two_players.random_strategy)
    T.append( state )
    t +=1


gt_trust_two_players.plot(T, 'random_strategy.png')