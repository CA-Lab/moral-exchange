from multiprocessing import Process
from time import sleep
import networkx as nx
import random as rd
import pymongo
from bson.objectid import ObjectId


client = pymongo.MongoClient("localhost", 27017)
db = client.trustnet


C = True
D = False


def init_watts():
    g = nx.watts_strogatz_graph(100, 2, 0.3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([C,D])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)
        
    return g


def network_to_mongo(g):
    db.trustnet.drop()

    for e in g.edges():
        u = { 'node': e[0] }
        u.update(g.node[e[0]]) 

        v = { 'node': e[1] }
        v.update(g.node[e[1]])

        edge = {'u': u,
                'v': v }
        edge.update(g.get_edge_data(*e))

        db.trustnet.save(edge)

        
def mongo_to_network():
    g = nx.Graph()

    for e in db.trustnet.find():
        u = e.pop("u")
        v = e.pop("v")
        e.pop("_id")

        g.add_edge(u['node'],v['node'],e)

        nid = u.pop("node")
        g.add_node(nid, u)

        nid = v.pop("node")
        g.add_node(nid, v)
            
    return g

g = init_watts()

network_to_mongo(g)
        
# def f(name):
#     g = nx.watts_strogatz_graph(9000, 3, 0.5)
#     while True:
#         cl = nx.average_clustering(g)
#         print 'hello', name
#         sleep(0.2)


# a = {}
# for n in range(1,14):
#     a[n] = Process(target=f, args=("pr %s" % n,))
#     a[n].start()

