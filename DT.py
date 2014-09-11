# coding: cp437
import copy
from treelib import Node, Tree

fileName=""
fileName = raw_input('Digite la direccion o nombre del archivo:  ')
file = open(fileName,'r')
fileContent = file.read()

lineaTemporal = fileContent.split("\n")
etiquetas = lineaTemporal[0].split(",")
contenido = []

for i in range(1,len(lineaTemporal)):
	contenido.append(lineaTemporal[i].split(","))


#print(etiquetas)
#print(contenido)

valoresContenido = []
valoresResultados =[]

for i in range(0,len(contenido)):
	if(not contenido[i][len(etiquetas)-1] in valoresResultados):
		valoresResultados.append(contenido[i][len(etiquetas)-1])

for i in range(0,len(contenido)):
	for j in range(0,len(contenido[0])-1):
		if(not contenido[i][j] in valoresContenido):
			valoresContenido.append(contenido[i][j])

#print(valoresContenido)
#print(valoresResultados)

def calPosibilidad(columna,valColumna,resultado):
	contResultado = 0
	contvalColumna=0
	for i in range(0,len(contenido)):
		if(contenido[i][columna]==valColumna):
			contvalColumna+=1
			if (contenido[i][len(etiquetas)-1]==resultado):
				contResultado+=1

	contvalColumna=contvalColumna*1.0
	contResultado=contResultado*1.0
	#print(float(contResultado/contvalColumna))
	return float(contResultado/contvalColumna)


def calNumeroEnCol(columna,valColumna):
	contvalColumna=0
	for i in range(0,len(contenido)):
		if(contenido[i][columna]==valColumna):
			contvalColumna+=1

	return contvalColumna

def calEntropia(columna):
	posibilidades=[]
	result = 0
	for i in range(0,len(valoresContenido)):
		temp=1
		for j in range(0, len(valoresResultados)):
			temp=temp*float(calPosibilidad(columna,str(i),str(j)))

		temp2=float(calNumeroEnCol(columna,str(i)))
		posibilidades.append(float(temp*(temp2/len(contenido))))
		#print(posibilidades)

	for i in range(0,len(posibilidades)):
		result = result + posibilidades[i]

	print("Entropia para Columna",columna,result)
	return result

for i in range(0,len(etiquetas)):
	calEntropia(i)


