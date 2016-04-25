import os
import cx_Oracle
import csv

def inicio(inicio,final):
    SQL='''SELECT vp.cuenta,vp.campana,vp.NEGOCIO,vp.Categoria,sum(vp.cantidad*vp.Precio) as Monto,
    count(distinct vp.categoria) as CantidadCategoria,
    Round((sum(vp.cantidad*vp.Precio)/AVON.sku_CalculaMonto(vp.CUENTA,vp.campana))*100,2) as Porcentaje
    FROM avon.view_Productos2013_2015 vp where vp.cuenta between '''+inicio+''' and '''+final+''' 
    group by vp.cuenta,vp.campana,vp.NEGOCIO,vp.Categoria
    order by campana,negocio,categoria,porcentaje desc'''
    return(SQL)

#SQL='''SELECT * from avon.av_negocio 117139'''

def escribirArchivo(cursor):
    outfile = open('Query.csv', 'a') # Indicamos el valor 'w'.
    for i in cursor:       
        linea=','.join(i)+"\n"
        outfile.write(linea)
    outfile.close()

def toString(lista):
    for i in lista:
        for j in range (0,len(i)):
            i[j]=str(i[j])
    return lista  
    

def toList(cursor):
    lista=[]
    for i in cursor:
        temp=list(i)
        lista.append(temp)       
    return (lista)
    ##escribirArchivo(cursor)
        ##linea=','.join(i)+"\n"
        ##outfile.write(linea)
    

def connect(SQL): 
    # You can set these in system variables but just in case you didnt
    #os.putenv('ORACLE_HOME', '/oracle/product/10.2.0/db_1') 
    #os.putenv('LD_LIBRARY_PATH', '/oracle/product/10.2.0/db_1/lib') 

    #>>> db = cx_Oracle.connect('TESTER', 'D3loi773943$', '5.152.182.176:1521/')
    #>>> db1 = cx_Oracle.connect('hr/hrpwd@localhost:1521/XE')
    #dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'XE')
    dsn_tns = '(DESCRIPTION =    (ADDRESS_LIST =      (ADDRESS = (PROTOCOL = TCP)(HOST = 5.152.182.176)(PORT = 1521))    )    (CONNECT_DATA =  (SERVICE_NAME = DBAVON) ) )'
    connection = cx_Oracle.connect('TESTER', 'D3loi773943$', dsn_tns) 
    #connection = cx_Oracle.connect('TESTER/D3loi773943$@5.152.182.176:1521/DBAVON')
    #connection = cx_Oracle.connect('TESTER/D3loi773943$@5.152.182.176:1521/DBAVON')

    cursor = connection.cursor()
    cursor.execute(SQL)
    lista=toList(cursor)
    lista1=toString(lista)
    escribirArchivo(lista1)

    cursor.close()
    #connection.close()
def ejecutar():
    i=0
    while i <= 398000:
        SQL=inicio(str(i),str(i+1000))
        connect(SQL)
        i=i+1000
        
##DBAVONPRUEBAS=
##  (DESCRIPTION =
##    (ADDRESS_LIST =
##      (ADDRESS = (PROTOCOL = TCP)(HOST = 5.152.182.176)(PORT = 1521))
##    )
##    (CONNECT_DATA =
##      (SERVICE_NAME = DBAVON)
##    )
##  )
####
##User: TESTER
##Pass: D3loi773943$
## 
