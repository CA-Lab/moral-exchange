from pyveplot import *
import networkx as nx
import random


h = Hiveplot( 'cerrito_degree.svg')


axis0 = Axis( (500,1100), # start
              (500,20), # end
              stroke="grey", stroke_opacity="0.5", stroke_width="2.5") # pass SVG attributes of axes
# define as many axes as you need
axis1 = Axis( (600,1200), (1300,1350), stroke="grey", stroke_opacity="0.5", stroke_width="2.5")
axis2 = Axis( (460,1200), (286,1320), stroke="grey", stroke_opacity="0.5", stroke_width="2.5")
axis3 = Axis( (240,1352), (10,1508), stroke="grey", stroke_opacity="0.5", stroke_width="2.5")


h.axes.append( axis0 )
h.axes.append( axis1 )
h.axes.append( axis2 )
h.axes.append( axis3 )


# a random network
#g = nx.erdos_renyi_graph(100,0.3)

#Graph from pickle
g = nx.read_gpickle('cerrito_actores')


# randomly distribute nodes in axes
the_axes = [ axis0,
             axis1,
             axis2,
             axis3 ]


civil = ['APPA', 'ARTELANA', 'ARTEPAJA', 'ASOCAPRISER', 'ASOGANACER', 'ASOMATE', 'ASOPAGAR', 'ASOPIGAR', 'Campesinos', 'CDS', 'CEI', 'Comunidad', 'DC', 'Finquero', 'Gps_Armados', 'Gps_Conservacion', 'Gps_Ecologistas', 'Jose_Florez_(Historico)', 'Lideres_Comunales', 'Maria_Florez_(Historico)', 'ONGs', 'Organizaciones', 'Padre_(historico_1954)', 'UAK/UWA', 'UIS', 'ASOMOARCE']

gobierno = ['Ceres', 'CGR', 'Hospital', 'ICA', 'SENA', 'Admon_Mpal', 'Alcalde', 'Alcaldia', 'ASOJUNTAS', 'BanAgrario', 'Camacho_(Historico)', 'CAS', 'COANDIS_(Asoc_Mpal)', 'Comisaria_Familia', 'COMULDESPA', 'Concejo_Mpal', 'Gob_Arauca', 'Gob_Boyaca', 'Gob_Casanare', 'Gob_Cundinamarca', 'Gobernacion', 'Gobierno', 'Gob_Santander', 'Ing_Planeacion', 'Inspeccion_de_policia', 'MinAgricultura', 'MinAmbiente', 'Of_Saneamiento_Ambiental', 'Personeria', 'Presidencia', 'Prov_Garcia_Rovira', 'Uribe', 'Bomberos', 'Policia', 'Sec_Gobierno']

empresas = ['FRESCALECHE', 'MAFRACOL','Mineras', 'CARBORIENTE', 'Empresas', 'Empresas-RQ', 'Multinacionales', 'Queserias']

educacion = ['Docentes','UniPamplona', 'Universidades', 'Estudiantes', 'Gloria_Calderon', 'Normal_Pie_de_Cuesta', 'Padres_de_Familia', 'Serafito_Calderon', 'William_Bastos', 'Normal', 'Col_Vereda_Cerrito']

interviews = { 'ASOMOARCE': 'E1',
               'Bomberos':  'E2',
               'FRESCALECHE': 'E3',
               'Normal':    'E4',
               'Policia':   'E5',
               'MAFRACOL': 'E6',
               'Col_Vereda_Cerrito': 'E7',
               'Sec_Gobierno': 'E8'}

#for node in g.nodes():



offset = 0.025
for n in gobierno:
    #print nx.degree(g, n), n
    nd = Node(n)
    axis0.add_node(nd, offset)
    offset += 0.026
    nd.dwg.add(nd.dwg.circle(center = (nd.x, nd.y),
                               r      = 12,
                               #r      = nx.degree(g, n),
                               fill   = 'yellow',
                               fill_opacity = 0.5,
                               stroke = 'black',
                               stroke_width = 0.5))

    if n in interviews:
        nd.dwg.add(nd.dwg.text(interviews[n], insert=(nd.x, nd.y)))
    #nd.dwg.add(nd.dwg.text(n, insert=(nd.x, nd.y)))
    
offset = 0.037
for n in civil:
    #print nx.degree(g, n), n
    nd = Node(n)
    axis1.add_node(nd, offset)
    offset += 0.037
    nd.dwg.add(nd.dwg.circle(center = (nd.x, nd.y),
                                r      = 12,
                                #r      = nx.degree(g, n),
                                fill   = 'blue',
                                fill_opacity = 0.5,
                                stroke = 'black',
                                stroke_width = 0.5))
    if n in interviews:
        nd.dwg.add(nd.dwg.text(interviews[n], insert=(nd.x, nd.y)))


offset = 0.085
for n in educacion:
    #print nx.degree(g, n), n
    nd = Node(n)
    axis3.add_node(nd, offset)
    offset += 0.085
    nd.dwg.add(nd.dwg.circle(center = (nd.x, nd.y),
                                r      = 12,
                                #r      = nx.degree(g, n),
                                fill   = 'magenta',
                                fill_opacity = 0.5,
                                stroke = 'black',
                                stroke_width = 0.5))
    if n in interviews:
        nd.dwg.add(nd.dwg.text(interviews[n], insert=(nd.x, nd.y)))

offset = 0.11
for n in empresas:
    #print nx.degree(g, n), n
    nd = Node(n)
    axis2.add_node(nd, offset)
    offset += 0.11
    nd.dwg.add(nd.dwg.circle(center = (nd.x, nd.y),
                                r      = 12,
                                #r      = nx.degree(g, n),
                                fill   = 'red',
                                fill_opacity = 0.5,
                                stroke = 'black',
                                stroke_width = 0.5))
    if n in interviews:
        nd.dwg.add(nd.dwg.text(interviews[n], insert=(nd.x, nd.y)))
    
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
                  stroke_width='1.0',  # pass any SVG attributes to an edge
                  stroke_opacity='0.7',
                  stroke='purple',
                  fill='none')

#edges from axis0 to axis2        
for e in g.edges():
    if (e[0] in axis0.nodes) and (e[1] in axis2.nodes):
        h.connect(axis0, e[0], -45,  # source angle
                  axis2, e[1], 45, # target angle
                  stroke_width='1.0',  # pass any SVG attributes to an edge
                  stroke_opacity='0.7',
                  stroke='blue',
                  fill='none')       

        
# edges from axis0 to axis3
for e in g.edges():
    if (e[0] in axis0.nodes) and (e[1] in axis3.nodes):
        h.connect(axis0, e[0], -45,
                  axis3, e[1], 45,
                  stroke_width='1.0',
                  stroke_opacity='0.7',
                  stroke='red',
                  fill='none')

# edges from axis1 to axis2
for e in g.edges():
    if (e[0] in axis1.nodes) and (e[1] in axis2.nodes):
        h.connect(axis1, e[0], 15,
                  axis2, e[1], -15,
                  stroke_width='1.0',
                  stroke_opacity='0.7',
                  stroke=random.choice(['magenta']),
                  fill='none')

# edges from axis1 to axis3
for e in g.edges():
    if (e[0] in axis1.nodes) and (e[1] in axis3.nodes):
        h.connect(axis1, e[0], 15,
                  axis3, e[1], -15,
                  stroke_width='1.0',
                  stroke_opacity='0.7',
                  stroke=random.choice(['green']),
                  fill='none')
        
h.save()
