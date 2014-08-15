#!/usr/bin/python

import networkx as nx
import random as rd
import matplotlib
matplotlib.use('TkAgg')
import pylab as pl
import matplotlib.pyplot as plt

nt = nx.Graph()
nt.add_node( 'a' )
nt.add_node( 'b' )
nt.add_edge( 'a', 'b', t=10.0 )

def init(): #posteriormente arreglar para escoger la condicion de
    #incio: dos cooperadores, cooperador vs detractor, dos
    #detractores o inicio aleatorio. Tambien para definir los valores
    #del fitness y de la confianza

    global time, nt, positions

    time = 0
    
    #nt.node['a']['id'] = c
    #nt.node['b']['id'] = d

    nt.node['a']['w'] = 10.0 #fitness inicial
    nt.node['b']['w'] = 10.0 #fitness inicial



    
    nodes = nt.nodes(True)
     

init()

positions = nx.random_layout(nt)

# nx.draw(nt)
# plt.show()


# def draw():
#     pl.cla()
#     nx.draw(nt, pos = positions, node_color = [nt.node[i]['id'] for i in nt.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1)
#     #Falta dibujar el vinculo con el grosor del mismo representando el grado de confianza
#     pl.axis('image')
#     pl.title('t = ' + str(time))
#     plt.show() 

def node_strategy(): #players get their strategies randomly    
    x = 0.5 #eventualmente modificar para que quien corra la simulacion elija la probabilidad de que el nodo salga cooperador o detractor.
    for i in nt.nodes():
        if x > rd.random():
            nt.node[i]['id'] = 'c'
        else:
            nt.node[i]['id'] = 'd'



def fitness(): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor
    for i, j in nt.edges():
        if nt.node[i]['id'] == 'c' and nt.node[j]['id'] == 'd':
            nt.node[i]['w'] -= 1.0
            nt.node[j]['w'] += 2.0
            
        if nt.node[i]['id'] == 'd' and nt.node[j]['id'] == 'c':
            nt.node[i]['w'] += 2.0
            nt.node[j]['w'] -= 1.0

        if nt.node[i]['id'] == 'c' and nt.node[j]['id'] == 'c':
            nt.node[i]['w'] += 0.5
            nt.node[j]['w'] += 0.5

        if nt.node[i]['id'] == 'd' and nt.node[j]['id'] == 'd':
            nt.node[i]['w'] -= 2
            nt.node[j]['w'] -= 2



def trust(): #Funcion de evaluacion de la confianza
    for i, j in nt.edges():
        if nt.node[i]['id'] != nt.node[j]['id']:
            nt.edge[i][j]['t'] -= 1
                
        if nt.node[i]['id'] == 'c' and nt.node[j]['id'] == 'c':
            nt.edge[i][j]['t'] += 2

        if nt.node[i]['id']=='d' and nt.node[j]['id']=='d':
            nt.edge[i][j]['t'] -= 2

import pprint

def step():
    global time, nt, positions
    time += 1
    node_strategy()
    fitness()
    trust()



time_list = []
trust_list = []
fitness_a = []
fitness_b = []
id_a = []
id_b = []
while nt.get_edge_data('a','b')['t']>=0 and (nt.node['a']['w']>=0 or nt.node['b']['w']>=0) and time<100:
    step()
    time_list.append(time)
    trust_list.append(nt.get_edge_data('a','b')['t'])
    fitness_a.append(nt.node['a']['w'])
    fitness_b.append(nt.node['b']['w'])
    if nt.node['b']['id']=='c':
        id_b.append(-1)
    else:
        id_b.append(-2)

    if nt.node['a']['id']=='c':
        id_a.append(-3)
    else:
        id_a.append(-4)



plt.plot(time_list,trust_list)
plt.plot(time_list,fitness_a,color='r')
plt.plot(time_list,fitness_b,color='g')
plt.plot(time_list,id_a,color='r')
plt.plot(time_list,id_b,color='g')
plt.show()

#step()
#draw()

#def ploteo():    

#import pycxsimulator
#pycxsimulator.GUI().start(func = [init, draw, step])


