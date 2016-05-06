from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import os
import time
import math
from ExtraccionBD import *
imprimir=[]

def retrocedermenu():
    tree.delete(*tree.get_children())
    nom=txt.delete(1.0, END)  
    panel.remove(fingresar)
    panel.add(frame)


def imprimirArchivo():
    global imprimir
    hora=time.strftime('%H%M%S')
    dia=time.strftime('%d%B%Y')
    outfile = open('Export'+dia+hora+'.csv', 'w') # Indicamos el valor 'w'.
    outfile.write('Cuenta,GrupoZona,GrupoProducto,GrupoValor\n')
    for i in imprimir:
        linea=','.join(i)+"\n"
        outfile.write(linea)
    outfile.close() 	

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
            return(lista[i][9])
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
    #contrasenna=ent1.get()
    if cuentas!=['']:
        if ano1!="":
            if ano2!="":
                try:                    
                    temp=[]
                    listaFinal=[]
                    for i in cuentas:
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
                    cargarTree(listaFinal)
                    panel.remove(frame)
                    panel.add(fingresar)   
                      
                except ValueError:
                     messagebox.showinfo(title="Error",message="Lo que digito no es valido")
                     nombre=ent.delete(0,END)
                     ano1=ent3.delete(0,END)
                     ano2=ent4.delete(0,END)
                
                except TypeError:
                    messagebox.showinfo(title="Error",message="Usted no es un usuario Registrado")
                    nombre=ent.delete(0,END)
                    contrasenna=ent1.delete(0,END)                
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
frameprin["padding"]=(10,10) # Establece un Borde

panel=ttk.Panedwindow(frameprin, orient=VERTICAL)
panel.grid()

frame=ttk.Frame(frameprin)
fingresar=ttk.Frame(frameprin)
frameregis=ttk.Frame(frameprin)
frameventas=ttk.Frame(frameprin)
fnuevo=ttk.Frame(frameprin)
fusados=ttk.Frame(frameprin)
frm_adminmo=ttk.Frame(frameprin)
modiregis=ttk.Frame(frameprin)
frm_adminmo1=ttk.Frame(frameprin)
frm_adminmo2=ttk.Frame(frameprin)
frm_adminmo3=ttk.Frame(frameprin)

panel.add(frame)

imagen = PhotoImage(file="Log.gif")
flogin = Label(frame,image=imagen)

##imagen1 = PhotñoImage(file="salir.gif")
##flogin1 = Label(frame,image=imagen1)
##imagen2 = PhotoImage(file="Boton ingresar.gif")
##flogin2 = Label(frame,image=imagen2)
##imagen3 = PhotoImage(file="registrarse.gif")
##flogin3 = Label(frame,image=imagen3)

flogin.image=imagen
flogin.grid(row=0,column=0,columnspan=10,rowspan=50)

btn=Button(frame,text="Buscar",command=ingresar,cursor="hand2",bg="white")
btn.place(x=400,y=400)
w = Label(frame, text="Número de Cuenta")
w.place(x=10,y=174)

ano = Label(frame, text="Años:")
ano.place(x=50,y=110)
##btn1=Button(frame,image=imagen2,command=ingresar,relief="flat",cursor="hand2",bg="red")
##btn1.place(x=180,y=300)
##
##
##btn2=Button(frame,image=imagen3,command=registrarse,relief="flat",cursor="hand2",bg="gold")
##btn2.place(x=60,y=300)


#ent=Entry(flogin,width=30,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray")

txt= Text(flogin,width=20,height=13,bg="dark gray",font=("arial",14))
txt.place(x=120,y=160)

ent3=Entry(flogin,width=5,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray")
ent4=Entry(flogin,width=5,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray")
#ent1=Entry(flogin,width=29,relief="flat",borderwidth=7,font=("arial",14),bg="dark gray",show="*")
#ent.place(x=120,y=164)
ent3.place(x=120,y=100)
ent4.place(x=220,y=100)

ent3.insert(0, "2013")
ent4.insert(0,"2015")
#ent1.place(x=33,y=231)


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




#nuevo = PhotoImage(file="nuevos.gif")
btn5=Button(fpag,text="Atrás",command=retrocedermenu,cursor="hand2",bg="white")
btn5.place(x=500,y=500)

btn6=Button(fpag,text="Descargar Archivo",command=imprimirArchivo,cursor="hand2",bg="white")
btn6.place(x=300,y=500)

##usados = PhotoImage(file="usados.gif")
##btn6=Button(fpag,image=usados,command=usados_,relief="flat",cursor="hand2",bg="blue")
##btn6.place(x=300,y=40)
##
##venta = PhotoImage(file="ventas.gif")
##btn7=Button(fpag,image=venta,command=ventas,relief="flat",cursor="hand2",bg="yellow")
##btn7.place(x=500,y=40)
