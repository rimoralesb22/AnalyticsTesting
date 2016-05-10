from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import os
import time
import math
from ExtraccionBD import *
global dsn_tns
global user
global passwd

imprimir=[]

def porDefecto():
    
    tns3 = '(DESCRIPTION =    (ADDRESS_LIST =      (ADDRESS = (PROTOCOL = TCP)(HOST = 5.152.182.176)(PORT = 1521))    )    (CONNECT_DATA =  (SERVICE_NAME = DBAVON) ) )'
    user3 = 'TESTER'
    passwd3 = 'D3loi773943$'
    result = messagebox.askquestion("Restaurar", "¿Desea volver a los valores por defecto de la Base de Datos?", icon='warning')
    if result == 'yes':
        outfile = open("ConnectionData", 'w') # Indicamos el valor 'w'.       
        linea=tns3+','+user3+','+passwd3+'\n'
        outfile.write(linea)
        outfile.close()
        readDB()
        messagebox.showinfo(title="¡Listo!",message="Favor cerrar la aplicación para que los cambios surtan efecto")
    else:
        messagebox.showinfo(title="Información",message="No se han hecho cambios en los parametros de conexión de la base de datos")
    
    
def retrocedermenu():
    tree.delete(*tree.get_children())
    nom=txt.delete(1.0, END)
    ent3.delete(0,END)
    ent4.delete(0,END)
    ent3.insert(0, "2013")
    ent4.insert(0,"2015")
    panel.remove(fingresar)
    panel.add(frame)

def retrocedermenu1():
    nom=txt.delete(1.0, END)
    txt2.config(state=DISABLED,bg="dark gray")
    txt3.config(state=DISABLED,bg="dark gray")
    txt4.config(state=DISABLED,bg="dark gray")
    panel.remove(frameregis)
    panel.add(frame)

def modificarBD():
    txt2.config(state=NORMAL,bg="white")
    txt3.config(state="normal",bg="white")
    txt4.config(state=NORMAL,bg="white")

def guardarBD():
    tns=(txt2.get(1.0,END)[:-1])
    user2=(txt3.get(1.0,END)[:-1])
    passwd2=(txt4.get(1.0,END)[:-1])
    if tns!='':
        if user2!='':
            if passwd2!='':
                outfile = open("ConnectionData", 'w') # Indicamos el valor 'w'.       
                linea=tns+','+user2+','+passwd2+'\n'
                outfile.write(linea)
                outfile.close()
                txt2.config(state=DISABLED,bg="dark gray")
                txt3.config(state=DISABLED,bg="dark gray")
                txt4.config(state=DISABLED,bg="dark gray")
                readDB()
            else:
                messagebox.showinfo(title="Error",message="Password no puede estar vacio")
        else:
            messagebox.showinfo(title="Error",message="Usuario no puede estar vacio")
    else:
        messagebox.showinfo(title="Error",message="TNS NAME no puede estar vacio")
        
    
    
def modificar():    
    try:
        tree.delete(*tree.get_children())
        panel.remove(frame)
        panel.add(frameregis)
    except:
        tree.delete(*tree.get_children())
        panel.remove(fingresar)
        panel.add(frameregis)


def imprimirArchivo():
    global imprimir
    try:
        if imprimir!=[]:
            hora=time.strftime('%H%M%S')
            dia=time.strftime('%d%B%Y')
            outfile = open('Export'+dia+hora+'.csv', 'w') # Indicamos el valor 'w'.
            outfile.write('Cuenta,GrupoZona,GrupoProducto,GrupoValor\n')
            for i in imprimir:
                linea=','.join(i)+"\n"
                outfile.write(linea)
            outfile.close()
            messagebox.showinfo(title="¡Listo!",message='Archivo exportado Export'+dia+hora+'.csv')
    except:
        messagebox.showinfo(title="Error",message='''No se pudo exportar el archivo, no hay suficiente información para clasificar esta consultora,
\nVerificar columnas con la palabra None''')

def lecturaArchivo(archivo):
    f = open(archivo)
    lista=[]
    data1=[]
    data =f.readlines()
    for i in range (0,len(data)):
        data1=data[i].replace("\n", "")
        data1=data1.split(',')
        data1.append(1)
        lista.append(data1)
    return lista
def verificarZona(lista,Zona):
    for i in range (0,len(lista)):
        if lista[i][4]==str(Zona):
            return(lista[i][10])
def verificarProducto(producto):
    if int(producto)<=4:
        return "Especialista"
    else:
        return "Generalista"
def verificarValor(valor):
    temp=[0,0,0,0,0]
    for i in valor:
        tempGanancia=(float(i[0])-121617.9)/308901
        tempAntiguedad=(float(i[1])-38.31154)/53.98278
        tempParticiapacion=(float(i[2])-0.8049351)/0.2772263

        temp[0]=math.sqrt(pow((tempGanancia-1.6895731),2)+pow((tempAntiguedad-2.4434609),2)+pow((tempParticiapacion-0.4160024),2))
        temp[1]=math.sqrt(pow((tempGanancia--0.2950031 ),2)+pow((tempAntiguedad--0.4362777),2)+pow((tempParticiapacion--0.9556355),2))
        temp[2]=math.sqrt(pow((tempGanancia--0.2542144 ),2)+pow((tempAntiguedad--0.5476185),2)+pow((tempParticiapacion-0.5973422),2))
        temp[3]=math.sqrt(pow((tempGanancia-0.6701976),2)+pow((tempAntiguedad-0.6034230),2)+pow((tempParticiapacion-0.4649254 ),2))
        temp[4]=math.sqrt(pow((tempGanancia--0.2137478),2)+pow((tempAntiguedad-1.5045590),2)+pow((tempParticiapacion--2.1481070),2))
        indice=temp.index(min(temp))+1
        return(verificarValor_aux(indice))
def verificarValor_aux(cont):
    if cont==1:
        return 'Destacadas'
    elif cont==2:
        return 'Principiantes con necesidad de apoyo'
    elif cont ==3:
        return 'Principiantes con potencial'
    elif cont ==4:
        return 'Consolidadas'
    else:
        return 'Unión libre'
    
def cargarTree(lista):
    for i in lista:
        tree.insert("" , 0,    text="Consultora "+i[0], values=(i[1],i[2],i[3]))
    
def ingresar():
    global imprimir
    cuentas=(txt.get(1.0,END)[:-1]).split(",")
    ano1=ent3.get()
    ano2=ent4.get()
    if cuentas!=['']:
        if ano1!="":
            if ano2!="":
                if int(ano2)>int(ano1):
                    try:                    
                        temp=[]
                        listaFinal=[]
                        for i in cuentas:
                            try:
                                print("Ejecutando consultora "+i)
                                print("Porcentaje de ejecución: "+str(round((cuentas.index(i)+1)/len(cuentas)*100))+"%")
                                print("***************************************************")
                                print("***************************************************\n")
                                sqlZona=Zona(i,ano1,ano2)
                                zona=connect(sqlZona)
                                zonas1=(lecturaArchivo("kmeans-zona.csv"))
                                grupozona=verificarZona(zonas1,zona[0][0])

                                sqlProducto=Producto(i,ano1,ano2)
                                producto=connect(sqlProducto)

                                grupoproducto=verificarProducto(producto[0][0])

                                sqlValor=Valor(i,ano1,ano2)
                                valor=connect(sqlValor)                        
                                grupovalor=verificarValor(valor)
                                
                                temp.append(i)
                                temp.append(grupozona)
                                temp.append(grupoproducto)
                                temp.append(grupovalor)
                                listaFinal.append(temp)
                                temp=[]
                                imprimir=listaFinal
                                
                            except IndexError:
                                messagebox.showinfo(title="Error",message="No hay información disponible para la consultora: "+str(i))
                        print("\n\n*******************FINALIZADO**********************")        
                        cargarTree(listaFinal)
                        panel.remove(frame)
                        panel.add(fingresar)  
                          
                    except Exception as e: 
                         messagebox.showinfo(title="Error",message=str(e))
                else:
                    messagebox.showinfo(title="Error",message="El segundo año debe ser mayor al primero")  
            else:
                 messagebox.showinfo(title="Error",message="Debe incluir un rango de año")
        else:
             messagebox.showinfo(title="Error",message="Debe incluir un rango de año")          
    else:
        messagebox.showinfo(title="Error",message="Debe incluir un numero de cuenta")


root=Tk()
root.title("Analytics")

frameprin=ttk.Frame(root)
frameprin.pack(expand=YES)


panel=ttk.Panedwindow(frameprin, orient=VERTICAL)
panel.grid()

frame=ttk.Frame(frameprin)
fingresar=ttk.Frame(frameprin)
frameregis=ttk.Frame(frameprin)

panel.add(frame)

imagen = PhotoImage(file="Log.gif")
flogin = Label(frame,image=imagen)


flogin.image=imagen
flogin.grid(row=0,column=0,columnspan=10,rowspan=50)

btn=Button(frame,text="Buscar",command=ingresar,cursor="hand2",bg="white")
btn.place(x=400,y=400)
w = Label(frame, text="Número de Cuenta")
w.place(x=10,y=174)

ano = Label(frame, text="Años:")
ano.place(x=50,y=110)

txt= Text(flogin,width=20,height=13,bg="dark gray",font=("arial",14))
txt.place(x=120,y=160)

ent3=Entry(flogin,width=5,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray")
ent4=Entry(flogin,width=5,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray")

ent3.place(x=120,y=100)
ent4.place(x=220,y=100)

ent3.insert(0, "2013")
ent4.insert(0,"2015")


############ Menu
menubar = Menu(frame)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Modificar", command=modificar)
filemenu.add_command(label="Valores por Defecto", command=porDefecto)
menubar.add_cascade(label="Configuración de Base de Datos", menu=filemenu)
root.config(menu=menubar)
#=================================INGRESAR====================================================

imagen4 = PhotoImage(file="fondo ingresar.gif")
fpag = ttk.Label(fingresar,image=imagen4)
fpag.image=imagen4
fpag.grid(row=0,column=0,columnspan=10,rowspan=50)


tree = ttk.Treeview(fpag,height=20)
tree.place(x=80,y=50)
tree["columns"]=("Zona","Producto","Valor")
tree.column("Zona", width=100,stretch=NO)
tree.column("Producto", width=100,stretch=NO)
tree.column("Valor", width=100,stretch=NO)
tree.heading("Zona", text="Zona")
tree.heading("Producto", text="Producto")
tree.heading("Valor", text="Valor")



scbHDirSel = ttk.Scrollbar(fpag,
                           orient='horizontal',
                           command=tree.xview)
scbVDirSel = ttk.Scrollbar(fpag,
                           orient='vertical',
                           command=tree.yview)
tree.configure(xscrollcommand=scbHDirSel.set,
                    yscrollcommand=scbVDirSel.set)





btn5=Button(fpag,text="Atrás",command=retrocedermenu,cursor="hand2",bg="white")
btn5.place(x=500,y=500)

btn6=Button(fpag,text="Descargar Archivo",command=imprimirArchivo,cursor="hand2",bg="white")
btn6.place(x=300,y=500)


#================================REGISTRO==================================================================

imagen = PhotoImage(file="Log1.gif")
fregis = Label(frameregis,image=imagen)
fregis.image=imagen
fregis.grid(row=0,column=0,columnspan=10,rowspan=50)

txt2= Text(frameregis,width=50,height=6,bg="dark gray",font=("arial",14))
txt2.place(x=60,y=80)
txt2.insert(1.0,dsn_tns)

txt3= Text(frameregis,width=50,height=2,bg="dark gray",font=("arial",14))
txt3.place(x=60,y=250)
txt3.insert(1.0,user)

txt4= Text(frameregis,width=50,height=2,bg="dark gray",font=("arial",14))
txt4.place(x=60,y=330)
txt4.insert(1.0,passwd)

lbl7 = Label(frameregis, text="TNS Name")
lbl7.place(x=60,y=55)

lbl8 = Label(frameregis, text="User Name")
lbl8.place(x=60,y=223)

lbl9 = Label(frameregis, text="Password")
lbl9.place(x=60,y=305)

txt2.config(state=DISABLED)
txt3.config(state=DISABLED)
txt4.config(state=DISABLED)

btn6=Button(frameregis,text="Atrás",command=retrocedermenu1,cursor="hand2",bg="white")
btn6.place(x=500,y=500)

btn7=Button(frameregis,text="Modificar",command=modificarBD,cursor="hand2",bg="white")
btn7.place(x=300,y=500)

btn8=Button(frameregis,text="Guardar",command=guardarBD,cursor="hand2",bg="white")
btn8.place(x=400,y=500)




root.mainloop()
