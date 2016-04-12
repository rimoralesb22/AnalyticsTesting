# load Practice data frame into memory
#   if not alredy there
source('DBConnection.r')

#Kmeans

rs <- dbSendQuery(con,"select vf.cuenta,sum(vf.precio_folleto1) AS Ganacia,
avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1 as TotalCampanas,
                  Round(avon.sku_CuentaCampana(vf.cuenta)/(avon.sku_CampanaTot(AVON.sku_CampanaMax(vf.cuenta))-avon.sku_campanatot(avon.sku_CampanaMin(vf.cuenta))+1),2) as Participacion
                  from avon.view_Factura2013_2015_3 vf 
                  group by vf.cuenta
                  ORDER BY vf.cuenta")

Clientes <- fetch(rs)
head(Clientes)
#Clientes<- transform(Clientes,NOMBRE = as.factor(Clientes$NOMBRE))

#Calcular la cantidad de clusters
#------------------------------------------------------------------------------------
# Crea vector "Errores", sin datos
# Crea variable "K_Max" con la cant. maxima de k a analizar
Errores <-NULL
K_Max   <-9

#------------------------------------------------------------------------------------
# Ejecuta kmeans con diferentes cluster, desde 1 hasta 9
# Luego guarda el error de cada ejecucion en el vector "Errores"
for (i in 1:K_Max)
{
  Errores[i] <- sum(kmeans(Clientes[-1], centers=i)$withinss)
}

#------------------------------------------------------------------------------------
# Grafica el vector "Errores"
plot(1:K_Max, Errores, type="b", 
     xlab="Cantidad de Cluster", 
     ylab="Suma de error")
#
#---------------------------------------------------------------------------------
# Creando los 3 Cluster o usando K-MEANS
#Luego asigna grupo a cada cliente en tabla Cliente
#ModeloKMEANS <- kmeans(Clientes[-1],3)
#Clientes$Grupo <- ModeloKMEANS$cluster

#---------------------------------------------------------------------------------
#Graficando los puntos de dispersi?n y luego asignando a cada punto etiquetas
#plot(Clientes$ANOSCONSULTORA,Clientes$GANANCIA,
#     col=Clientes$Grupo,cex.axis=.7,cex.lab=.7)

#text(Clientes$ANOSCONSULTORA,Clientes$GANANCIA,
#     labels=Clientes$CUENTA,pos=1,col=Clientes$Grupo,cex=.7)

#Salvando Datos , con el id del grupo
#write.csv(Clientes,"C:/Users/ricmorales/Desktop/BD/ganancia.csv")




#--------------------------------------------------------------#
# PASO 2: Crea vector con Algoritmos y tabla vacía para guardar Iteraciones
Algoritmos         <-c("Hartigan-Wong","Lloyd","Forgy","MacQueen") 
CantidadAlgoritmos <-length(Algoritmos) # guarda la cantidad de algoritmos usados
Iteraciones        <-data.frame(Intraclase=numeric(),Algoritmo=character())

#-------------------------------------------------------------------------

# PASO 3: Ejecuta k-means 10 veces en cada algoritmo
# y guarda la Distancia Intracluster de cada iteracion en la tabla Iteraciones
for (i in 1:CantidadAlgoritmos) 
{
  for (ii in 1:10) 
  {
    Modelo      <- kmeans(Clientes[-1],6, algorithm = Algoritmos[i])
    Iteraciones <- rbind(Iteraciones,
                         data.frame(Intraclase = Modelo$betweenss,
                                    Algoritmo = Algoritmos[i]))
  }
}

#-------------------------------------------------------------------------
# PASO 4: Calcula la media de Distancia Intracluster en cada algoritmo
#  e identificar Algoritmo Ganador 
Resultados       <- tapply(Iteraciones$Intraclase,Iteraciones$Algoritmo,mean) 
Resultados       <-sort(Resultados,decreasing = T)
AlgoritmoGanador <-names(Resultados[1])

#-------------------------------------------------------------------------
# PASO 5: Ejecuta kmeans con algoritmo ganador y asigna grupo a cada cliente
KmeansOptimizado <- kmeans(Clientes[2:3],6, algorithm = AlgoritmoGanador)
Clientes$Grupo   <-KmeansOptimizado$cluster

#-------------------------------------------------------------------------

#PASO 6: Grafica segmentacion de algoritomo ganador y luego asigna etiquetas
plot(Clientes$TOTALCAMPANAS,Clientes$GANANCIA,col=Clientes$Grupo,cex.axis=.7,cex.lab=.7)
text(Clientes$TOTALCAMPANAS,Clientes$GANANCIA,
     labels=Clientes$CUENTA,pos=1,col=Clientes$Grupo,cex=.7)
title(main=paste("Algoritmo ganador:",AlgoritmoGanador),cex.main=.9)

write.csv(Clientes,"C:/Users/ricmorales/Desktop/BD/ganancia_optimizado_6Clusters.csv")