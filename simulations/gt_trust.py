#!/usr/bin/python

import networkx as nx
import random as rd
import pylab as pl
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



c = 0
d = 1


def init(): #posteriormente arreglar para escoger la condicion de
    #incio: dos cooperadores, cooperador vs detractor, dos
    #detractores o inicio aleatorio. Tambien para definir los valores
    #del fitness y de la confianza

    global time, nt, positions

    time = 0
    
    nt = nx.Graph()
    nt.add_node( 'a' )
    nt.add_node( 'b' )

    #nt.node['a']['id'] = c
    #nt.node['b']['id'] = d

    nt.node['a']['w'] = 10 #fitness inicial
    nt.node['b']['w'] = 10 #fitness inicial

    nt.add_edge( 'a', 'b' )
    nt.edge['a']['b']['t'] = 10 #Confianza incial de la relacion
    
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

def node_strategy(nodes): #players get their strategies randomly

    x = 0.5 #eventualmente modificar para que quien corra la simulacion elija la probabilidad de que el nodo salga cooperador o detractor.
    for i in nt.nodes():
        if x > rd.random():
            nt.node[i]['id'] = c
        else:
            nt.node[i]['id'] = d
    return nt.nodes(True)


def fitness(nodes): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor
    for i, j in nodes:
        for i, j in nt.edges():
            if nt.node[i]['id'] == c and nt.node[j]['id'] == d:
                nt.node[i]['w'] = nt.node[i]['w'] - 1
                nt.node[j]['w'] = nt.node[j]['w'] - 2
            
            if nt.node[i]['id'] == d and nt.node[j]['id'] == c:
                nt.node[i]['w'] = nt.node[i]['w'] + 2
                nt.node[j]['w'] = nt.node[j]['w'] - 1

            if nt.node[i]['id'] == c and nt.node[j]['id'] == c:
                nt.node[i]['w'] = nt.node[i]['w'] + .5
                nt.node[j]['w'] = nt.node[j]['w'] + .5

            if nt.node[i]['id'] == d and nt.node[j]['id'] == d:
                nt.node[i]['w'] = nt.node[i]['w'] - 2
                nt.node[j]['w'] = nt.node[j]['w'] - 2
    return nodes


def trust(nodes): #Funcion de evaluacion de la confianza
    for i, j in nodes:
        for i, j in nt.edges():
            if nt.node[i]['id'] != nt.node[j]['id']:
                nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - 1
                
            if nt.node[i]['id'] == c and nt.node[j]['id'] == c:
                nt.edge[i][j]['t'] = nt.edge[i][j]['t'] + 2

            if nt.node[i]['id']==d and nt.node[j]['id']==d:
                nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - 2

            trust_1 = nt.edge[i][j]['t']
        return trust_1

def step():
    global time, nt, positions
    
    time += 1
    
    for nodes in nt.nodes():
        nodes = node_strategy(nodes)
        fitness(nodes)
        t_degree = trust(nodes)
    
    return  nodes, t_degree

step()
#draw()

#def ploteo():    

#import pycxsimulator
#pycxsimulator.GUI().start(func = [init, draw, step])


