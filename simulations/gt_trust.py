#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import random as rd

c = 0
d = 1


def init(): #posteriormente arreglar para escoger la condicion de
    #incio: dos cooperadores, cooperador vs detractor, dos
    #detractores o inicio aleatorio. Tambien para definir los valores
    #del fitness y de la confianza

    global time, nt, positions, next_nt

    time = 0

    nt = nx.Graph()
    nt.add_node( 'a' )
    nt.add_node( 'b' )

    nt.node['a']['id'] = c
    nt.node['a']['w'] = 10
    nt.node['b']['id'] = d
    nt.node['b']['w'] = 10

    nt.add_edge( 'a', 'b' )
    nt.edge['a']['b']['t'] = 10

init()

positions = nx.random_layout(nt)

nx.draw(nt)
plt.show()



def trust(i, j): #Funcion de evaluacion de la confianza

    for i, j in nt.nodes(True):
        if nt.node[i]['id'] != nt.node[j]['id']:
           nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - regla

        if nt.node[i]['id'] = c and nt.node[j]['id'] = c:
            nt.edge[i][j]['t'] = nt.edge[i][j]['t'] + regla

        else:
            nt.edge[i][j]['t'] = nt.edge[i][j]['t'] - regla

def fitness(i, j): #funcion de evaluacion y actualizacion del fitness
    #de cada competidor



def ploteo():

def step():#no se si hace falta. Tal vez todo debe estar dentro de ploteo

def strategy_random():#players get their strategies randomly

import pycxsimulator
pycxsimulator.GUI().start(func = [init, draw, step])


