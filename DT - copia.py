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

valoresResultados.sort()
valoresContenido.sort()
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
while(hijosRaiz<=len(valoresResultados)):
	aaa = raw_input("")
	print ("------------------")
	tree.show()
	if(len(hijo._fpointer)<valoresResultados and len(contenido)>2):

		label=menorColumna

		print("contenido antes de eliminar",contenido)
		print("voy a eliminar estos valores",str(valoresContenido[len(hijo._fpointer)]), " de esta columna ",menorColumna)
		elim=eliminarColumna(copy.deepcopy(contenido),copy.deepcopy(etiquetas),menorColumna,str(valoresContenido[len(hijo._fpointer)]))
		contenido=elim["contenido"]
		etiquetas=elim["etiquetas"]

		del entropias[:]
		for i in range(0,len(etiquetas)-1):
			entropias.append(calEntropia(contenido,i))

		print(contenido)
		print(entropias)
		print("Hijos Raiz", hijosRaiz)
		menorColumna=buscarMenor(entropias)
		print("valor", str(valoresContenido[len(hijo._fpointer)]))
		print("Menor Columna", menorColumna)
		print(contenido)
		xs =[]
		for i in range(0,len(valoresContenido)):
			x=UnaPos(contenido,str(valoresContenido[i]),menorColumna)
			xs.append(x)

		allZeroEnt=0
		for i in range(0,len(entropias)):
			if(entropias[i]<>0.0):
				allZeroEnt+=1

		ValoresActualesResultados = []
		for i in range(0,len(contenido)):
			if(not contenido[i][len(etiquetas)-1] in ValoresActualesResultados):
				ValoresActualesResultados.append(contenido[i][len(etiquetas)-1])

		print xs
		if (-1 in xs and len(xs)==1):
			histFunc.append(copy.deepcopy(contenido))
			hisEtiq.append(copy.deepcopy(etiquetas))
			if(hijo.identifier == 0):
				hijosRaiz+=1
			tree.create_node({"Etiqueta":etiquetas[menorColumna],"Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)
			histHij.append(tree.get_node(ide))
			hijo=tree.get_node(ide)

		else:
			if(allZeroEnt>=0 and len(contenido)>1 and len(ValoresActualesResultados)>=2):
				print "here"
				print(etiquetas)
				tree.create_node({"Etiqueta":etiquetas[0],"Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)
				padre = ide
				ide+=1
				tempTest = []
				for i in range(0,len(contenido)):
					if(not {"Valor":contenido[i][len(contenido[i])-1], "Camino":contenido[i][0]} in tempTest):
						tree.create_node({"Valor":contenido[i][len(contenido[i])-1], "Camino":contenido[i][0]},ide,padre)
						tempTest.append({"Valor":contenido[i][len(contenido[i])-1], "Camino":contenido[i][0]})
						ide+=1
				try:
					print ("--------BACKTRACKING----------")
					hijo=histHij.pop()
					contenido=histFunc.pop()
					etiquetas=hisEtiq.pop()

					del entropias[:]
					for i in range(0,len(etiquetas)-1):
						entropias.append(calEntropia(contenido,i))
					menorColumna=buscarMenor(entropias)
					print contenido
					print entropias
				except Exception:
					print "----DONE NOTHING TO BACKTRACK TO----"

			else:
				tree.create_node({"Valor":x, "Camino":valoresContenido[len(hijo._fpointer)]},ide,hijo.identifier)

			if(len(tree.get_node(0)._fpointer)==len(valoresResultados)):
				hijosRaiz=len(valoresResultados)+1
		ide+=1
	else:
		print ("--------BACKTRACKING----------")
		hijo=histHij.pop()
		contenido=histFunc.pop()
		etiquetas=hisEtiq.pop()

		del entropias[:]
		for i in range(0,len(etiquetas)-1):
			entropias.append(calEntropia(contenido,i))
		menorColumna=buscarMenor(entropias)
		print contenido
		print entropias

tree.show()