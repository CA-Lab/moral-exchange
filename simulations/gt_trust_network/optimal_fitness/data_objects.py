from time import sleep
import random as rd
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



#######################
# init some variables #
#######################
theta = 1




#############
# ORM setup #
#############
Base    = declarative_base()

# nodes have many edges, edges have at least two nodes #
nodes_edges = Table(
    "nodes_edges",
    Base.metadata,
    Column("fk_nodes", Integer, ForeignKey("nodes.id")),
    Column("fk_edges", Integer, ForeignKey("edges.id")),
)

# Node model #
class Node(Base):
    __tablename__='nodes'
    
    id      = Column(Integer, primary_key=True)
    fitness = Column(Integer)
    state   = Column(Boolean)
    
    edges   = relationship(
        "Edge",
        secondary=nodes_edges
    )

    
    def neighbors(self):
        nodes = set()
        for e in self.edges:
            for n in e.nodes:
                nodes.add(n)
        nodes.remove(self)
        return nodes

    
    # will I be True or False?
    def update_state(self):
        m = []    
        for e in self.edges:
            m.append( e.w )
        
        tau = sum(m)
        
        if not tau:
            tau = 0.0000000001
        
        d =  self.fitness / tau

        if d <= theta:
            self.state = not self.state

    
    def __repr__(self):
        return '<Node [%s] f=%i s=%s>' % (self.id, self.fitness, self.state)


# Edge model     #
class Edge(Base):
    __tablename__='edges'
    
    id    = Column(Integer, primary_key=True)
    w     = Column(Integer)
    
    nodes = relationship(
        "Node",
        secondary=nodes_edges
    )


    
    def prissoners_dilema( self ):    
        # interaction of nodes
        if self.nodes[0].state == True  and self.nodes[1].state ==  False:
            self.nodes[0].fitness += -2
            self.nodes[1].fitness += 2
            self.w += -1
                
        if self.nodes[0].state == False and self.nodes[1].state == True:
            self.nodes[0].fitness += 2
            self.nodes[1].fitness += -2
            self.w += -1
                
        if self.nodes[0].state == True  and self.nodes[1].state == True:
            self.nodes[0].fitness += 1
            self.nodes[1].fitness += 1
            self.w += 2
    
        if self.nodes[0].state == False and self.nodes[1].state ==  False:
            self.nodes[0].fitness += -1
            self.nodes[1].fitness += -1
            self.w += -2

        self.nodes[0].update_state()
        self.nodes[1].update_state()


        
    def __repr__(self):
        return '<Edge %s, w=%s>' % (self.nodes, self.w)










####################
# helper functions #
####################
def init_watts():
    g = nx.watts_strogatz_graph(150, 2, 0.3)
#    g = nx.barabasi_albert_graph(100, 15)
#    g = nx.erdos_renyi_graph(100, .3)

    for i in g.nodes():
        # choose random state
        g.node[i]['s'] = rd.choice([True, False])
        # all start with same fitness
        g.node[i]['f'] = 10

    for e in g.edges():
        g.add_edge(*e, w=10)

    return g






def network_to_db(g):
    session = Session()

    for n in g.nodes():
        node = Node(id      = n,
                    fitness = g.node[n]['f'],
                    state   = g.node[n]['s'])
        session.add(node)
    session.commit()

    
    for e in g.edges():
        u = session.query(Node).get(e[0])
        v = session.query(Node).get(e[1])

        edge = Edge( w     = g.get_edge_data(*e)['w'],
                     nodes = [u, v] )
        session.add(edge)
    session.commit()





def network_from_db():
    g = nx.Graph()
    # load nodes
    for n in session.query(Node).all():
        g.add_node(n.id, { 'f': n.fitness,
                           's': n.state })
    # load edges
    for e in session.query(Edge).all():
        g.add_edge(e.nodes[0].id,
                   e.nodes[1].id,
                   {'w': e.w })

    return g




def edge_from_edge( edge ):
    node    = rd.choice( edge.nodes )
    n_edges = list( node.edges )
    n_edges.remove( edge )
    if n_edges:
        return rd.choice(n_edges)
    else:
        return False





def random_prissoner_walk():
    session = Session()
    
    e = rd.choice( session.query(Edge).all() )
        
    while True:
        print "interaction", e
        try:
            e.prissoners_dilema()
            session.commit()
        except:
            session.rollback()
            raise
            print "rolled back"
        sleep(0.2) # makes ctl-break easier
        e = edge_from_edge( e )
        if not e:
            print "reached the border"
            e = rd.choice( session.query(Edge).all() )



