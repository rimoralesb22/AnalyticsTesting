##Kmeans - Zona

# load Practice data frame into memory
#   if not alredy there

source('utils.R')

# install the xlsx package, if needed
# and load it into memory
ensure.loaded("data.table")

Zonas = read.csv("KmeansZona_outliers.csv")
zonastable <- data.frame(Zonas)
head(zonastable)

zonastable$Valor <-gsub(",","",zonastable$Valor)
zonastable$Saturacion <-gsub(",","",zonastable$Saturacion)
zonastable$Potencial <-gsub(",","",zonastable$Potencial)
zonastable$Homogeneidad <-gsub(",","",zonastable$Homogeneidad)

zonastable$Valor <-as.numeric(zonastable$Valor)
zonastable$Saturacion <-as.numeric(zonastable$Saturacion)
zonastable$Potencial <-as.numeric(zonastable$Potencial)
zonastable$Homogeneidad <-as.numeric(zonastable$Homogeneidad)

zonas2 = scale(zonastable[3:5], center = TRUE, scale = TRUE)
head(zonas2)


zonastable = cbind(zonas2,zona=zonastable$ZONA,homogeneidadReal=zonastable$Homogeneidad,valorReal=zonastable$Valor,saturacionReal=zonastable$Saturacion,potencialReal=zonastable$Potencial)
head(zonastable)
zonastable <- data.frame(zonastable)

#cor(zonastable[1:4])

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
  Errores[i] <- sum(kmeans(zonastable[1:3], centers=i)$withinss)
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
  for (ii in 1:100) 
  {
    Modelo      <- kmeans(zonastable[1:3],3, algorithm = Algoritmos[i])
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
KmeansOptimizado <- kmeans(zonastable[1:3],3, algorithm = AlgoritmoGanador)
zonastable$Grupo   <-KmeansOptimizado$cluster


#-------------------------------------------------------------------------

#PASO 6: Grafica segmentacion de algoritomo ganador y luego asigna etiquetas
plot(zonastable$Homogeneidad,zonastable$Potencial,col=zonastable$Grupo,cex.axis=.7,cex.lab=.7)
text(zonastable$Homogeneidad,zonastable$Potencial,
     labels=zonastable$ZONA,pos=1,col=zonastable$Grupo,cex=.7)
title(main=paste("Algoritmo ganador:",AlgoritmoGanador),cex.main=.9)

write.csv(zonastable,"C:/Users/ricmorales/Desktop/kmeans-zona.csv")
