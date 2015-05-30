from pyveplot import *
import networkx as nx
import random


h = Hiveplot( 'cerrito_actores.svg')


axis0 = Axis( (200,350), # start
              (200,50), # end
              stroke="grey", stroke_opacity="0.5", stroke_width="2.5") # pass SVG attributes of axes
# define as many axes as you need
axis1 = Axis( (280,400), (600,540), stroke="grey", stroke_opacity="0.5", stroke_width="2.5")
axis2 = Axis( (150,400), (80,450), stroke="grey", stroke_opacity="0.5", stroke_width="2.5")


h.axes.append( axis0 )
h.axes.append( axis1 )
h.axes.append( axis2 )


# a random network
#g = nx.erdos_renyi_graph(100,0.3)

#Graph from pickle
g = nx.read_gpickle('cerrito_actores')


# randomly distribute nodes in axes
the_axes = [ axis0,
             axis1,
             axis2, ]


civil = ['Col_Vereda_Cerrito', 'Docentes','UniPamplona', 'Universidades', 'MAFRACOL', 'APPA', 'ARTELANA', 'ARTEPAJA', 'ASOCAPRISER', 'ASOGANACER', 'ASOMATE', 'ASOMOARCE', 'ASOPAGAR', 'ASOPIGAR', 'Campesinos', 'CDS', 'CEI', 'Comunidad', 'Cristina_Rep_Legal_ASOMOARCE', 'DC,' 'Estudiantes', 'Finquero', 'Gloria_Calderon', 'Gps_Armados', 'Gps_Conservacion', 'Gps_Ecologistas', 'Jose_Florez_Historico', 'Lideres_Comunales', 'Maria_Florez_Historico', 'Normal_Pie_de_Cuesta', 'Normal', 'ONGs', 'Organizaciones', 'Padre_historico_1954', 'Padres_de_Familia', 'Serafito_Calderon', 'UAK/UWA', 'UIS', 'William_Bastos']

gobierno = ['Ceres', 'CGR', 'Hospital', 'ICA', 'SENA', 'Admon_Mpal', 'Alcalde', 'Alcaldia', 'ASOJUNTAS', 'BanAgrario', 'Bomberos', 'Camacho_Historico', 'CAS', 'COANDIS_Asoc_Mpal', 'Comisaria_Familia', 'COMULDESPA', 'Concejo_Mpal', 'Gob_Arauca', 'Gob_Boyaca', 'Gob_Casanare', 'Gob_Cundinamarca', 'Gobernacion', 'Gobierno', 'Gob_Santander', 'Ing_Planeacion', 'Inspeccion_de_policia', 'MinAgricultura', 'MinAmbiente', 'Of_Saneamiento_Ambiental', 'Personeria', 'Policia', 'Presidencia', 'Prov_Garcia_Rovira', 'Sec_Gobierno', 'Uribe']

empresas = ['CARBORIENTE', 'Empresas', 'Empresas-RQ', 'FRESCALECHE', 'Mineras', 'Multinacionales', 'Queserias']


offset = 0.0255
for n in gobierno:
    nd = Node(n)
    axis0.add_node(nd, offset)
    offset += 0.0255
    nd.dwg = nd.dwg.circle(center = (nd.x, nd.y),
                           r      = 3,
                           fill   = 'yellow',
                           fill_opacity = 0.5,
                           stroke = 'black',
                           stroke_width = 0.5)

offset = 0.024
for n in civil:
    nd = Node(n)
    axis1.add_node(nd, offset)
    offset += 0.024
    nd.dwg = nd.dwg.circle(center = (nd.x, nd.y),
                           r      = 3,
                           fill   = 'blue',
                           fill_opacity = 0.5,
                           stroke = 'black',
                           stroke_width = 0.5)
    
    
offset = 0.1
for n in empresas:
    nd = Node(n)
    axis2.add_node(nd, offset)
    offset += 0.1
    nd.dwg = nd.dwg.circle(center = (nd.x, nd.y),
                           r      = 3,
                           fill   = 'red',
                           fill_opacity = 0.5,
                           stroke = 'black',
                           stroke_width = 0.5)

# for n in g.nodes():
#     nd = Node(n)
#     a = random.choice(the_axes)
#     # at random offsets, add_node method calculates node's x,y
#     a.add_node(nd, random.random())

#     # alter node drawing after adding it to axis
#     if random.choice([True, False]):
#         nd.dwg = nd.dwg.circle(center = (nd.x, nd.y),
#                                r      = float(nx.degree(g, n)) / 20.0,
#                                fill   = 'orange',
#                                stroke = random.choice(['red','green','blue','purple']),
#                                stroke_width = 0.1)
#     else:
#         # nodes' drawings can be any SVG shape
#         degree = float(nx.degree(g, n)) / 20.0
#         nd.dwg = nd.dwg.rect(insert = (nd.x - (degree/2.0), nd.y - (degree/2.0)),
#                              size   = (degree, degree),
#                              fill   = 'green',
#                              stroke = random.choice(['red','green','blue','purple']),
#                              stroke_width = 0.1)




#edges from axis0 to axis1
for e in g.edges():
    if (e[0] in axis0.nodes) and (e[1] in axis1.nodes):
        h.connect(axis0, e[0],
                  45,  # source angle
                  axis1, e[1], 
                  -45, # target angle
                  stroke_width='0.6',  # pass any SVG attributes to an edge
                  stroke_opacity='0.7',
                  stroke='purple',
                  fill='none')

# edges from axis0 to axis2
for e in g.edges():
    if (e[0] in axis0.nodes) and (e[1] in axis2.nodes):
        h.connect(axis0, e[0], -45,
                  axis2, e[1], 45,
                  stroke_width='0.6',
                  stroke_opacity='0.7',
                  stroke='red',
                  fill='none')

# edges from axis1 to axis2
for e in g.edges():
    if (e[0] in axis1.nodes) and (e[1] in axis2.nodes):
        h.connect(axis1, e[0], 15,
                  axis2, e[1], -15,
                  stroke_width='0.6',
                  stroke_opacity='0.7',
                  stroke=random.choice(['blue', 'red', 'purple', 'green', 'magenta']),
                  fill='none')

h.save()
