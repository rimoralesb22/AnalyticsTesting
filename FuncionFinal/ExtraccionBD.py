import os
import cx_Oracle
import csv
def Valor(cuenta,ano1,ano2):
    SQL='''select sum(vf.precio_folleto1) AS Ganacia,
    avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1 as TotalCampanas,
    Round(avon.sku_CuentaCampana(vf.cuenta)/(avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1),2) as Participacion
    from avon.view_Factura2013_2015_3 vf  where vf.cuenta = '''+cuenta+''' and vf.ano between '''+ano1+''' and '''+ano2+'''
    group by vf.cuenta
    ORDER BY vf.cuenta'''
    return(SQL)
def Zona(cuenta,ano1,ano2):
    SQL='''select distinct(vf.zona)
    from avon.view_Factura2013_2015_3 vf  where vf.cuenta = '''+cuenta+''' and vf.ano between '''+ano1+''' and '''+ano2+''''''
    return SQL
def Producto(cuenta,ano1,ano2):
    SQL='''SELECT count (distinct vp.Categoria)  FROM avon.view_Productos2013_2015 vp where vp.cuenta = '''+cuenta+''' and vp.ano between '''+ano1+''' and '''+ano2+''''''
    return(SQL)

#SQL='''SELECT * from avon.av_negocio 117139'''

def escribirArchivo(cursor,Archivo):
    outfile = open(Archivo, 'a') # Indicamos el valor 'w'.
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
    cursor.close()    
    lista1=toString(lista)
    #escribirArchivo(lista1,archivo)

    
    #connection.close()
    return lista1
def ejecutar(SQL):
    connect('''SELECT count (distinct vp.Categoria)  FROM avon.view_Productos2013_2015 vp  where vp.cuenta = 12509 and vp.ano between 2013 and 2015''')




    #ejecutar(str(i))
#connection.close()    
    
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
