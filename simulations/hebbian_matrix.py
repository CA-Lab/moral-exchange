import numpy as np
import random
from pprint import pprint

number_of_nodes = 20
number_of_iterations = 20
r = 0.0045


node = [random.choice([-1,0,1]) for n in range(number_of_nodes)]
node_p = list(node)
f_node_p = list(node)


w = number_of_nodes
h = number_of_nodes


# real network, edges init to zero
u_r = np.zeros((w, h))
# percieved network, init some edges as -1 or 1
u_p = np.zeros((w, h))
for i in range(h):
    for j in range(w):
        if random.random() < 0.1:
            u_p[i][j] = random.choice([-1,1])


f_u_r = u_r.copy()
f_u_p = u_p.copy()


def node_state(n):
    
    m_1 = 0
    m_2 = 0

    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            m_1 += (u_p[i][j] + u_r[i][j]) * -1 * node[n]
            m_2 += (u_p[i][j] + u_r[i][j]) *  1 * node[n]
            
    if m_1 > m_2:
        return -1
    else:
        return 1
        

def learn(i,j):
    m_1 = 0
    m_2 = 0
    for n in range(number_of_nodes):
        for m in range(number_of_nodes):
            m_1 += (u_r[n][m] + u_p[n][m] + r) * node_p[n] * node_p[m]
            m_2 += (u_r[n][m] + u_p[n][m] - r) * node_p[n] * node_p[m]

    if m_1 > m_2:
        return u_r[i][j] + r
    else:
        return u_r[i][j] - r 

   


len(node)
len(node_p)

for t in range(0, number_of_iterations):
    for n in range(number_of_nodes):
        f_node_p[n] = node_state(n)
        
    for n in range(number_of_nodes):
        for m in range(number_of_nodes):
            f_u_r = learn(n,m)


    len(node)
    len(f_node_p)            
    node_p, u_r = f_node_p, f_u_r

    pprint(node)
    pprint(node_p)

