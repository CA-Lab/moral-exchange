#!/usr/bin/python

import networkx as nx
import random as rd
import pylab as pl
import matplotlib
matplotlib.use('TkAgg')
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
    pprint.pprint( nt.nodes(True) )
    node_strategy()
    fitness()
    pprint.pprint( nt.nodes(True) )
    trust()
    pprint.pprint(nt.get_edge_data('a','b'))




step()
#draw()

#def ploteo():    

#import pycxsimulator
#pycxsimulator.GUI().start(func = [init, draw, step])


