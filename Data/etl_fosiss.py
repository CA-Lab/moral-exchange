# coding: utf-8
import csv
import codecs
import pprint

projects = {}

with open('fosiss_titulos.csv', 'r') as csvfile:
    title_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in title_reader:
        titulo = row[1]
        projects[titulo] = {'year': row[0]}


# "TITULO DEL PROYECTO",INSTITUCIÓN,"RESPONSABLE TÉCNICO","NIVEL S.N.I.",DEMANDA
with open('fosiss_proyectos.csv', 'r') as csvfile:
    projects_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in projects_reader:
        titulo = row[0]
        if row[0] != "TITULO DEL PROYECTO":
            projects[titulo]['institution'] = row[1]
            projects[titulo]['responsable'] = row[2]
            projects[titulo]['sni level']   = row[3]
            projects[titulo]['demanda']     = row[4]


# discard duplicated field "institución"
#"TÍTULO DEL PROYECTO",INSTITUCIÓN,"NOMBRE COLABORADOR","NIVEL S.N.I. COLABORADOR","INSTITUCIÓN COLABORADOR",ESPECIALIDAD
with open('fosiss_colaboradores.csv', 'r') as csvfile:
    colaboradores_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in colaboradores_reader:
        titulo = row[0]
        colaborador = { 'name': row[2],
                        'nivel sni': row[3],
                        'institucion colaborador': row[4],
                        'especialidad': row[5] }
        if titulo != "TÍTULO DEL PROYECTO":
            try:
                if 'colaboradores' in projects[titulo]:
                    projects[titulo]['colaboradores'].append(colaborador)
                else:
                    projects[titulo]['colaboradores'] = [colaborador, ]
            except KeyError:
                print 'PROYECTO MISTERIO:', titulo
                
pprint.pprint(projects)
