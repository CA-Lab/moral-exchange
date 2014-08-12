#!/usr/bin/python

import networkx as nx
import random as rd
import pylab as pl
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



c = 0
d = 1


def init(): #posteriormente arreglar para escoger la condicion de
    #incio: dos cooperadores, cooperador vs detractor, dos
    #detractores o inicio aleatorio. Tambien para definir los valores
    #del fitness y de la confianza

    global time, nt, positions, next_nt, node_fitness, trust

    time = 0
    fit_1 = [] #Almacenar valores de fitness de nodo a
    fit_2 = [] #Almacenar valores de fitness de nodo b
    #fit_3 = [] #Almacenar valores de fitness de nodo c
    trust_1 = [] #Almacenar valores de confianza de el vinculo entre nodos a y b
    #trust_2 = [] #Almacenar valores de confianza de el vinculo entre nodos a y c
    #trust_3 = [] #Almacenar valores de confianza de el vinculo entre nodos b y c
    nt = nx.Graph()
    nt.add_node( 'a' )
    nt.add_node( 'b' )

    nt.node['a']['id'] = c
    nt.node['a']['w'] = 10 #fitness inicial
    nt.node['b']['id'] = d
    nt.node['b']['w'] = 10 #fitness inicial

    nt.add_edge( 'a', 'b' )
    nt.edge['a']['b']['t'] = 10 #Confianza incial de la relacion

init()

positions = nx.random_layout(nt)

# nx.draw(nt)
# plt.show()


def draw():
    pl.cla()
    nx.draw(nt, pos = positions, node_color = [nt.node[i]['id'] for i in nt.nodes_iter()], with_labels = True, edge_color = 'c', cmap = pl.cm.RdBu, vmin = 0, vmax = 1)
    #Falta dibujar el vinculo con el grosor del mismo representando el grado de confianza
    pl.axis('image')
    pl.title('t = ' + str(time))
    plt.show() 


def trust(i, j): #Funcion de evaluacion de la confianza
    global trust_1
    for i, j in nt.nodes(True):
        if nt.node[i]['id'] != nt.node[j]['id']:
           nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - regla

        if nt.node[i]['id'] == c and nt.node[j]['id'] == c:
            nt.edge[i][j]['t'] = nt.edge[i][j]['t'] + regla

        else:
            nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - regla
    trust_1.append( nt.edge[i][j]['t'] )


def fitness(i, j): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor
    
    for i, j in g.edges():
        if nt.node[i]['id'] == c and nt.node[j]['id'] == d:
            nt.node[i]['w'] = nt.node[i]['w'] - 1
            
        if nt.node[i]['id'] == d and nt.node[j]['id'] == c:
            nt.node[i]['w'] = nt.node[i]['w'] + 1

        if nt.node[i]['id'] == c and nt.node[j]['id'] == c:
            nt.node[i]['w'] = nt.node[i]['w'] + .5

        if nt.node[i]['id'] == d and nt.node[j]['id'] == d:
            nt.node[i]['w'] = nt.node[i]['w']


#def step():


def node_strategy(nodes): #players get their strategies randomly

    x = 0.5 #eventualmente modificar para que quien corra la simulacion elija la probabilidad de que el nodo salga cooperador o detractor.
    for i in nt.nodes():
        if x > rd.random():
            nt.node[i]['id'] = c
        else:
            nt.node[i]['id'] = d
draw()

#def ploteo():    

# import pycxsimulator
# pycxsimulator.GUI().start(func = [init, draw, step])


