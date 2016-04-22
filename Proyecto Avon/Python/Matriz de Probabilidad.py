import json
from pprint import pprint

##with open('Export20142015.json') as data_file:    
##    data = json.load(data_file)
listaFinal=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lista=[] 
def lecturaArchivo():
    f = open("Export_python_20142015 - Filtrado.csv")   
    data =f.readlines()
    for i in range (0,len(data)):
        data1=data[i].replace("\n", "")
        data1=data1.split(',')
        data1.append(1)
        lista.append(data1)
    conteoMatriz(lista)
#[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,15,c16,17,c18,c19]
def conteoMatriz(lista):
    contadorCeros=0
    for i in lista:
        for j in range (2,len(i)):
            if int(i[j]) == 0:
                contadorCeros+=1
            else:
                if contadorCeros!=0:
                    conteoCeros(contadorCeros)
                    contadorCeros=0          
def conteoCeros(cont):
    listaFinal[cont-1]+=1    
    
def escribirArchivo():
    outfile = open('Export_python_20142015.csv', 'a') # Indicamos el valor 'w'.
    for i in lista:
        linea=','.join(i)+"\n"
        outfile.write(linea)
    outfile.close()

lecturaArchivo()

#escribirArchivo()

