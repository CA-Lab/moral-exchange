import argparse
import data_objects as do
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph
from time import sleep





################################
# parse command line arguments #
################################
parser = argparse.ArgumentParser(description='prissoner dilema network simulation')
parser.add_argument('--db_url', default='sqlite:///db.sqlite', help='DB URL, default: sqlite:///db.sqlite')
# parser.add_argument('--mode', required=True, choices=['init','walk'])
args = parser.parse_args()


####################
# database connect #
####################
engine  = create_engine(args.db_url)
do.Session = sessionmaker(bind=engine)

# network as global
g = Graph()



def create_network_from_db():
    session = do.Session()
    # load nodes
    for n in session.query(do.Node).all():
        if n.state:
            fill = color(0.1,0.1,0.7)
        else:
            fill = color(0.7,0.1,0.1)

        g.add_node(id=n.id,
                   radius = n.fitness,
                   stroke = color(0,0,0,0), 
                   fill = fill,
                   text = False)

    # load edges
    for e in session.query(do.Edge).all():
        if e.w > 0:
            weight = e.w/60
        else:
            weight = 0.01

        g.add_edge(e.nodes[0].id, e.nodes[1].id,
                   length = 1.0, 
                   weight = weight,
                   stroke = color(0))




def update_network_from_db(canvas):
    session = do.Session()

    for n in session.query(do.Node).all():
        N = g.node(n.id)

        if n.fitness > 2:
            N.radius = n.fitness
        else:
            N.radius = 2

        if n.state:
            N.fill = color(0.1,0.1,0.7)
        else:
            N.fill = color(0.7,0.1,0.1)

    for e in session.query(do.Edge).all():
        E = g.edge(e.nodes[0], e.nodes[1])
        if E:
            if e.w > 0:
                E.weight = e.w/60
            else:
                E.weight = 0.01

    print "updated"

create_network_from_db()



# for node in g.nodes:
#     node.radius = node.radius + node.radius*node.weight

# for node in g.nodes:
#     if len(node.edges) == 1:
#         node.edges[0].length *= 0.1

g.distance         = 10  # Overall spacing between nodes.
g.layout.force     = 0.01 # Strength of the attractive & repulsive force.
g.layout.repulsion = 15   # Repulsion radius.

dragged = None
def draw(canvas):
    
    canvas.clear()
    background(1)
    translate(canvas.width/2, canvas.height/2)
    
    # With directed=True, edges have an arrowhead indicating the direction of the connection.
    # With weighted=True, Node.centrality is indicated by a shadow under high-traffic nodes.
    # With weighted=0.0-1.0, indicates nodes whose centrality > the given threshold.
    # This requires some extra calculations.
    g.draw(weighted=0.5, directed=False)
    g.update(iterations=4)
#    sleep(0.2)
#    print "updated"
    # Make it interactive!
    # When the mouse is pressed, remember on which node.
    # Drag this node around when the mouse is moved.
    dx = canvas.mouse.x - canvas.width/2 # Undo translate().
    dy = canvas.mouse.y - canvas.height/2
    global dragged
    if canvas.mouse.pressed and not dragged:
        dragged = g.node_at(dx, dy)
    if not canvas.mouse.pressed:
        dragged = None
    if dragged:
        dragged.x = dx
        dragged.y = dy
        
canvas.size = 1280, 1600
canvas.run(draw=draw, update=update_network_from_db)
