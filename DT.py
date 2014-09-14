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

def calPosibilidad(contenido,columna,valColumna,resultado):
	contResultado = 0
	contvalColumna=0
	for i in range(0,len(contenido)):
		if(contenido[i][columna]==valColumna):
			contvalColumna+=1
			if (contenido[i][len(etiquetas)-1]==resultado):
				contResultado+=1

	contvalColumna=contvalColumna*1.0
	contResultado=contResultado*1.0
	try:
	#print(float(contResultado/contvalColumna))
		return float(contResultado/contvalColumna)
	except Exception:
		return 0


def calNumeroEnCol(contenido,columna,valColumna):
	contvalColumna=0
	for i in range(0,len(contenido)):
		if(contenido[i][columna]==valColumna):
			contvalColumna+=1

	if(contvalColumna==0):
		return 1
	else:
		return contvalColumna

def calEntropia(contenido,columna):
	posibilidades=[]
	result = 0
	for i in range(0,len(valoresContenido)):
		temp=1
		for j in range(0, len(valoresResultados)):
			temp=temp*float(calPosibilidad(contenido,columna,str(i),str(j)))

		temp2=float(calNumeroEnCol(contenido,columna,str(i)))
		posibilidades.append(float(temp*(temp2/len(contenido))))
		#print(posibilidades)

	for i in range(0,len(posibilidades)):
		result = result + posibilidades[i]

	#print("Entropia para Columna",columna,result)
	return result

def eliminarColumna(contenidoCopy,etiquetasCopy,columna,valor):
	etiquetasCopy.pop(columna)
	i=0
	while i < len(contenidoCopy):
		#print contenido[i]
		if(contenidoCopy[i][columna]<>valor):
			contenidoCopy.pop(i)
		else:
			contenidoCopy[i].pop(columna)
			i+=1

	return {"contenido":contenidoCopy, "etiquetas":etiquetasCopy}

def buscarMenor(entropias):
	temp=9999
	indicador = -99
	for i in range(0,len(entropias)):
		if(entropias[i]<temp):
			temp=entropias[i]
			indicador = i
	return indicador

def UnaPos(contenido, valorContenido,columna):
	algo=[]
	for i in range(0,len(valoresResultados)):
		temp=0
		for k in range(0, len(contenido)):
			if(contenido[k][columna]==valorContenido):
				if(contenido[k][len(etiquetas)-1]==valoresResultados[i]):
					temp+=1
		temp2 = {"valorContenido": valorContenido, "valorResultado": valoresResultados[i], "valor":temp}
		algo.append(copy.deepcopy(temp2))

	print(algo)
	numCeros = 0
	noCero = -1
	for i in range(0,len(algo)):
		if(algo[i]["valor"]==0):
			numCeros+=1
		else:
			noCero = i

	if(numCeros==(len(algo)-1)):
		return algo[noCero]["valorResultado"]
	else:
		return -1


#print(UnaPos(contenido,"1",3))
entropias =[]

for i in range(0,len(etiquetas)-1):
	entropias.append(calEntropia(contenido,i))
print entropias
menorColumna=buscarMenor(entropias)

tree=Tree()
tree.create_node({"Etiqueta":etiquetas[menorColumna] , "Camino": "Raiz", "CamElg":0},0)




historicoContenido = []
historicoEtiquetas =[]



hijo=tree.get_node(0)
histFunc=[]
histFunc.append(contenido)
histHij=[]
histHij.append(hijo)
hisEtiq=[]
hisEtiq.append(etiquetas)
hijosRaiz=0

ide=1
print UnaPos(contenido,"0",3)
while(hijosRaiz<=valoresResultados):
	print ("----")
	tree.show()
	if(len(hijo._fpointer)<valoresResultados):
		del entropias[:]
		label=menorColumna
		elim=eliminarColumna(copy.deepcopy(contenido),copy.deepcopy(etiquetas),menorColumna,str(valoresContenido[len(hijo._fpointer)]))
		contenido=elim["contenido"]
		histFunc.append(copy.deepcopy(contenido))
		etiquetas=elim["etiquetas"]
		hisEtiq.append(etiquetas)
		for i in range(0,len(etiquetas)-1):
			entropias.append(calEntropia(contenido,i))

		print(contenido)
		print (entropias)
		menorColumna=buscarMenor(entropias)
		print "Unapos: ",valoresContenido[len(hijo._fpointer)]," , ", menorColumna
		x=UnaPos(contenido,str(valoresContenido[len(hijo._fpointer)]),menorColumna)
		print "X=",x
		if (x==-1):
			if(hijo.identifier == 0):
				print("HIJO!")
				hijosRaiz+=1
			tree.create_node({"Etiqueta":etiquetas[menorColumna],"Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)
			histHij.append(tree.get_node(ide))
			hijo=tree.get_node(ide)
			

		else:
			if(len(entropias)==1 and entropias[0]==0.0):
				tree.create_node({"Etiqueta":etiquetas[0],"Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)
				padre = ide
				ide+=1
				for i in range(0,len(contenido)):
					tree.create_node({"Valor":contenido[i][len(etiquetas)-1], "Camino":contenido[i][0]},ide,padre)
					ide+=1

			else:
				tree.create_node({"Valor":x, "Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)

				if(tree.get_node(0)._fpointer==valoresResultados):
					hijosRaiz=valoresResultados+1
					hijo=histHij.pop()
					contenido=histFunc.pop()
					etiquetas=hisEtiq.pop()
		ide+=1
	else:
		hijo=histHij.pop()
		contenido=histFunc.pop()
		etiquetas=hisEtiq.pop()